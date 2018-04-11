# -*- mode: ruby -*-
# vi: set ft=ruby :

# This is the basic entry-point method here. You can use this
# to just create vms ad nauseum in your Vagrantfile. From within
# your main Vagrantfile configuration block, just call to this
# method to create as many VMs as you want. So your Vagrantfile
# can look as simple as
# Vagrant.configure('2') do config
#   vm(config, "myhost")
# end
def vm(config, name, base_box='fedora/27-cloud-base')
	config.vm.define name do |node|
		node.vm.provider :libvirt do |libvirt, override|
			local_setup(override, base_box)
			libvirt.memory = 4096
			libvirt.cpus = 2
		end
		node.vm.provider :virtualbox do |virtualbox, override|
			local_setup(override, base_box)
		end
		node.vm.hostname = name + ".box"
		node.vm.synced_folder ".", "/vagrant", disabled: true
		node.vm.provider :openstack do |os, override|
			os.image = get_image(base_box)
			override.ssh.username = get_username(base_box)
			os.server_name = 'pet-' + ENV['USER'] + '-' + name
		end
		yield node if block_given?
	end
end

# Use this method to add Ansible integration to your Vagrantfile.
# After creating the machine by the above method, you can pass it
# into here to have Ansible run as the provisioner on guest
# creation. You can do something like
# vm(config, "myhost") do node
#   ansible(node)
# end
# in order to run the playbook.
#
# The argument "book" is the path, relative to the main Vagrantfile,
# to the playbook in your repository that ought to be run. If there
# are muliple playbooks that need to be run, in succession, you
# should be able to call this method multiple times
def ansible(config, book='../../playbooks/site.yml')
	config.vm.provision :ansible do |ansible|
		ansible.limit = "all"
		ansible.verbose = "-v"
		ansible.playbook = book
		yield ansible if block_given?
	end
end

# A few methods that are used as helpers in the above work
$ip = 2

def local_setup(node, base_box)
	node.vm.box = base_box
	node.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0", libvirt__guest_ipv6: 'yes'
	$ip += 1
	node.vm.synced_folder "../..", "/home/vagrant/dev", type: "sshfs", sshfs_opts_append: "-o idmap=user"
end

def get_username(base_box)
	if base_box.start_with?('centos')
		return 'centos'
	elsif base_box.start_with?('rhel')
		return 'root'
	else
		return 'fedora'
	end
end

def get_image(base_box)
	if base_box == 'centos/7'
		return 'CentOS-7-x86_64-GenericCloud-released-latest'
	elsif base_box == 'centos/6'
		return 'CentOS-6-x86_64-GenericCloud-released-latest'
	elsif base_box == 'fedora/25-cloud-base'
		return 'Fedora-Cloud-Base-25-compose-latest'
	elsif base_box == 'fedora/24-cloud-base'
		return 'Fedora-Cloud-Base-24-compose-latest'
	elsif base_box == 'fedora/27-cloud-base'
		return 'Fedora-Cloud-Base-27-1.6'
	end
end

# This code allows you to use the OpenStack provider to run your VMs while
# not configuring anything more than the normal OS_* named variables that
# the os-client-config Python packages also understand. That way, if your
# host machine is already configured for easy access to your OpenStack instance,
# then you can just run "vagrant --provider openstack up" and this will auto
# configure auth
Vagrant.configure("2") do |config|
	config.vm.provider :openstack do |os, override|
		os.openstack_auth_url = ENV['OS_AUTH_URL']
		os.username = ENV['OS_USERNAME']
		os.password = ENV['OS_PASSWORD']
		os.tenant_name = ENV['OS_PROJECT_NAME']
		os.flavor = ENV['OS_NOVA_FLAVOR']
		os.floating_ip_pool = ENV['OS_FLOATING_NETWORK']
		os.networks = [{ name: ENV['OS_NETWORK'] }]
		os.server_create_timeout = 900
	end
end
