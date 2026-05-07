-- seed_data.sql - Datos de ejemplo para desarrollo
-- Esta archivo será ejecutado automáticamente por Docker durante la inicialización

-- Desactivar restricciones temporalmente
SET CONSTRAINTS ALL DEFERRED;

-- ============================================================
-- INSERTANDO DATOS DE PRUEBA
-- ============================================================

-- Usuarios
INSERT INTO usuario (nombre, email) VALUES
    ('Dr. Juan García López', 'juan.garcia@ejemplo.es'),
    ('Dra. María Rodríguez Martín', 'maria.rodriguez@ejemplo.es'),
    ('Prof. Carlos Sánchez Pérez', 'carlos.sanchez@ejemplo.es')
ON CONFLICT (email) DO NOTHING;

-- Laboratorios
INSERT INTO laboratorio (nombre, descripcion) VALUES
    ('Laboratorio de Análisis Literario', 'Análisis y clasificación de obras literarias españolas'),
    ('Laboratorio de Digitalización', 'Digitalización de periódicos históricos'),
    ('Laboratorio de Consultoría Bibliográfica', 'Consultoría y referencias bibliográficas')
ON CONFLICT (nombre) DO NOTHING;

-- Lugares
INSERT INTO lugar (nombre, lugar_principal, lugar_secundario) VALUES
    ('Madrid', true, false),
    ('Barcelona', true, false),
    ('Sevilla', true, false),
    ('Valencia', false, true),
    ('Bilbao', false, true),
    ('Andalucía', false, false),
    ('Castilla y León', false, false),
    ('Cataluña', false, false);

-- Personajes
INSERT INTO personajes (personaje_principal, personaje_secundario) VALUES
    ('Don Quijote de la Mancha', NULL),
    ('Sancho Panza', NULL),
    (NULL, 'Dulcinea del Toboso'),
    ('Madame Bovary', NULL),
    (NULL, 'Capitán Ahab'),
    ('Elizabeth Bennet', NULL);

-- Proyectos
INSERT INTO proyectos (nombre, descripcion, cita, usuario_id, laboratorio_id)
SELECT 
    p_nombre,
    p_descripcion,
    p_cita,
    (SELECT id_usuario FROM usuario LIMIT 1),
    l.id_laboratorio
FROM (VALUES
    ('Canonización del Teatro Español (1850-1950)', 
     'Estudio de la evolución del teatro español en el siglo XIX y primera mitad del XX',
     'García, J. (2024). Canonización del Teatro Español. Editorial BNE.',
     (SELECT id_laboratorio FROM laboratorio WHERE nombre = 'Laboratorio de Análisis Literario')),
    ('Análisis de Periódicos Españoles (1900-1950)',
     'Recopilación y análisis de contenido de periódicos españoles del primer cuarto del siglo XX',
     'Rodríguez, M. (2024). Periódicos españoles. Editorial Universidad.',
     (SELECT id_laboratorio FROM laboratorio WHERE nombre = 'Laboratorio de Digitalización'))
) AS p_temp(p_nombre, p_descripcion, p_cita, l_id)
JOIN laboratorio l ON l.id_laboratorio = p_temp.l_id;

-- Obras - Novelas
INSERT INTO obra (titulo, tipo_publicacion, autor_firma, nombre_autor, anio, fecha, 
                  dia, mes, tema_principal, paginas, como_citar, fecha_creacion)
VALUES
    ('El Quijote', 'Novela', 'Cervantes', 'Miguel de Cervantes Saavedra', 1605, '1605-01-16', 16, 1,
     'Aventuras caballerescas', '620', 'Cervantes, M. (1605). El Quijote. Imprenta de Juan de la Cuesta.', CURRENT_TIMESTAMP),
    ('La Regenta', 'Novela', 'Clarín', 'Leopoldo Alas y Ureña', 1884, '1884-03-15', 15, 3,
     'Sociedad española provincial', '600', 'Clarín. (1884). La Regenta. Editorial Maucci.', CURRENT_TIMESTAMP),
    ('Ángeles y Demonios', 'Novela', 'D.A. Brown', 'Robert Langdon', 2000, '2000-05-01', 1, 5,
     'Misterio y aventura', '450', 'Brown, D.A. (2000). Ángeles y Demonios. Planeta.', CURRENT_TIMESTAMP),
    ('Soldados de Salamina', 'Novela', 'Cercas', 'Javier Cercas', 2001, '2001-09-01', 1, 9,
     'Guerra civil española', '380', 'Cercas, J. (2001). Soldados de Salamina. Tusquets.', CURRENT_TIMESTAMP);

-- Obras - Periódicos
INSERT INTO obra (titulo, tipo_publicacion, autor_firma, nombre_autor, anio, fecha,
                  dia, mes, num_periodico, tema_principal, como_citar, fecha_creacion)
VALUES
    ('ABC', 'Periódico', 'Varias Secciones', 'ABC', 1905, '1905-01-01', 1, 1,
     '1', 'Información general', 'ABC. (1905, enero). Sección de noticias.', CURRENT_TIMESTAMP),
    ('La Vanguardia', 'Periódico', 'Redacción', 'La Vanguardia', 1920, '1920-06-15', 15, 6,
     '2847', 'Información regional', 'La Vanguardia. (1920, junio).', CURRENT_TIMESTAMP),
    ('El Mundo', 'Periódico', 'Crítica Literaria', 'El Mundo', 1950, '1950-12-25', 25, 12,
     '15002', 'Crítica cultural', 'El Mundo. (1950, diciembre).', CURRENT_TIMESTAMP);

-- Obras - Poesía
INSERT INTO obra (titulo, tipo_publicacion, autor_firma, nombre_autor, anio, fecha,
                  dia, mes, tema_principal, paginas, como_citar, fecha_creacion)
