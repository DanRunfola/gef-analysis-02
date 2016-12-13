
# general setup

requires vagrant and virtual box
`sudo apt-get install-y vagrant virutalbox`

1. clone/pull this repo
2. `cd /path/to/repo`
3. `vagrant up` to build VM
4. `vagrant ssh` to access VM
5. `bash /vagrant/vagrant_setup.sh` to prepare environment (will be automated via vagrant up command eventually)
6. run analysis / do any other work in VM
7. use CTRL-D or exit in vagrant terminal to exit (same as any other shell)
8. `vagrant destroy` to kill the VM


# To create a "release" of this repo which can be use later for replication/testing purposes:

If you are using the latest versions of geoML, CausualForest, and any other referenced repos:

1. run analysis
2. push results of analysis to your project's github repo (optional)
3. update `vagrant_setup.sh` by uncommenting the appropriate `git checkout` lines and update the hash to the current commits of each repo (geoML, CausalForest, etc.)
4. push changes to your project's github repo
5. create new release via github for your project's repo

the code which includes the vagrant box VM setup for this release can now be downloaded later and will pull the specific versions any other repos used to run the script, and use the current set of scripts/data for your project
