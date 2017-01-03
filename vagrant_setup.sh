#!/bin/bash


# to set up vm and access it on your local machine:

# clone/pull repo
# `cd /path/to/repo`
# `vagrant up` to build vm
# `vagrant ssh` to access vm


# -------------------------------------


# -------------------
# general setup

sudo apt-get update
sudo apt-get install -y git


cd ~
rm -rf geoML
git clone https://github.com/itpir/geoML.git
cd geoML
# uncomment following line and edit hash if you
# want to pull specific version of repo
# git checkout 'ce49e6cc2c0ffdce28dc2ad4aa17cfa0baab54a2'


cd ~
rm -rf CausalForest
git clone https://github.com/itpir/CausalForest.git
cd CausalForest
# uncomment following line and edit hash if you
# want to pull specific version of repo
# git checkout 'ce49e6cc2c0ffdce28dc2ad4aa17cfa0baab54a2'


# currently private repo, needs to be public for auto clone without credentials

# cd ~
# rm -rf geoValuate
# git clone https://github.com/itpir/geoValuate.git
# cd geoValuate

# uncomment following line and edit hash if you
# want to pull specific version of repo
# git checkout 'ce49e6cc2c0ffdce28dc2ad4aa17cfa0baab54a2'




# -------------------
# prep vm with scikit and python

cd ~
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86.sh
bash Miniconda2-latest-Linux-x86.sh -b
miniconda2/bin/conda install -y scikit-learn
sudo apt-get install -y python-pip python-dev
sudo pip install --upgrade pip
sudo pip install Cython
sudo pip install nose
sudo pip install numpy
sudo pip install pandas
sudo apt-get install -y python-scipy

cd CausalForest/scikit-learn
make
python setup.py build
sudo python setup.py install


# -------------------
# prep vm with r

cd ~
sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list'
gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
gpg -a --export E084DAB9 | sudo apt-key add -
sudo apt-get update

sudo apt-get -y install r-base-core=3.3.2-1trusty0
sudo apt-get -y --force-yes install r-doc-html=3.3.2-1trusty0
sudo apt-get -y install r-base-dev=3.3.2-1trusty0

sudo apt-get install -y libgdal-dev
sudo apt-get install -y libproj-dev
sudo apt-get install -y libcurl4-openssl-dev

sudo Rscript -e 'install.packages("devtools", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("rgdal", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("stargazer", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("sp", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("MatchIt", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("rpart.plot", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("matrixStats", repos="http://cran.us.r-project.org", dependencies=TRUE)'
sudo Rscript -e 'install.packages("ggplot2", repos="http://cran.us.r-project.org", dependencies=TRUE)'


