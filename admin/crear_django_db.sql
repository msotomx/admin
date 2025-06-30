-- correrlo desde la terminal (bash): mysql -u root -p < crear_django_db.sql
-- admin_user: cámbialo por un nombre personalizado si manejas múltiples apps.
-- TuPasswordSegura2024!: usa una contraseña fuerte (16+ caracteres, mayúsculas, símbolos).
-- localhost: %   Si tu app se conecta desde otro servidor (p. ej., Gunicorn vía Unix socket o externo), usa % o IP específica:
-- (sql) CREATE USER 'admin_user'@'%' IDENTIFIED BY '...';


-- 🔧 Crear la base de datos
CREATE DATABASE IF NOT EXISTS db_admin
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 👤 Crear el usuario (ajusta contraseña)
CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'TuPasswordSegura2024!';

-- 🛡️ Otorgar permisos solo sobre la base db_admin
GRANT SELECT, INSERT, UPDATE, DELETE,
CREATE, DROP, INDEX, ALTER, REFERENCES,
LOCK TABLES, EXECUTE
ON db_admin.*
TO 'admin_user'@'localhost';

-- ✅ Aplicar cambios
FLUSH PRIVILEGES;
