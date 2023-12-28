from client import get_client
from user import notification_loop, setup_event_notifications

client = get_client()
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(notification_loop())
    setup_event_notifications
