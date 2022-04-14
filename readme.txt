ngrok: http://127.0.0.1:4040
celery: http://localhost:5555


The beginning part is the same as last time
Here is the link: https://bramble-limburger-c57.notion.site/2021-10-21-f26978e3c49f49c296e86a3c092d7f76

After that
1)Install Redis
	sudo apt-get install redis-server
2)Install pip3 package
	pip3 install -r requirements.txt
3)Open four terminal and run each file under this folder
	/ai2021mis/shell_files

How to use the shell file:
1) install the requirements (pip3 install -r requirements.txt)
2) change the run_all.sh 
	2.1) find the file on ai2021mis/shell_files/run_all.sh
	2.2) Change the first line to the way you go to your venv.
		example : usually i will do 
			"cd GitHub/ai2021mis"
			"source VENV/bin/activate"
			Then i will change my firstline to GitHub/ai2021mis/VENV/bin/activate
3) Then run the run_all.sh file using this command on terminal
	= "GitHub/ai2021mis/shell_files/run_all.sh"
