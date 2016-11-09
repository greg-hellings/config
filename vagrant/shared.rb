# shared.rb
# A shared method for allowing me to spin up multiple VMs easily with easily repeated IP addresses

$ip = 2

def vm(config, name, base_box='fedora/24-cloud-base')
    config.vm.define name do |node|
        node.vm.box = base_box
        node.vm.hostname = name + ".box"
        node.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0"
        node.vm.synced_folder "../..", "/vagrant", type: "sshfs"
        node.vm.provision "ansible" do |ansible|
            ansible.playbook = "../../site.yml"
            yield ansible if block_given?
        end
        $ip += 1
    end
end
