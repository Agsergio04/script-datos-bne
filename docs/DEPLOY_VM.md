# Despliegue en una máquina virtual con Apache + Docker

Guía para desplegar el proyecto en una VM Ubuntu/Debian conviviendo con un
Apache existente (típicamente un servidor que ya sirve otra aplicación PHP
como **Dédalo**, **WordPress**, etc.).

Resultado: la app accesible en `http(s)://tu-dominio/bne/` sin tocar el resto
del servidor.

> Esta guía está escrita en base a un despliegue real en
> `dedalo.uca.es/bne/` (Ubuntu 24.04 + Apache 2.4 + Docker), pero sirve para
> cualquier VM con Apache y Docker.

---

## 0. Seguridad antes de nada

- Las contraseñas de servidor y BD que te facilite el servicio informático
  **no se commitean** en el repo. Van en un `.env` con permisos `chmod 600`.
- Cambia tu contraseña con `passwd` al primer login por SSH.
- Si tu administrador comparte credenciales por correo o chat sin cifrar,
  pídele rotarlas y guárdalas tú en un gestor de contraseñas.

## 1. Conectarse y diagnóstico

```bash
ssh <usuario>@<servidor>
passwd                      # cambia tu contraseña

cat /etc/os-release         # distribución
sudo -v && echo "sudo OK"
docker --version 2>/dev/null || echo "sin Docker"
sudo ss -tlnp | grep -E ':(80|443|3000|5000|5432)\b'
```

Anota qué puertos están ocupados. Lo habitual:
- **80 / 443** → Apache (la otra aplicación ya servida).
- **5432** → un PostgreSQL nativo del sistema, si lo hay.

## 2. Instalar Docker (si no está)

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
exit
```
Vuelve a entrar por SSH y verifica:
```bash
docker run --rm hello-world
```

## 3. Clonar el proyecto

```bash
sudo mkdir -p /opt/bne && sudo chown $USER:$USER /opt/bne
cd /opt/bne
git clone https://github.com/Agsergio04/script-datos-bne.git
cd script-datos-bne
```

## 4. Configurar el `.env` (CRÍTICO)

```bash
cat > .env <<'EOF'
POSTGRES_DB=bne_db
POSTGRES_USER=bne_user
POSTGRES_PASSWORD=<contraseña-larga-aleatoria>
SECRET_KEY=<otra-cosa-larga-aleatoria>
REACT_APP_API_URL=http://<tu-dominio>/bne
PGADMIN_EMAIL=admin@<tu-dominio>
PGADMIN_PASSWORD=<otra-contraseña>
EOF
chmod 600 .env
```

⚠️ **Detalle muy importante**: `REACT_APP_API_URL` **NO debe terminar en `/api`**.
El código del frontend ya añade `/api/...` por su cuenta. Si pones
`http://.../bne/api`, las peticiones salen como `http://.../bne/api/api/...`
y dan 404.

- ✅ Correcto: `REACT_APP_API_URL=http://dedalo.uca.es/bne`
- ❌ Incorrecto: `REACT_APP_API_URL=http://dedalo.uca.es/bne/api`

Y si tu servidor **no termina SSL** para tu VM (Apache sin vhost `:443` propio),
usa `http://` aquí — sino el navegador hará peticiones a `https://` que no
responden.

## 5. Ajustar puertos en `docker-compose.yml`

Si el servidor ya tiene un PostgreSQL nativo en `:5432` (muy común), mueve el
del proyecto a `:5433` para no chocar. Y enlaza **todos los puertos a
`127.0.0.1`** para que solo Apache los exponga al exterior:

```bash
sed -i \
  -e 's|^\(\s*-\s*\)"5432:5432"|\1"127.0.0.1:5433:5432"|' \
  -e 's|^\(\s*-\s*\)"5000:5000"|\1"127.0.0.1:5000:5000"|' \
  -e 's|^\(\s*-\s*\)"3000:3000"|\1"127.0.0.1:3000:3000"|' \
  -e 's|^\(\s*-\s*\)"5050:80"|\1"127.0.0.1:5050:80"|' \
  docker-compose.yml

grep -nE 'ports|127\.0\.0\.1' docker-compose.yml   # verifica
```

Resultado esperado:
```
- "127.0.0.1:5433:5432"     ← db
- "127.0.0.1:5000:5000"     ← backend
- "127.0.0.1:3000:3000"     ← frontend
- "127.0.0.1:5050:80"       ← pgAdmin
```

## 6. Levantar los servicios

```bash
docker compose up -d --build
sleep 8
docker compose ps
docker compose logs db --tail 30
```

Los 4 contenedores deben estar `(healthy)`. Verifica en local:
```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:3000/health
```

## 7. Configurar Apache como proxy a `/bne/`

