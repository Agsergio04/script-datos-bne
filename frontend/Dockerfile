# Dockerfile para el Frontend (React)
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Crear archivo .env con valores por defecto
RUN echo "REACT_APP_API_URL=http://localhost:5000" > .env

# Build
RUN npm run build

# Stage de producción
FROM nginx:alpine

# Copiar build de la etapa anterior
COPY --from=builder /app/build /usr/share/nginx/html

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 3000

# Comando para iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
