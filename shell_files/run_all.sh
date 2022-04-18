source Github/VENV/bin/activate
gnome-terminal -- ./run_ngrok.sh
sleep 10
gnome-terminal -- ./run_server.sh
sleep 5
gnome-terminal -- ./run_celery_worker.sh 
sleep 5
gnome-terminal -- ./run_celery_flower.sh
$SHELL
