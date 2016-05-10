
[![Divhide](http://blog.divhide.com/assets/images/divhide_128px.png)](http://divhide.com/)

# Using a docker connection with ansible

This contains an example of an ansible playbook that starts up a docker container using
docker-machine and uses an ansible docker connection to do the machine setup.

```

# initialize docker-machine
docker-machine start local
eval "$(docker-machine env local)"

# run the playbook using the dynamic inventory
ansible-playbook -i docker-machine.py playbook.yml

# check docker running containers
docker ps

# connect to running instance
docker exec -it XXXXXXX bash

```

You can read more about it on [this](http://divhide.com/2016/05/10/creating-an-ansible-docker-connection-with-docker-machine/) blog post.

# Author

Oscar Brito
