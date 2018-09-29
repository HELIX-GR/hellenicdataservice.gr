FROM 'jupyterhub/jupyterhub:0.9'

RUN pip install oauthenticator dockerspawner

# For debug purposes only
RUN apt-get update && apt-get install -y vim

COPY jupyterhub_config.py server.key server.crt /srv/jupyterhub/
