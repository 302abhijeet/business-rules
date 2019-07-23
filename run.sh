cd GUI
npm run build
serve -l 5001 -s build &
cd .. 
cd web-services
python3.7 main_server.py