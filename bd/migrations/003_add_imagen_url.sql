-- Migración 003: Añadir columna imagen_url a obra y autor
-- Almacena la URL de la imagen relacionada (portada/digitalización en obra,
-- retrato en autor) extraída de datos.bne.es para previsualización.

ALTER TABLE obra  ADD COLUMN IF NOT EXISTS imagen_url TEXT;
ALTER TABLE autor ADD COLUMN IF NOT EXISTS imagen_url TEXT;
