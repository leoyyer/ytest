#!/bin/bash

# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all unused images
docker image prune -a -f

# Remove all unused volumes
docker volume prune -f

# Remove all unused networks
docker network prune -f

# Remove all unused data
docker system prune -a --volumes -f

# Optionally clear Docker local config and cache files
rm -rf ~/Library/Containers/com.docker.docker
rm -rf ~/.docker

echo "Docker cleanup completed."
