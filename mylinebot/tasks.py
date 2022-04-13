from celery import shared_task
import time
import mylinebot
from pyngrok import ngrok

@shared_task(name='Send Alert Message')
def create_task(message):
    for notification_id, message_info in message.items():
        line_id = message_info['lineid']
        alert_id = message_info['alert_id']
        timestamp = message_info['timestamp']
        description = message_info['description']
        continuous_alert = message_info['continuous_alert']
        repeat_interval = message_info['repeat_interval']

        if continuous_alert:
            while True:
                mylinebot.alert.send_alert(line_id, alert_id, timestamp, description, notification_id)
                time.sleep(repeat_interval)
                print(f"pushing messages to <{line_id}>...<{alert_id}>")
        else:
            mylinebot.alert.send_alert(line_id, alert_id, timestamp, description, notification_id)


@shared_task(name='Send Alert Image')
def create_image_task(message):
    for notification_id, message_info in message.items():
        line_id = message_info['line_id']
        alert_id = message_info['alert_id']
        image_url = message_info['image_url']

        mylinebot.alert.send_alert_picture(line_id, alert_id, image_url, notification_id)


@shared_task(name='ngrok')
def turn_on_ngrok():
    http_tunnel = ngrok.connect(8000, bind_tls=True)
    print(http_tunnel)
    http_tunnel2 = ngrok.get_tunnels()
    print(http_tunnel2)

    ngrok_process = ngrok.get_ngrok_process()

    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")
        ngrok.kill()
