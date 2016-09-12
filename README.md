

# Introduction
The tournament runs a Swiss type tournament as long as there is an even 
number of registered players and one tournament is played at a time. 

# requirements

## Vagrant and Virtual Box
this project is using 
1. [Vagrant](https://www.vagrantup.com/downloads.html)
2. [Virtual Box](https://www.virtualbox.org/wiki/Downloads).
Vagrant is the software that configures the virtual machine and lets you share files between the host computer and the VM's filesystem.
Virtual Box is the software that runs the virtual machine 

## PostgreSQL
The database used for this project. Make sure that PostgreSQL is installed on your system

## psychopg2 and bleach
This project imported 2 libraries: psychopg2 and bleach

# To access the documents in the VM
please follow the steps describe [here](https://www.udacity.com/wiki/ud197/install-vagrant) under the `Use Git/Github to fetch the VM configuration` heading

# Run the virtual machine
1. Make sure you are in the correct directory: `cd /fullstack/vagrant/`
2. Type `vagrant` up
3. When the VM is running, type `vagrant ssh`

# References
https://www.udacity.com/wiki/ud197/install-vagrant
