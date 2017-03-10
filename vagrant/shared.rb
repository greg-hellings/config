# shared.rb
# A shared method for allowing me to spin up multiple VMs easily with easily repeated IP addresses

$ip = 2

def get_image(base_box)
	if base_box == 'centos/7'
		return 'CentOS-7-x86_64-GenericCloud-released-latest'
	elsif base_box == 'centos/6'
		return 'CentOS-6-x86_64-GenericCloud-released-latest'
	elsif base_box == 'fedora/25-cloud-base'
		return 'Fedora-Cloud-Base-25-compose-latest'
	elsif base_box == 'fedora/24-cloud-base'
		return 'FEdora-Cloud-Base-24-compose-latest'
	end
end

def get_username(base_box)
	if base_box == 'centos/7' or base_box == 'centos/6'
		return 'centos'
	else
		return 'fedora'
	end
end

def local_setup(node, base_box)
	node.vm.box = base_box
	node.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0"
	$ip += 1
	node.vm.synced_folder "../..", "/home/vagrant/dev", type: "sshfs"
end

def vm(config, name, base_box='fedora/25-cloud-base')
    config.vm.define name do |node|
		node.vm.provider :libvirt do |libvirt, override|
			local_setup(override, base_box)
		end
		node.vm.provider :virtualbox do |virtualbox, override|
			local_setup(override, base_box)
		end
        node.vm.hostname = name + ".box"
		node.vm.provider :openstack do |os, override|
			os.openstack_auth_url = ENV['OS_ENDPOINT']
			os.username = ENV['OS_USERNAME']
			os.password = ENV['OS_PASSWORD']
			os.tenant_name = ENV['OS_TENANT']
			os.flavor = ENV['OS_NOVA_FLAVOR']
			os.floating_ip_pool = ENV['OS_FLOATING_NETWORK']
			os.image = get_image(base_box)
			os.server_create_timeout = 900
			override.ssh.username = get_username(base_box)
			#override.vm.synced_folder "../..", "/home/" + get_username(base_box) + "/dev", type: "sshfs"
			override.vm.synced_folder ".", "/vagrant", disabled: true
		end

        yield node if block_given?
    end
end

def ansible(config)
    config.vm.provision :ansible do |ansible|
        ansible.limit = "all"
        ansible.verbose = "-v"
        ansible.playbook = "../../site.yml"
        yield ansible if block_given?
    end
end