VALUES
    ('Rimas y Leyendas', 'Poesía', 'Bécquer', 'Gustavo Adolfo Bécquer', 1871, '1871-11-01', 1, 11,
     'Amor, melancolía, misterio', '280', 'Bécquer, G.A. (1871). Rimas y Leyendas. Editorial Fortanet.', CURRENT_TIMESTAMP),
    ('Modernismo', 'Poesía', 'Machado', 'Antonio Machado', 1899, '1899-06-01', 1, 6,
     'Modernismo español', '156', 'Machado, A. (1899). Modernismo. Tipografía Católica.', CURRENT_TIMESTAMP),
    ('Espantajo', 'Poesía', 'Lorca', 'Federico García Lorca', 1928, '1928-09-01', 1, 9,
     'Vanguardia, surrealismo', '78', 'García Lorca, F. (1928). Espantajo.', CURRENT_TIMESTAMP);

-- Obras - Teatro
INSERT INTO obra (titulo, tipo_publicacion, autor_firma, nombre_autor, anio, fecha,
                  dia, mes, tema_principal, paginas, como_citar, fecha_creacion)
VALUES
    ('La vida es sueño', 'Teatro', 'Calderón', 'Pedro Calderón de la Barca', 1636, '1636-01-01', 1, 1,
     'Existencialismo, libertad', '250', 'Calderón, P. (1636). La vida es sueño. Editorial Crítica.', CURRENT_TIMESTAMP),
    ('Bodas de sangre', 'Teatro', 'Lorca', 'Federico García Lorca', 1933, '1933-03-08', 8, 3,
     'Drama rural español', '180', 'García Lorca, F. (1933). Bodas de sangre. Editorial Losada.', CURRENT_TIMESTAMP);

-- Asociar obras con lugares
INSERT INTO obra_lugar (id_obra, id_lugar)
SELECT o.id_obra, l.id_lugar
FROM obra o
JOIN lugar l ON (o.titulo LIKE '%Quijote%' AND l.nombre = 'Castilla y León')
   OR (o.titulo LIKE '%Regenta%' AND l.nombre = 'Oviedo')
   OR (o.titulo LIKE '%Salamina%' AND l.nombre = 'Castilla y León')
LIMIT 10;

-- Asociar obras con personajes
INSERT INTO obra_personajes (id_obra, id_personaje)
SELECT o.id_obra, p.id_personaje
FROM obra o
JOIN personajes p ON (o.titulo = 'El Quijote' AND (p.personaje_principal = 'Don Quijote de la Mancha' 
                                                   OR p.personaje_principal = 'Sancho Panza'))
                  OR (o.titulo = 'Bodas de sangre' AND p.id_personaje IN (1, 2))
LIMIT 10;

-- Insertar tipos de obras (teatro, novela, etc.)
INSERT INTO teatro (id_obra, resumen, modalidad_teatro)
SELECT id_obra, 
        'Drama filosófico que cuestiona la naturaleza de la realidad y el libre albedrío',
        'Drama filosófico'
FROM obra WHERE titulo = 'La vida es sueño'
ON CONFLICT (id_obra) DO NOTHING;

INSERT INTO teatro (id_obra, resumen, modalidad_teatro)
SELECT id_obra,
        'Tragedia rural con elementos simbólicos sobre el destino y el honor',
        'Tragedia rural'
FROM obra WHERE titulo = 'Bodas de sangre'
ON CONFLICT (id_obra) DO NOTHING;

INSERT INTO novela (id_obra, modalidad_novela, tipo_de_ubicacion)
SELECT id_obra,
        'Novela satírica',
        'Rural/Manchego'
FROM obra WHERE titulo = 'El Quijote'
ON CONFLICT (id_obra) DO NOTHING;

INSERT INTO novela (id_obra, modalidad_novela, tipo_de_ubicacion)
SELECT id_obra,
        'Novela realista-naturalista',
        'Urbano/Provincial'
FROM obra WHERE titulo = 'La Regenta'
ON CONFLICT (id_obra) DO NOTHING;

INSERT INTO periodico (id_obra, modalidad_periodico)
SELECT id_obra, 'Periódico de información general'
FROM obra WHERE tipo_publicacion = 'Periódico'
ON CONFLICT (id_obra) DO NOTHING;

INSERT INTO poesia (id_obra, resumen, modalidad_poesia)
SELECT id_obra, 'Colección de baladas y leyendas con temática romántica',
        'Baladas y leyendas'
FROM obra WHERE titulo = 'Rimas y Leyendas'
ON CONFLICT (id_obra) DO NOTHING;

-- Asociar obras a proyectos
INSERT INTO proyecto_obra (id_proyecto, id_obra)
SELECT (SELECT MIN(id_proyecto) FROM proyectos), id_obra
FROM obra
WHERE titulo IN ('El Quijote', 'La Regenta', 'La vida es sueño', 'Bodas de sangre')
ON CONFLICT DO NOTHING;

INSERT INTO proyecto_obra (id_proyecto, id_obra)
SELECT (SELECT MAX(id_proyecto) FROM proyectos), id_obra
FROM obra
WHERE tipo_publicacion = 'Periódico'
ON CONFLICT DO NOTHING;

-- ============================================================
-- VERIFICACIÓN DE DATOS INSERTADOS
-- ============================================================

SELECT COUNT(*) as total_usuarios FROM usuario;
SELECT COUNT(*) as total_laboratorios FROM laboratorio;
SELECT COUNT(*) as total_proyectos FROM proyectos;
SELECT COUNT(*) as total_obras FROM obra;
SELECT COUNT(*) as total_lugares FROM lugar;
SELECT COUNT(*) as total_personajes FROM personajes;

SET CONSTRAINTS ALL IMMEDIATE;
