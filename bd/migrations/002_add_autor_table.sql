-- Migración 002: Añadir tabla autor y FK en obra
-- Ejecutar sobre una BD existente que ya tiene el schema inicial

-- ============================================================
-- TABLA AUTOR (estructura de datos.bne.es para personas)
-- ============================================================

CREATE TABLE IF NOT EXISTS autor (
    id_autor BIGSERIAL PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    nombre_firma VARCHAR(255),
    pseudonimos TEXT,
    -- Fechas como texto: BNE usa fechas aproximadas como "ca. 1500" o "fl. 1600-1650"
    fecha_nacimiento VARCHAR(100),
    anio_nacimiento INT CHECK (anio_nacimiento > 0 AND anio_nacimiento <= 2100),
    lugar_nacimiento VARCHAR(255),
    fecha_muerte VARCHAR(100),
    anio_muerte INT CHECK (anio_muerte > 0 AND anio_muerte <= 2100),
    lugar_muerte VARCHAR(255),
    nacionalidad VARCHAR(100),
    ocupacion VARCHAR(255),
    genero VARCHAR(50),
    lengua VARCHAR(100),
    biografia TEXT,
    bne_identificador VARCHAR(100) UNIQUE,
    url_datos_bne TEXT,
    viaf_id VARCHAR(100),
    otros_identificadores TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_nombre_autor_no_vacio CHECK (nombre_completo != '')
);

-- ============================================================
-- FK EN OBRA → AUTOR (nullable para compatibilidad con datos existentes)
-- ============================================================

ALTER TABLE obra
    ADD COLUMN IF NOT EXISTS id_autor BIGINT,
    ADD CONSTRAINT fk_obra_autor
        FOREIGN KEY (id_autor) REFERENCES autor(id_autor)
        ON UPDATE CASCADE ON DELETE SET NULL;

-- ============================================================
-- ÍNDICES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_autor_nombre ON autor(nombre_completo);
CREATE INDEX IF NOT EXISTS idx_autor_bne_id ON autor(bne_identificador);
CREATE INDEX IF NOT EXISTS idx_autor_anio_nacimiento ON autor(anio_nacimiento);
CREATE INDEX IF NOT EXISTS idx_autor_nacionalidad ON autor(nacionalidad);
CREATE INDEX IF NOT EXISTS idx_obra_id_autor ON obra(id_autor);

-- ============================================================
-- VISTA AUTORES CON OBRAS
-- ============================================================

CREATE OR REPLACE VIEW v_autores_con_obras AS
SELECT
    a.id_autor,
    a.nombre_completo,
    a.nombre_firma,
    a.anio_nacimiento,
    a.anio_muerte,
    a.nacionalidad,
    a.ocupacion,
    a.bne_identificador,
    COUNT(o.id_obra) AS total_obras,
    COUNT(DISTINCT o.tipo_publicacion) AS tipos_publicacion,
    MIN(o.anio) AS primera_obra,
    MAX(o.anio) AS ultima_obra
FROM autor a
LEFT JOIN obra o ON a.id_autor = o.id_autor
GROUP BY a.id_autor, a.nombre_completo, a.nombre_firma, a.anio_nacimiento,
         a.anio_muerte, a.nacionalidad, a.ocupacion, a.bne_identificador
ORDER BY total_obras DESC;

-- ============================================================
-- TRIGGER actualizar_timestamp PARA AUTOR
-- ============================================================

CREATE TRIGGER trigger_autor_actualizado
BEFORE UPDATE ON autor
FOR EACH ROW
EXECUTE FUNCTION actualizar_timestamp();
