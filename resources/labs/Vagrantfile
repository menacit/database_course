# SPDX-FileCopyrightText: © 2024 Menacit AB <foss@menacit.se>
# SPDX-License-Identifier: CC-BY-SA-4.0
# X-Context: Database course

# Vagrant configuration for setting up lab system VM
Vagrant.configure("2") do |config|
  config.vm.hostname = "database-lab-system"
  # Base lab system on Ubuntu 22.04 LTS (generic box works with VMMs besides VirtualBox)
  config.vm.box = "generic/ubuntu2204"
  config.vm.box_check_update = false
  # Expose course resources (labs, quizzes, etc.) on "/course_data" in lab VM
  config.vm.synced_folder "..", "/course_data", SharedFoldersEnableSymlinksCreate: true
  config.vm.synced_folder ".", "/vagrant", SharedFoldersEnableSymlinksCreate: true

  # Configure port forwarding of (10001-10009/TCP) for accessing lab web applications running in VM
  (1..9).each do |port_suffix|
    port = 10000 + port_suffix
    config.vm.network "forwarded_port", guest: port, host: port, host_ip: "127.0.0.1"
  end

  # Provision VM using Ansible playbook
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "setup_lab_system.yml"
  end
end
