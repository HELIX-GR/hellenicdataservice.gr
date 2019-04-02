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

## 2.1 Setup with Vagrant and Ansible ##

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

## 2.2 Setup with Ansible only ##

If the target machines (either virtual or physical) are already setup and networked (usually in a private network),
then we can directly play the Ansible playbooks:

    ansible-playbook -u root play-basic.yml
    
    ansible-playbook -u root [-e data_partition=/dev/sdc1] play-docker.yml
    
    ansible-playbook -u root [-e data_partition=/dev/sdc1] play-nfs.yml

    ansible-playbook -u root [-e listen_to_primary_ipv4_address=1] play-docker-swarm.yml
    
    ansible-playbook -u root play-jupyterhub.yml

If we want to only re-play the configuration part for JupyterHub:

    ansible-playbook -u root --step --tags configuration play-jupyterhub.yml

