#!/bin/sh

set -e  # Salir si hay un error

echo "Esperando a que la base de datos esté disponible..."
until pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER; do
  sleep 1
done

echo "Aplicando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando el servidor..."
exec "$@"  # Esto permite pasar el comando final desde docker-compose
