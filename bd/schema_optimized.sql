-- Esquema optimizado para PostgreSQL 18
-- Incluye constraints, índices y optimizaciones

-- ============================================================
-- TABLAS BASE
-- ============================================================

CREATE TABLE usuario (
    id_usuario BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(255) UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE laboratorio (
    id_laboratorio BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE proyectos (
    id_proyecto BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    cita TEXT,
    usuario_id BIGINT,
    laboratorio_id BIGINT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_proyectos_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_proyectos_laboratorio
        FOREIGN KEY (laboratorio_id) REFERENCES laboratorio(id_laboratorio)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT check_nombre_no_vacio CHECK (nombre != '')
);

CREATE TABLE lugar (
    id_lugar BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    lugar_principal BOOLEAN DEFAULT FALSE,
    lugar_secundario BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_no_ambos_tipos CHECK (NOT (lugar_principal AND lugar_secundario))
);

CREATE TABLE personajes (
    id_personaje BIGSERIAL PRIMARY KEY,
    personaje_principal VARCHAR(255),
    personaje_secundario VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_personaje_existente CHECK (personaje_principal IS NOT NULL OR personaje_secundario IS NOT NULL)
);

-- ============================================================
-- TABLA PRINCIPAL: OBRA
-- ============================================================

CREATE TABLE obra (
    id_obra BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(500) NOT NULL,
    tipo_publicacion VARCHAR(100),
    autor_firma VARCHAR(255),
    nombre_autor VARCHAR(255),
    anio INT CHECK (anio > 1400 AND anio <= EXTRACT(YEAR FROM CURRENT_DATE)),
    enlace TEXT UNIQUE,
    fecha DATE,
    dia INT CHECK (dia >= 1 AND dia <= 31),
    mes INT CHECK (mes >= 1 AND mes <= 12),
    num_periodico VARCHAR(100),
    variante_titulo VARCHAR(255),
    pseudonimos_autor VARCHAR(255),
    tema_principal VARCHAR(255),
    paginas VARCHAR(50),
    imprenta VARCHAR(255),
    como_citar TEXT,
    lugar_impresion VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_titulo_no_vacio CHECK (titulo != ''),
    CONSTRAINT check_fecha_valida CHECK (
        (fecha IS NULL) OR (
            EXTRACT(DAY FROM fecha) = dia AND 
            EXTRACT(MONTH FROM fecha) = mes AND 
            EXTRACT(YEAR FROM fecha) = anio
        )
    )
);

-- ============================================================
-- TABLAS DE TIPOS DE OBRAS (Herencia)
-- ============================================================

CREATE TABLE teatro (
    id_obra BIGINT PRIMARY KEY,
    fuente_procedencia TEXT,
    resumen TEXT,
    modalidad_teatro VARCHAR(100),
    otros_motivos TEXT,
    CONSTRAINT fk_teatro_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE novela (
    id_obra BIGINT PRIMARY KEY,
    fragmento_donde_aparece TEXT,
    otros_motivos TEXT,
    modalidad_novela VARCHAR(100),
    tipo_de_ubicacion VARCHAR(100),
    aspectos_formales TEXT,
    observaciones TEXT,
    como_citar TEXT,
    fuente_procedencia TEXT,
    CONSTRAINT fk_novela_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE periodico (
    id_obra BIGINT PRIMARY KEY,
    modalidad_periodico VARCHAR(100),
    num_periodico VARCHAR(100),
    fragmento_donde_aparece TEXT,
    CONSTRAINT fk_periodico_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE poesia (
    id_obra BIGINT PRIMARY KEY,
    aspectos_formales TEXT,
    resumen TEXT,
    fuente_procedencia TEXT,
    modalidad_poesia VARCHAR(100),
    CONSTRAINT fk_poesia_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE musica_impresa (
    id_obra BIGINT PRIMARY KEY,
    resumen TEXT,
    aspectos_formales TEXT,
    observaciones TEXT,
    modalidad_musica_impresa VARCHAR(100),
    CONSTRAINT fk_musica_impresa_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE narracion_breve (
    id_obra BIGINT PRIMARY KEY,
    observaciones TEXT,
    otros_motivos TEXT,
    modalidad_narracion_breve VARCHAR(100),
    CONSTRAINT fk_narracion_breve_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE poema (
    id_obra BIGINT PRIMARY KEY,
    observaciones TEXT,
    modalidad_poema VARCHAR(100),
    num_de_periodico VARCHAR(100),
    fuente_de_preferencia TEXT,
    lugar_de_impresion VARCHAR(255),
    modalidad_de_periodico VARCHAR(100),
    CONSTRAINT fk_poema_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- ============================================================
-- TABLAS ASOCIATIVAS (M:N)
-- ============================================================

CREATE TABLE obra_lugar (
    id_obra BIGINT NOT NULL,
    id_lugar BIGINT NOT NULL,
    PRIMARY KEY (id_obra, id_lugar),
    CONSTRAINT fk_obra_lugar_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_obra_lugar_lugar
        FOREIGN KEY (id_lugar) REFERENCES lugar(id_lugar)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE obra_personajes (
    id_obra BIGINT NOT NULL,
    id_personaje BIGINT NOT NULL,
    PRIMARY KEY (id_obra, id_personaje),
    CONSTRAINT fk_obra_personajes_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_obra_personajes_personaje
        FOREIGN KEY (id_personaje) REFERENCES personajes(id_personaje)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE proyecto_obra (
    id_proyecto BIGINT NOT NULL,
    id_obra BIGINT NOT NULL,
    fecha_insercion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_proyecto, id_obra),
    CONSTRAINT fk_proyecto_obra_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_proyecto_obra_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- ============================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================

-- Índices en tablas base
CREATE INDEX idx_usuario_nombre ON usuario(nombre);
CREATE INDEX idx_usuario_email ON usuario(email);
CREATE INDEX idx_laboratorio_nombre ON laboratorio(nombre);

-- Índices en tabla principal obra
CREATE INDEX idx_obra_titulo ON obra(titulo);
CREATE INDEX idx_obra_autor ON obra(nombre_autor, autor_firma);
CREATE INDEX idx_obra_anio ON obra(anio);
CREATE INDEX idx_obra_tipo_publicacion ON obra(tipo_publicacion);
CREATE INDEX idx_obra_tema ON obra(tema_principal);
CREATE INDEX idx_obra_fecha ON obra(fecha);
CREATE INDEX idx_obra_enlace ON obra(enlace);
CREATE INDEX idx_obra_creacion ON obra(fecha_creacion);

-- Índices en proyectos
CREATE INDEX idx_proyectos_usuario ON proyectos(usuario_id);
CREATE INDEX idx_proyectos_laboratorio ON proyectos(laboratorio_id);
CREATE INDEX idx_proyectos_nombre ON proyectos(nombre);

-- Índices en tablas asociativas
CREATE INDEX idx_obra_lugar_lugar ON obra_lugar(id_lugar);
CREATE INDEX idx_obra_personajes_personaje ON obra_personajes(id_personaje);
CREATE INDEX idx_proyecto_obra_obra ON proyecto_obra(id_obra);

-- Índices compuestos para búsquedas comunes
CREATE INDEX idx_obra_autor_anio ON obra(nombre_autor, anio);
CREATE INDEX idx_obra_tipo_fecha ON obra(tipo_publicacion, fecha);

-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

CREATE VIEW v_obras_por_proyecto AS
SELECT 
    p.id_proyecto,
    p.nombre AS proyecto,
    COUNT(po.id_obra) AS total_obras,
    MIN(o.fecha) AS fecha_mas_antigua,
    MAX(o.fecha) AS fecha_mas_reciente
FROM proyectos p
LEFT JOIN proyecto_obra po ON p.id_proyecto = po.id_proyecto
LEFT JOIN obra o ON po.id_obra = o.id_obra
GROUP BY p.id_proyecto, p.nombre;

CREATE VIEW v_obras_por_autor AS
SELECT 
    nombre_autor,
    COUNT(*) AS total_obras,
    COUNT(DISTINCT tipo_publicacion) AS tipos_publicacion,
    MIN(anio) AS primer_obra,
    MAX(anio) AS ultima_obra
FROM obra
WHERE nombre_autor IS NOT NULL
GROUP BY nombre_autor
ORDER BY total_obras DESC;

CREATE VIEW v_obras_por_tipo AS
SELECT 
    tipo_publicacion,
    COUNT(*) AS total,
    COUNT(DISTINCT nombre_autor) AS autores_unicos,
    AVG(anio) AS anio_promedio
FROM obra
GROUP BY tipo_publicacion
ORDER BY total DESC;

CREATE VIEW v_periodicos_completos AS
SELECT 
    o.id_obra,
    o.titulo,
    o.num_periodico,
    o.fecha,
    o.nombre_autor,
    p.modalidad_periodico,
    p.fragmento_donde_aparece
FROM obra o
LEFT JOIN periodico p ON o.id_obra = p.id_obra
WHERE o.tipo_publicacion = 'periódico';

-- ============================================================
-- FUNCIONES PARA MANTENIMIENTO
-- ============================================================

CREATE OR REPLACE FUNCTION actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para actualizar timestamp
CREATE TRIGGER trigger_usuario_actualizado
BEFORE UPDATE ON usuario
FOR EACH ROW
EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trigger_proyectos_actualizado
BEFORE UPDATE ON proyectos
FOR EACH ROW
EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER trigger_obra_actualizado
BEFORE UPDATE ON obra
FOR EACH ROW
EXECUTE FUNCTION actualizar_timestamp();
