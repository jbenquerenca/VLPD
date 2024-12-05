pip install opencv-python scipy matplotlib ftfy regex tqdm Cython
pip install git+https://github.com/openai/CLIP.git
pip install "numpy<1.24"
wget https://openaipublic.azureedge.net/clip/models/afeb0e10f9e5a86da6080e35cf09123aca3b358a0c3e3b6c78a7b63bc04b6762/RN50.pt
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
cd utils
make
cd ..
