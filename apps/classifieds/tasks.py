import os
import uuid
import aiohttp
import asyncio

from PIL import Image
from io import BytesIO

from celery import shared_task
from django.conf import settings
from django.core.files import File

from .models import Classified, ClassifiedImage, PENDING


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

    from .serializers import ClassifiedSerializer

    serializer = ClassifiedSerializer(classified)
    data = serializer.data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(notify_bot(data))


@shared_task
def upload_classified_images(classified_id, uploaded_images):
    classified = Classified.objects.get(pk=classified_id)

    for image in uploaded_images:

        if image.size > 2*1024*1024:
            output = BytesIO()
            Image.open(image).convert('RGB').save(
                output, format='JPEG', optimize=True, quality=85
            )
            output.seek(0)
            image = File(output, name=image.name)

        filename = f'{uuid.uuid4()}.{image.name.split(".")[-1]}'

        path = os.path.join(
            settings.MEDIA_ROOT, 'classifieds', str(classified.id), filename
        )

        with open(path, 'wb+') as dest:
            for chunk in image.read():
                dest.write(chunk)

        classified_image = ClassifiedImage(
            classified=classified,
            image=path
        )
        classified_image.save()

    classified.status = PENDING
    classified.save()
