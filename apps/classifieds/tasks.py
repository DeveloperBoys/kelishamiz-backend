import aiohttp
import asyncio

from PIL import Image
from io import BytesIO

from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Classified, ClassifiedImage


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
def upload_classified_images(classified_id, uploaded_files):
    batch = []

    for file in uploaded_files:
        output = BytesIO()
        if file.size > 2*1024*1024:
            Image.open(file).convert('RGB').save(
                output, format='JPEG', optimize=True, quality=85)
        output.seek(0)
        optimized_file = SimpleUploadedFile(
            file.name, output.read())
        image = ClassifiedImage(
            classified_id=classified_id,
            image=optimized_file
        )
        batch.append(image)

    return ClassifiedImage.objects.bulk_create(batch)
