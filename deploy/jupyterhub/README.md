# README - Setup jupyterhub #

## 0. Prerequisites ##

### 0.1 Ansible Environment ###

You must install `Ansible` on the control machine, preferably in a virtual Python environment:

    virtualenv pyenv
    . pyenv/bin/activate
    pip install ansible==2.2 netaddr

### 0.2 Provide SSH keys ###

Place your PEM-formatted private key under `keys/id_rsa` and corresponding public key under `keys/id_rsa.pub`. 
Ensure that private key has proper permissions (`0600`).  

## 1. Prepare inventory file ##

An single inventory file should be created at `hosts.yml`. Both `vagrant` and `ansible` will use this same inventory.
An example inventory file can be found [here](hosts.yml.example).

## 2.1 Setup with Vagrant and Ansible ##

If we want a full Vagrant environment (of course we will also need `vagrant` installed), then:

    vagrant up

In this case, `vagrant` will provide the virtual machines (via virtualbox), will setup the private network, 
and then will delegate to an `ansible` playbook to actually setup the swarm nodes.

## 2.2 Setup with Ansible only ##

If the target machines (either virtual or physical) are already setup and networked (usually in a private network),
then we can directly play the Ansible playbook:

    # Prepare target hosts
    ansible -m script -a install-ansible-prereqs.sh all
    # Play
    ansible-playbook play.yml

