-- Este archivo se ejecuta automáticamente al crear los contenedores
-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear esquemas para organizar mejor las tablas
CREATE SCHEMA IF NOT EXISTS commands;
CREATE SCHEMA IF NOT EXISTS queries;

-- Dar permisos al usuario postgres
GRANT ALL PRIVILEGES ON SCHEMA commands TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA queries TO postgres;