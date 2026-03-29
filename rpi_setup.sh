# Download repo
cd ~/Desktop
git clone https://github.com/kezzyhko/led-matrix
cd led-matrix

# Install conda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aaarch64.sh
chmod +x Miniconda3-latest-Linux-aarch64.sh
./Miniconda3-latest-Linux-aarch64.sh
rm Miniconda3-latest-Linux-aarch64.sh
source ~/.bashrc

# Install dependencies
conda env create
conda activate led-matrix
cp example_config.cfg config.cfg

