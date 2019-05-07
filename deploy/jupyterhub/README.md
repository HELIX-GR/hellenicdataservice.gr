# README - Setup jupyterhub #

## 0. Prerequisites ##

### 0.1 Ansible Environment ###

You must install `Ansible` on the control machine, preferably in a virtual Python environment:

    virtualenv pyenv
    . pyenv/bin/activate
    pip install ansible==2.5 netaddr

### 0.2 Provide SSH keys ###

Place your PEM-formatted private key under `keys/id_rsa` and corresponding public key under `keys/id_rsa.pub`. 
Ensure that private key has proper permissions (`0600`).  

### 0.3 Provide key/certificate pair for JupyterHub server ###

Place the key/certificate pair for JupyterHub server under `certs/server.key` and `certs/server.crt`. 

### 0.4 Create disk storage

Run the (local) ansible playbook to create all needed VDI disk images:

    ansible-playbook -v -i hosts.yml prepare-disk-images.yml

Verify images are created. For example:

    vboxmanage showmediuminfo disk $PWD/data/nfs/1.vdi

## 1. Prepare inventory file ##

An single inventory file should be created at `hosts.yml`. Both `vagrant` and `ansible` will use this same inventory.
An example inventory file can be found [here](hosts.yml.example).

## 1.1 Setup with Vagrant and Ansible ##

If we want a full Vagrant environment (of course we will also need `vagrant` installed), setup the machines and provision in multiple phases.
All phases, apart from the initial `vagrant up`, delegate their work to Ansible playbooks.

Setup machines (networking, ansible prerequisites):

    vagrant up --provision-with=shell,file
    
Setup basic infrastructure (basic software packages, docker engine, NFS server and clients):
    
    vagrant provision --provision-with=setup-basic
    vagrant provision --provision-with=setup-docker
    vagrant provision --provision-with=setup-nfs
    
Setup docker swarm: 

    vagrant provision --provision-with=setup-docker-swarm

Setup JupyterHub: 
    
    vagrant provision --provision-with=setup-jupyterhub

## 1.2 Setup with Ansible only ##

If the target machines (either virtual or physical) are already setup and networked (usually in a private network),
then we can directly play the Ansible playbooks:

    ansible-playbook -u root play-basic.yml
    
    ansible-playbook -u root [-e data_partition=/dev/sdc1] play-docker.yml
    
    ansible-playbook -u root [-e data_partition=/dev/sdc1] play-nfs.yml

    ansible-playbook -u root [-e listen_to_primary_ipv4_address=1] play-docker-swarm.yml
    
    ansible-playbook -u root play-jupyterhub.yml

If we want to only re-play the configuration part for JupyterHub:

    ansible-playbook -u root --step --tags configuration play-jupyterhub.yml

## 2. Docker containers ##

After installing JupyterHub server through the Ansible installer, in your Docker Swarm environment you will have 2 Docker images available (as listed in https://github.com/HELIX-GR/hellenicdataservice.gr/blob/master/deploy/jupyterhub/group_vars/all.yml.example):

    notebook_images:
    - 'jupyterhub/singleuser:0.9'
    - 'jupyter/datascience-notebook:77e10160c7ef'
    default_notebook_image: 'jupyterhub/singleuser:0.9'

### 2.1 JupyterHub SingleUser ###

Built from the `jupyter/base-notebook` base image.

This image contains a single user notebook server for use with [JupyterHub](https://github.com/jupyterhub/jupyterhub). In particular, it is meant to be used with the [DockerSpawner](https://github.com/jupyterhub/dockerspawner/blob/master/dockerspawner/dockerspawner.py) class to launch user notebook servers within docker containers.

The only thing this image accomplishes is pinning the jupyterhub version on top of base-notebook.
In most cases, one of the Jupyter [docker-stacks](https://github.com/jupyter/docker-stacks) is a better choice.
You will just have to make sure that you have the right version of JupyterHub installed in your image, which can usually be accomplished with one line:

```Dockerfile
FROM jupyter/base-notebook:5ded1de07260
RUN pip3 install jupyterhub==0.7.2
```

The dockerfile that builds this image exposes `BASE_IMAGE` and `JUPYTERHUB_VERSION` as build args, so you can do:

    docker build -t singleuser \
      --build-arg BASE_IMAGE=jupyter/scipy-notebook \
      --build-arg JUPYTERHUB_VERSION=0.8.0 \
      .

in this directory to get a new image `singleuser` that is based on `jupyter/scipy-notebook` with JupyterHub 0.8, for example.

This particular image runs as the `jovyan` user, with home directory at `/home/jovyan`. Dockerfile available at https://github.com/jupyterhub/jupyterhub/blob/master/singleuser/Dockerfile

### 2.2 Jupyter DataScience ###

Built from the `jupyter/scipy-notebook` base image.

This image includes libraries for data analysis from the Julia, Python, and R communities. The image includes:
* Minimally-functional Jupyter Notebook server (e.g., no pandoc for saving notebooks as PDFs)
* Miniconda Python 3.x in /opt/conda
* Pandoc and TeX Live for notebook document conversion
* git, emacs, jed, nano, tzdata, and unzip
* pandas, numexpr, matplotlib, scipy, seaborn, scikit-learn, scikit-image, sympy, cython, patsy, statsmodel, cloudpickle, dill, numba, bokeh, sqlalchemy, hdf5, vincent, beautifulsoup, protobuf, and xlrd packages
* ipywidgets for interactive visualizations in Python notebooks
* Facets for visualizing machine learning datasets
* The R interpreter and base environment
* IRKernel to support R code in Jupyter notebooks
* tidyverse packages, including ggplot2, dplyr, tidyr, readr, purrr, tibble, stringr, lubridate, and broom from conda-forge
* plyr, devtools, shiny, rmarkdown, forecast, rsqlite, reshape2, nycflights13, caret, rcurl, and randomforest packages from conda-forge
* The Julia compiler and base environment
* IJulia to support Julia code in Jupyter notebooks
* HDF5, Gadfly, and RDatasets packages

For more details see https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-datascience-notebook

Dockerfile available at https://github.com/jupyter/docker-stacks/blob/master/datascience-notebook/Dockerfile