#!/bin/bash

sudo apt-get install python3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

sudo apt-get install python3-pip
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

sudo apt-get install python3-setuptools
sudo apt-get install python3-dev

sudo pip3 install Django==2.0.5
sudo pip3 install django-bootstrap4
sudo pip3 install libsass django-compressor django-sass-processor

# REST
#sudo pip3 install djangorestframework
#sudo pip install markdown       # Markdown support for the browsable API.
#sudo pip install django-filter  # Filtering support

#Swagger
#sudo apt-get install python3-dev
#sudo pip install django-rest-swagger

