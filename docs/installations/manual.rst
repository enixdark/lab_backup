..
   Author: quandc<cqshinn92@gmail.com>
   Maintainer: quandc<cqshinn92@gmail.com>

Manual Installation
===================

Requiremet:
```````````

- Python >= 2.7
- virtualenv
- pip

Setup:
``````

By using pip, you can install ansible on all OS

Use pip command to install:

```pip install ansible```

Note: Some version ansible 'll need to install some tools, libs such as libxml ,paramiko, etc
so to avoid bugs , we should install libs and use python 2.7.

Create new virtualenv to seperate avoid affect to python system.

```virtualenv --python=/usr/bin/python2 .venv```

Active python use virtualenv:

```. bin/.venv/bin/activate```

Now, install all dependency packages for project:

```pip install -r requiremets.txt```


Then update hosts and ssh config for remote servers that you want to access.

In `hosts`  file you can define based on follow structure:

[name]
server1
server2
....
serverN

Where `name` is identify that you use for list of servers and  `server1, server2, ... serverN` 're list ips or domain.

Then, please go to `roles/labo/defaults/main.yml`, this's config file for all functions in project.

Finally, Let's test it:

```ansible-playbook -vvv```


