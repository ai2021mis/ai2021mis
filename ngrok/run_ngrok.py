from pyngrok import ngrok

https_tunnel = str(ngrok.connect(8000, bind_tls=True))
https_tunnel = https_tunnel.split('"')[1]
all_tunnel = ngrok.get_tunnels()
print(all_tunnel)

file_name = 'ngrok_link.txt'

with open(file_name, 'w') as file_obj:
    file_obj.write(str(https_tunnel))

ngrok_process = ngrok.get_ngrok_process()

try:
    # Block until CTRL-C or some other terminating event
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print(" Shutting down server.")
    ngrok.kill()
