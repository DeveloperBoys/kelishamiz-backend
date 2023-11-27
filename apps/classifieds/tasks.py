import aiohttp
import asyncio
from celery import shared_task

from .models import Classified
from .serializers import ClassifiedSerializer


@shared_task
async def notify_bot(classified_data):
    url = "https://bot.kelishamiz.uz/classified"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=classified_data) as response:
            response_text = await response.text()
            print(f"Notified bot, got response: {response_text}")
            return response_text


@shared_task
def trigger_bot_notification(classified_id):
    classified = Classified.objects.get(id=classified_id)

    serializer = ClassifiedSerializer(classified)
    data = serializer.data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(notify_bot(data))
