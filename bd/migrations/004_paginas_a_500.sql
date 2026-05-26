-- Migración 004: ampliar obra.paginas de VARCHAR(50) a VARCHAR(500)
-- El modelo SQLAlchemy ya declaraba String(500); este campo puede contener
-- la descripción física completa de la obra (p. ej. "324 p. ; 21 cm").

ALTER TABLE obra ALTER COLUMN paginas TYPE VARCHAR(500);
