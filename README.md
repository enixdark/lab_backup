

### Automation to create user, add ssh create backup for mongodb from localhost and container
- this is collections scripts use ansible to create user, add ssh create backup for mongodb from localhost and container

## Require
- local
  + python >= 2.7
  + ansible >= 2.̀5.0

## Before Setup
- Config remote host , private key ssh in ansible.cfg and hosts file
- add password via ssh-agent to avoid ask about password when remote to any servers
  +  `ssh-agent bash && ssh-add ~/.ssh/id_rsa`
- Config variables for services in environments/staging/group_vars ( example: user, password, etc )
`

## Setup
- Enable exec file in project:
  + `chmod +x *.sh`
- setup virtualenv with ansible
  + ./env.sh
  + source ./venv/bin/activate
  + pip install requirements.txt
- deploy services to server, add -vvvv if you want full logs to check tasks
  + ansible-playbook playbook.yml [-vvvv]

## Note
- this project 's collect distinct tasks, script, so to run it please do:

- Update variables in `roles/labo/defaults` folder
- Run ansible Tasks:
  - For create remote user use:
    + to add new user use `ansible-playbook playbook.yml -vvv -e add_user=true`
    + to remove a user use `ansible-playbook playbook.yml -e user_add=true -e user_remove=true`

  - For add ssh from local to server remote for specific user:
    + `ansible-playbook playbook.yml -e ssh_add=true`
  
  - For to create backup use:
    + `ansible-playbook playbook.yml -e use_backup=true`
  
  - In that case use docker, you 'll need following instruction: 
    + assume, you 'll run docker from command or compose, please create new/mount volume for 2 folder ( data folder and backup folder)
    with container name
    + for example: `docker run -v data:/data/db -v backup:/backup --name labo_mongo -d mongo`
    + then, reconfig variables in `roles/labo/defaults` folder
    + finally, use command:  `ansible-playbook playbook.yml -e use_backup=true -e use_docker=true`
  