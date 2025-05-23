#!/bin/bash

# LLB Docker Utility Script
# This script provides convenient commands for managing the LLB Docker environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "docker-compose is not installed. Please install it and try again."
        exit 1
    fi
}

# Function to build all images
build_all() {
    print_status "Building all Docker images..."
    docker-compose build --no-cache
    print_success "All images built successfully!"
}

# Function to start development environment
start_dev() {
    print_status "Starting development environment..."
    docker-compose -f docker-compose.dev.yml up -d
    print_success "Development environment started!"
    print_status "Services available at:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8001"
    echo "  - Database: localhost:5433"
    echo "  - Redis: localhost:6380"
}

# Function to start production environment
start_prod() {
    print_status "Starting production environment..."
    docker-compose up -d
    print_success "Production environment started!"
    print_status "Application available at: http://localhost"
}

# Function to stop all services
stop_all() {
    print_status "Stopping all services..."
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
    print_success "All services stopped!"
}

# Function to view logs
logs() {
    local service=$1
    if [ -z "$service" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $service..."
        docker-compose logs -f "$service"
    fi
}

# Function to run database migrations
migrate() {
    print_status "Running database migrations..."
    docker-compose exec backend alembic upgrade head
    print_success "Database migrations completed!"
}

# Function to create a new migration
create_migration() {
    local message=$1
    if [ -z "$message" ]; then
        print_error "Please provide a migration message"
        echo "Usage: $0 create-migration \"migration message\""
        exit 1
    fi
    
    print_status "Creating new migration: $message"
    docker-compose exec backend alembic revision --autogenerate -m "$message"
    print_success "Migration created successfully!"
}

# Function to run tests
test() {
    local service=$1
    case $service in
        backend)
            print_status "Running backend tests..."
            docker-compose exec backend pytest
            ;;
        frontend)
            print_status "Running frontend tests..."
            docker-compose exec frontend npm test -- --coverage --watchAll=false
            ;;
        *)
            print_status "Running all tests..."
            docker-compose exec backend pytest
            docker-compose exec frontend npm test -- --coverage --watchAll=false
            ;;
    esac
    print_success "Tests completed!"
}

# Function to clean up Docker resources
cleanup() {
    print_warning "This will remove all stopped containers, unused networks, and dangling images."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker resources..."
        docker system prune -f
        print_success "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to reset everything
reset() {
    print_warning "This will stop all services and remove all volumes (data will be lost)."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Resetting environment..."
        docker-compose down -v
        docker-compose -f docker-compose.dev.yml down -v
        docker system prune -f
        print_success "Environment reset completed!"
    else
        print_status "Reset cancelled."
    fi
}

# Function to show status
status() {
    print_status "Docker container status:"
    docker-compose ps
    echo
    print_status "Docker images:"
    docker images | grep llb
}

# Function to enter a container shell
shell() {
    local service=$1
    if [ -z "$service" ]; then
        print_error "Please specify a service (backend, frontend, db, redis)"
        exit 1
    fi
    
    print_status "Opening shell in $service container..."
    case $service in
        backend)
            docker-compose exec backend bash
            ;;
        frontend)
            docker-compose exec frontend sh
            ;;
        db)
            docker-compose exec db psql -U llb_user -d llb_db
            ;;
        redis)
            docker-compose exec redis redis-cli
            ;;
        *)
            docker-compose exec "$service" sh
            ;;
    esac
}

# Function to show help
show_help() {
    echo "LLB Docker Utility Script"
    echo
    echo "Usage: $0 [command] [options]"
    echo
    echo "Commands:"
    echo "  build           Build all Docker images"
    echo "  start-dev       Start development environment"
    echo "  start-prod      Start production environment"
    echo "  stop            Stop all services"
    echo "  logs [service]  Show logs (optionally for specific service)"
    echo "  migrate         Run database migrations"
    echo "  create-migration \"message\"  Create new migration"
    echo "  test [service]  Run tests (backend, frontend, or all)"
    echo "  status          Show container and image status"
    echo "  shell <service> Open shell in container (backend, frontend, db, redis)"
    echo "  cleanup         Clean up Docker resources"
    echo "  reset           Reset entire environment (removes volumes)"
    echo "  help            Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start-dev"
    echo "  $0 logs backend"
    echo "  $0 test backend"
    echo "  $0 shell backend"
    echo "  $0 create-migration \"Add user preferences table\""
}

# Main script logic
main() {
    check_docker
    check_docker_compose
    
    case $1 in
        build)
            build_all
            ;;
        start-dev)
            start_dev
            ;;
        start-prod)
            start_prod
            ;;
        stop)
            stop_all
            ;;
        logs)
            logs "$2"
            ;;
        migrate)
            migrate
            ;;
        create-migration)
            create_migration "$2"
            ;;
        test)
            test "$2"
            ;;
        status)
            status
            ;;
        shell)
            shell "$2"
            ;;
        cleanup)
            cleanup
            ;;
        reset)
            reset
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 