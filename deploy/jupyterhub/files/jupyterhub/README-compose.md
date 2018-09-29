## Compose JupyterHub as a Swarm Service


Build image:

    docker-compose build

Create Swarm service `jupyterhub` inside `jupyterhub` project:

    docker stack deploy -c docker-compose.yml jupyterhub
 
After a while, service `jupyterhub_jupyterhub` should be up and running:

    docker service ps jupyterhub_jupyterhub
    docker service logs jupyterhub_jupyterhub
