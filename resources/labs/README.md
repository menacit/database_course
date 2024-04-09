<!--
SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
SPDX-License-Identifier: CC-BY-SA-4.0
X-Context: Database course
-->

# Database course - Labs
See subdirectories (if any) for specific lab instructions.


## Setup lab environment
In order to participate in the course labs, several tools need to be installed and configured on
the student's lab system. There are three possible paths for setting up the lab environment:

1. **Automated:** Uses automation tools to create a VM/configure a VM with required software
2. **Assisted:** Execute automation of existing system to install/configure required software
3. **Manual:** Install and configure required software manually on an existing system


### Automated setup
As prerequisites for an automated and isolated setup, the following software components must be
installed on the student's host/physical computer (supports Windows, macOS and Linux):

- [**Virtualbox**](https://www.virtualbox.org/): Software for running virtual machines ("VMs")
- [**Vagrant**](https://developer.hashicorp.com/vagrant/downloads): Automation tool for VM setup

Open a command prompt/terminal/PowerShell and navigate to the file system path containing the
course "labs" directory (the same folder this README file is stored in):

```
$ cd /my/path/to/database_course/resources/labs
```

Execute the following command and wait a minute for Vagrant to create/configure a lab VM:

```
$ vagrant up
```

If the command above executed successfully, issue the command below to access the lab environment:

```
$ vagrant ssh
```

To verify the installation, execute the following command in the Vagrant SSH session - it should
return a version number and nothing else:

```
$ docker compose version --short
```

Vagrant automatically shares the course "resources" directory between the host computer and the VM,
which can be utilized to access lab files and similar. In order to access it, navigate to the path
"/course\_data" once inside the lab environment.  

If problems occur during the setup process, students should read through the "Common issues"
section below before contacting the course teacher for support.
 

## Assisted setup
Users who, for whatever reason, can't/prefer not to use Vagrant and/or VirtualBox may opt for an
assisted setup of the lab system. This can be done on a physical or virtual machine, provided that
it runs Ubuntu 22.04 LTS or a compatible derivative

For assisted setup, install [Ansible](https://www.ansible.com/) (available in most OS repositories)
and run the Ansible playbook "resources/labs/setup\_lab\_system.yml" on the target system:

```
$ sudo ansible-playbook -v -c local -e default_user="${USER}" setup_lab_system.yml 
```

After the playbook execution, restart your host (or logout/login of the user session).
In order to verify that the assisted installation was successful, execute the command below:

```
$ docker run --rm docker.io/library/hello-world:latest
```

To verify the installation/configuration of the Docker compose plugin, execute the following
command - it should return a version number and nothing else:

```
$ docker compose version --short
```


## Manual setup
In order to manually setup a lab environment, a Linux host with shell access (cloud, local VM or
bare metal - doesn't matter) is required.

Install Docker and the Docker Compose-plugin on the Linux host according to the
[official instructions](https://docs.docker.com/engine/install/) (_no Snaps/Flatpaks, please_).  
Also install "sqlite" version 3 or later (package name is usually "sqlite3").

If the student wants to execute Docker CLI commands as an unprivileged user (non-root), issue the
following command on the lab system and restart the terminal session/SSH connection:

```
$ sudo usermod -a -G docker "${USER}"
```

In order to verify that Docker has been installed correctly, execute the command below:

```
$ docker run --rm docker.io/library/hello-world:latest
```

To verify the installation/configuration of the Docker compose plugin, execute the following
command - it should return a version number and nothing else:

```
$ docker compose version --short
```

For troubleshooting, the student should refer to the official Docker documentation before
consulting/requesting support from the teacher.


## Common issues

### Problems starting Vagrant VM
The most common issue type student experience is problems accessing their VM when executing the
command "vagrant up". This typically occurs when the command is not executed in the correct
directory. Before issuing any Vagrant commands, ensure that the current working directory is the
course "labs" folder:

```
$ cd /my/path/to/database_course/resources/labs
```


### Enabling virtualisation support
Virtualisation software like VirtualBox relies on hardware features included in most processors.
These features are typically enabled by default, but some computer manufacturers require that they
are explicitly enabled.  
  
If the student is experiencing issues creating virtual machines, review "step one" and "step two"
in [Microsoft's virtualisation support documentation](https://support.microsoft.com/en-us/windows/enable-virtualization-on-windows-11-pcs-c5578302-6e43-4b4b-a449-8ced115f58e1).


### "Incompatible character encodings"
Vagrant doesn't handle file system paths well with non-ASCII character/mixed character encoding.  
Users who encounter error messages such as "join: incompatible character encodings: CP850 and..."
have two options: create a new user account/file system path containing only ASCII characters (A-Z)
or reconfigure the Vagrant path settings, as documented below.  
  
On Windows, start a command prompt **as administrator** (right click "Run as administrator") and
execute the following commands:

```
$ md "C:\vagrant_data"
$ setx VAGRANT_HOME "C:/vagrant_data"
$ setx GEM_HOME "C:/vagrant_data"
$ takeown /a /r /f "C:\vagrant_data"
$ "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setproperty machinefolder "C:\vagrant_data"
```

Copy the "resources" directory into "C:\\vagrant\_data" and re-execute "vagrant up".


### "Permission denied" when using Gitbash
On a Windows system, Vagrant commands should not be executed in a "Gitbash" shell as it has known
compatibility issues, especially related to SSH authentication to the guest VM. If possible,
utilize a PowerShell prompt or the ["Windows Terminal" app](https://aka.ms/terminal) instead.
