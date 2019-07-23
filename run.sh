cd GUI
npm run build
serve -l 5001 -s build &
cd .. 
cd web-services
python main_server