```bash
sudo tee /etc/apache2/conf-available/bne.conf >/dev/null <<'EOF'
# Proyecto BNE — convive con la aplicación principal del servidor
<Location /bne/>
    ProxyPass        http://127.0.0.1:3000/
    ProxyPassReverse http://127.0.0.1:3000/
</Location>
<Location /bne/api/>
    ProxyPass        http://127.0.0.1:5000/api/
    ProxyPassReverse http://127.0.0.1:5000/api/
</Location>
<Location /bne/health>
    ProxyPass        http://127.0.0.1:5000/health
    ProxyPassReverse http://127.0.0.1:5000/health
</Location>
EOF

sudo a2enmod proxy proxy_http
sudo a2enconf bne
sudo apache2ctl configtest      # debe decir "Syntax OK"
sudo systemctl reload apache2
```

## 8. Verificar

Desde la VM:
```bash
curl -I http://localhost/bne/health         # 200 OK
curl    http://localhost/bne/api/info       # JSON
```

Desde tu portátil, abre en el navegador:
**`http://<tu-dominio>/bne/`**

Importa una obra para probar el flujo completo:
1. Pestaña **Periódicos → Por URL**
2. Pega: `https://datos.bne.es/edicion/bimo0000659916.html`
3. Importar → debe aparecer con portada BDH.

---

## Problemas comunes y soluciones

### a) Postgres no arranca (en bucle de reinicio)

Síntoma — `docker compose logs db` muestra:
> `Error: in 18+, these Docker images are configured to store database data in a format...`

Causa: Postgres 18 cambió el punto de montaje del volumen. Está corregido en
versiones recientes del repo, pero si tu copia es antigua:

```bash
sed -i 's|postgres_data:/var/lib/postgresql/data|postgres_data:/var/lib/postgresql|' docker-compose.yml
docker compose down -v      # ¡borra el volumen vacío!
docker compose up -d --build
```

### b) En el navegador la app carga pero los botones no hacen nada

Abre DevTools → Network. Si ves peticiones a **`/bne/api/api/...`** (doble
`api`), tu `REACT_APP_API_URL` tiene `/api` al final. Quítalo:

```bash
sed -i 's|REACT_APP_API_URL=.*|REACT_APP_API_URL=http://<tu-dominio>/bne|' .env
docker compose build --no-cache frontend
docker compose up -d frontend
```
Luego en el navegador: **Ctrl+Shift+R** (o pestaña incógnita) para saltar
caché.

### c) `ERR_SSL_PROTOCOL_ERROR` / `wrong version number`

Tu Apache no termina SSL para esta VM (no hay `<VirtualHost *:443>`).
Soluciones por orden de preferencia:

1. **Si el dominio principal sí tiene HTTPS** (lo termina algo externo de la
   institución), pide al servicio informático que también enrute `/bne/`
   sobre HTTPS hacia tu VM.
2. **Mientras tanto**, sirve la app en HTTP (`REACT_APP_API_URL=http://...`).
3. Más adelante, configura SSL en tu Apache con Let's Encrypt o el
   certificado institucional.

### d) Puerto 5432 ocupado

Hay un PostgreSQL nativo en el sistema. No lo desactives — usa `:5433` para
el contenedor (paso 5). El backend dentro del contenedor sigue hablando con
`db:5432` por la red interna de Docker; el `5433` solo es para acceso desde
el host (p. ej. con `psql -p 5433`).

---

## Mantenimiento

### Actualizar a la última versión del código
```bash
cd /opt/bne/script-datos-bne
git pull
docker compose up -d --build
```

### Logs en vivo
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Backup de la BD (cron diario)
```bash
sudo tee /etc/cron.d/bne-backup >/dev/null <<EOF
30 3 * * * <usuario> cd /opt/bne/script-datos-bne && docker compose exec -T db pg_dump -U bne_user bne_db | gzip > /var/backups/bne_\$(date +\%F).sql.gz
EOF
```

### Parar / reiniciar
```bash
docker compose down              # parar (mantiene datos)
docker compose down -v           # parar y BORRAR la BD (¡cuidado!)
docker compose restart backend   # solo el backend
```

### Cambiar contraseñas
1. Edita `.env` en el servidor.
2. `docker compose down && docker compose up -d` (la BD existente ya tiene su
   user/pass; cambiar `POSTGRES_PASSWORD` aquí solo afecta a nuevas inicializaciones).
   Para cambiar la contraseña de la BD existente:
   ```bash
   docker compose exec -T db psql -U bne_user -d bne_db -c "ALTER USER bne_user WITH PASSWORD '<nueva>';"
   ```

---

## Resumen ejecutivo

| Recurso | Dónde | Puerto |
|---|---|---|
| Frontend | Apache `/bne/` → contenedor nginx | 80 (vía Apache) |
| Backend  | proxy `/bne/api/` → contenedor Flask | interno `:5000` |
| Postgres | contenedor (datos en volumen Docker) | interno `:5433` |
| pgAdmin  | sin exponer; SSH-tunnel si lo necesitas | interno `:5050` |
| Otra app (Dédalo, etc.) | Apache, sin tocar | sin tocar |
