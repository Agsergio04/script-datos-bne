#!/bin/bash

# Script de utilidades para el proyecto BNE
# Proporciona comandos comunes para desarrollo y deployment

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funciones auxiliares
print_header() {
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}========================================${NC}\n"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Comandos disponibles
help() {
    cat << EOF
BNE Project - Utilidades

Uso: ./utils.sh [comando]

Comandos disponibles:
  help              - Mostrar este mensaje
  start             - Iniciar todos los servicios
  stop              - Detener todos los servicios
  restart           - Reiniciar todos los servicios
  logs              - Ver logs en tiempo real
  logs-backend      - Ver logs del backend
  logs-db           - Ver logs de la BD
  status            - Ver estado de los servicios
  clean             - Limpiar volúmenes (PERDERÁ DATOS)
  backup            - Crear backup de la BD
  restore <file>    - Restaurar backup de la BD
  db-shell          - Acceder a la BD por terminal
  backend-shell     - Acceder a shell del backend
  seed              - Reiniciar BD con datos de ejemplo
  test              - Ejecutar tests del backend
  lint              - Ejecutar linter

Ejemplos:
  ./utils.sh start
  ./utils.sh logs-backend
  ./utils.sh backup
EOF
}

start() {
    print_header "Iniciando servicios BNE..."
    docker-compose up -d
    print_success "Servicios iniciados"
    echo -e "\nAcceso a los servicios:"
    echo -e "  Frontend:    ${YELLOW}http://localhost:3000${NC}"
    echo -e "  Backend:     ${YELLOW}http://localhost:5000${NC}"
    echo -e "  pgAdmin:     ${YELLOW}http://localhost:5050${NC}"
    echo -e "  BD:          ${YELLOW}localhost:5432${NC}\n"
}

stop() {
    print_header "Deteniendo servicios..."
    docker-compose down
    print_success "Servicios detenidos"
}

restart() {
    print_header "Reiniciando servicios..."
    docker-compose restart
    print_success "Servicios reiniciados"
}

logs() {
    docker-compose logs -f
}

logs_backend() {
    docker-compose logs -f backend
}

logs_db() {
    docker-compose logs -f db
}

status() {
    print_header "Estado de los servicios"
    docker-compose ps
}

clean() {
    print_warning "Esto eliminará TODOS los volúmenes y PERDERÁ todos los datos"
    read -p "¿Continuar? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_header "Limpiando volúmenes..."
        docker-compose down -v
        print_success "Limpieza completada"
    else
        print_warning "Operación cancelada"
    fi
}

backup() {
    print_header "Creando backup de la BD..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="backup_bne_${TIMESTAMP}.sql"
    
    docker exec bne_database pg_dump -U bne_user -d bne_db > "$BACKUP_FILE"
    print_success "Backup creado: $BACKUP_FILE"
}

restore() {
    if [ -z "$1" ]; then
        print_error "Debe especificar archivo de backup"
        echo "Uso: ./utils.sh restore <archivo.sql>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Archivo no encontrado: $1"
        exit 1
    fi
    
    print_warning "Esto sobrescribirá la BD actual"
    read -p "¿Continuar? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_header "Restaurando backup..."
        cat "$1" | docker exec -i bne_database psql -U bne_user -d bne_db
        print_success "Backup restaurado desde: $1"
    else
        print_warning "Operación cancelada"
    fi
}

db_shell() {
    print_header "Accediendo a BD PostgreSQL..."
    docker exec -it bne_database psql -U bne_user -d bne_db
}

backend_shell() {
    print_header "Accediendo a shell del backend..."
    docker exec -it bne_backend bash
}

seed() {
    print_header "Reiniciando BD con datos de ejemplo..."
    docker-compose down -v
    docker-compose up -d db
    
    # Esperar a que BD esté lista
    sleep 5
    
    # Ejecutar migraciones y seeders
    docker exec bne_database psql -U bne_user -d bne_db < bd/schema_optimized.sql
    docker exec bne_database psql -U bne_user -d bne_db < bd/seeders/seed_data.sql
    
    print_success "BD reiniciada con datos de ejemplo"
}

test() {
    print_header "Ejecutando tests..."
    docker exec bne_backend pytest -v
}

lint() {
    print_header "Ejecutando linter..."
    docker exec bne_backend flake8 . --max-line-length=120 --exclude=venv
}

# Procesar comando
case "${1:-help}" in
    help)
        help
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    logs-backend)
        logs_backend
        ;;
    logs-db)
        logs_db
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    backup)
        backup
        ;;
    restore)
        restore "$2"
        ;;
    db-shell)
        db_shell
        ;;
    backend-shell)
        backend_shell
        ;;
    seed)
        seed
        ;;
    test)
        test
        ;;
    lint)
        lint
        ;;
    *)
        print_error "Comando desconocido: $1"
        echo "Usa './utils.sh help' para ver los comandos disponibles"
        exit 1
        ;;
esac
