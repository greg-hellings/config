# shared.rb
# A shared method for allowing me to spin up multiple VMs easily with easily repeated IP addresses

$ip = 2

def local_setup(node, base_box)
	node.vm.box = base_box
	node.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0"
	$ip += 1
	node.vm.synced_folder "../..", "/home/vagrant/dev", type: "sshfs", sshfs_opts_append: "-o idmap=user"
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
		node.vm.synced_folder ".", "/vagrant", disabled: true
		node.vm.provider :openstack do |os, override|
			os.image = get_image(base_box)
			override.ssh.username = get_username(base_box)
			os.server_name = 'pet-' + ENV['USER'] + '-' + name
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
