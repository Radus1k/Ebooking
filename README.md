# Ebooking


Simple Ebooking website using Django for backend & frontend, dockerized

## Technology stack  
- **Deployment**: Docker Compose v2.12.2 (Docker Engine - Community v20.10.21)
- **Backend**: Django 4.1.5 (Python 3.11)
- **Async tasks**: Celery 5.2.3 (dawn-chorus)
- **Message broker**: Redis 5.0.7
- **Frontend**: Django templates
- **Styling**: Bootstrap4, Django Crispy Forms

## Setting up OS Requirements
1. Follow instructions at [Install Docker Engine on Ubuntu (Install using the repository)](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).  
⚠️ Check your Docker Compose version by running `docker compose version`. Expected output: `Docker Compose version v2.6.0`.

2. Follow instructions at [Post-installation steps for Linux (Manage Docker as a non-root user)](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) in order to be able to run Docker without `root` privileges. Afterwards, run these two commands 
```
 sudo systemctl enable docker.service
 sudo systemctl enable containerd.service
```
in order to ensure the Docker service starts on boot.

## _Development_ environment

Commands to [+create+] / [-destroy-] the **development** environment: 
```
 # Build images from .yml file & start containers (services) 🔼
 docker compose -f ./docker-compose.dev.yml up -d --build  
```
   
```
 # Stop & delete containers (services) 🔽
 docker compose -f ./docker-compose.dev.yml down
```
Commands to [+start+] / [-stop-] the **development** environment:
```
 # Start containers (services) ✅, after they have been stopped using the 'stop' command 
 docker compose -f ./docker-compose.dev.yml start  
```
   
```
 # Stop containers (services) ❎, WITHOUT deleting them 
 docker compose -f ./docker-compose.dev.yml stop
```
Use `stop` when leaving for the day.  
Use `start` when you start working.  
Use `up -d --build` only when the `docker-compose.dev.yml` file is changed.

#### **Services**

- [+django+]: Responsible for running the development webserver at `0.0.0.0:8000`. Autoreload functionality on code change is also functional,  
- [+db_postgres+]: PostgreSQL database server. Used here in order to more closely resemble the prod environment,  
- [+db_pgadmin+]: Web management interface for PostgreSQL db servers. Only accepts outside traffic from `127.0.0.1` on port `8001`,
- [+celery_beat+] & [+celery_worker+]: Responsible for scheduling periodic tasks (e.g., DB backup) and executing asynchronous tasks (e.g., e-mail notifications), respectively,
- [+redis+]: A message broker which allows Celery Beat, Celery Worker & Django to work together in order to execute periodic & async tasks.
```

## **Extra** commands
Force build images & start containers for an environment: 
```
 docker compose -f ./docker-compose.[dev|prod].yml up -d --build --remove-orphans --force-recreate
```
Force rebuild of **ONLY ONE** service: 
```
 docker compose -f ./docker-compose.[dev|prod].yml build <service name>
```
List all images on the host system: 
```
 docker image list -a
```  
List all containers (running or stopped): 
```
 docker container list -a
```   
Clean up leftover images after several consecutive builds in order to free up disk space (the cache is also discarded): 
```
 docker rmi $(docker images -q -f dangling=true)
 docker builder prune
```
Inspect the logs of a container that **is currently running**:
```
 docker-compose logs -f [container id|container name]
```
Get a shell inside of a container
```
 docker exec -it <container name> /bin/bash
```
