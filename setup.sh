#setup for pyhton and GUI
cd GUI
sudo apt-get install nodejs
npm install
npm run build
cd ..
cd web-services
sudo apt-get install python3
sudo apt-get install pip3
pip install flask
pip install pymongo
pip install flask_cors
pip install requests
pip install mysql-connector
pip install paramiko