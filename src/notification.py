from client import client
import asyncio

async def send_dm(event):
    try:
        user = await asyncio.wait_for(client.fetch_user(event[2]), timeout=10)
        await asyncio.wait_for(user.send("Event " + event[0] + " is now!"), timeout=5)
    except asyncio.TimeoutError:
        print(f"Sending DM to user {event[2]} timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")