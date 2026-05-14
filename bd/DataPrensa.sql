-- Esquema base para PostgreSQL 18
-- Ajusta nombres/campos si tu diagrama tiene más atributos visibles.

CREATE TABLE usuario (
    id_usuario BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL
);

CREATE TABLE laboratorio (
    id_laboratorio BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL
);

CREATE TABLE proyectos (
    id_proyecto BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cita TEXT,
    usuario_id BIGINT,
    laboratorio_id BIGINT,
    CONSTRAINT fk_proyectos_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_proyectos_laboratorio
        FOREIGN KEY (laboratorio_id) REFERENCES laboratorio(id_laboratorio)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE obra (
    id_obra BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(500) NOT NULL,
    tipo_publicacion VARCHAR(100),
    autor_firma VARCHAR(255),
    nombre_autor VARCHAR(255),
    anio INT,
    enlace TEXT,
    fecha DATE,
    dia INT,
    mes INT,
    num_periodico VARCHAR(100),
    variante_titulo VARCHAR(255),
    pseudonimos_autor VARCHAR(255),
    tema_principal VARCHAR(255),
    paginas VARCHAR(500),
    imprenta VARCHAR(255),
    como_citar TEXT,
    lugar_impresion VARCHAR(255)
);

CREATE TABLE lugar (
    id_lugar BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    lugar_principal BOOLEAN DEFAULT FALSE,
    lugar_secundario BOOLEAN DEFAULT FALSE
);

CREATE TABLE personajes (
    id_personaje BIGSERIAL PRIMARY KEY,
    personaje_principal VARCHAR(255),
    personaje_secundario VARCHAR(255)
);

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

CREATE TABLE periodoico (
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

-- Relaciones M:N o asociativas típicas
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
    fecha_insercion TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id_proyecto, id_obra),
    CONSTRAINT fk_proyecto_obra_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_proyecto_obra_obra
        FOREIGN KEY (id_obra) REFERENCES obra(id_obra)
        ON UPDATE CASCADE ON DELETE CASCADE
);