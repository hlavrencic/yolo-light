#!/bin/bash
# Quick Start Script para YOLO Light API
# Uso: bash quick_start.sh [comando]

set -e

CONTAINER_NAME="yolo-api"
IMAGE_NAME="yolo-light:latest"
API_URL="http://localhost:8000"

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

case "${1:-help}" in

    build)
        print_header "Building Docker Image"
        docker build -t $IMAGE_NAME .
        print_success "Docker image built: $IMAGE_NAME"
        ;;

    run)
        print_header "Starting API Container"
        
        # Stop existing container if running
        if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            print_info "Stopping existing container..."
            docker stop $CONTAINER_NAME 2>/dev/null || true
            docker rm $CONTAINER_NAME 2>/dev/null || true
        fi
        
        docker run -d \
            -p 8000:8000 \
            --name $CONTAINER_NAME \
            $IMAGE_NAME
        
        print_success "Container started: $CONTAINER_NAME"
        print_info "Wait 2-3 seconds for startup..."
        sleep 2
        
        # Check health
        if curl -s $API_URL/health > /dev/null; then
            print_success "API is responding on $API_URL"
        else
            print_error "API not responding yet. Check logs: docker logs $CONTAINER_NAME"
        fi
        ;;

    stop)
        print_header "Stopping API Container"
        if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            docker stop $CONTAINER_NAME
            docker rm $CONTAINER_NAME
            print_success "Container stopped and removed"
        else
            print_info "Container not running"
        fi
        ;;

    logs)
        print_header "Container Logs"
        docker logs -f $CONTAINER_NAME
        ;;

    test)
        print_header "Running Test Suite"
        if command -v python3 &> /dev/null; then
            python3 test_api_complete.py
        else
            print_error "Python3 not found. Install it or use: wsl python3 test_api_complete.py"
        fi
        ;;

    health)
        print_header "API Health Check"
        response=$(curl -s $API_URL/health)
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
        ;;

    detect)
        print_header "Testing Object Detection"
        
        image="${2:-testing/foto.jpg}"
        
        if [ ! -f "$image" ]; then
            print_error "Image file not found: $image"
            echo "Usage: bash quick_start.sh detect [image_path]"
            exit 1
        fi
        
        print_info "Detecting objects in: $image"
        curl -s -X POST -F "file=@$image" $API_URL/detect | python3 -m json.tool
        ;;

    rebuild)
        print_header "Rebuilding Everything"
        bash $0 stop
        bash $0 build
        bash $0 run
        bash $0 health
        ;;

    restart)
        print_header "Restarting API"
        bash $0 stop
        bash $0 run
        bash $0 health
        ;;

    stats)
        print_header "Container Statistics"
        docker stats --no-stream $CONTAINER_NAME
        ;;

    shell)
        print_header "Entering Container Shell"
        docker exec -it $CONTAINER_NAME bash
        ;;

    clean)
        print_header "Cleanup"
        bash $0 stop
        if [ "$2" = "--all" ]; then
            print_info "Removing image: $IMAGE_NAME"
            docker rmi $IMAGE_NAME 2>/dev/null || true
            print_success "Cleanup complete"
        fi
        ;;

    *)
        cat << EOF

${GREEN}YOLO Light API - Quick Start${NC}

Usage: bash quick_start.sh [command]

${GREEN}Commands:${NC}

  build      - Build Docker image
  run        - Start API container
  stop       - Stop and remove container
  restart    - Restart container
  rebuild    - Build, stop, and run
  
  logs       - Show container logs (live)
  stats      - Show container statistics
  shell      - Enter container shell
  
  health     - Check API health
  detect     - Test object detection with image
               Usage: bash quick_start.sh detect [image_path]
               Default: testing/foto.jpg
  
  test       - Run complete test suite
  
  clean      - Stop container and cleanup
             Add --all flag to also remove image:
             bash quick_start.sh clean --all

${GREEN}Examples:${NC}

  # Quick setup
  bash quick_start.sh rebuild
  bash quick_start.sh health

  # Test with custom image
  bash quick_start.sh detect testing/habitacion.jpg

  # Run tests
  bash quick_start.sh test

  # Check performance
  bash quick_start.sh stats

${GREEN}API Endpoints:${NC}

  GET  $API_URL/health        - Health check
  GET  $API_URL/              - API info
  POST $API_URL/detect        - Detect objects

${GREEN}Documentation:${NC}

  README.md               - Main guide
  DEPLOYMENT_RPI4.md      - RPi4 setup
  DEVELOPMENT_STATUS.md   - Current status

EOF
        ;;
esac
