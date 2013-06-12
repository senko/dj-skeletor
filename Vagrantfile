Vagrant.configure("2") do |config|
    config.vm.box = "precise32"
    config.vm.synced_folder "salt/", "/srv/salt"
    config.vm.provision :salt do |salt|
        salt.minion_config = "salt/minion"
        salt.run_highstate = true
    end
end

Vagrant::Config.run do |config|
  config.vm.forward_port 80, 8000
end
