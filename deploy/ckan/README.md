# README

## 0. Requirements

### 0.1. Provide keys 

Provide key pair under `keys` (`keys/id_rsa` and `keys/id_rsa.pub`). These keys will be installed to all hosts.

### 0.2. Configure

Copy `hosts.yml.example` to `hosts.yml` and edit.

Copy `group_vars/{all,ckan}.yml.example` to `group_vars/{all,ckan}.yml` and edit to adjust to your needs.

## 1. Install

Setup machine:
    
    vagrant up

Install CKAN:

    ansible-playbook -v -u ubuntu play-ckan.yml
