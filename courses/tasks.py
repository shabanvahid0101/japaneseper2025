# courses/tasks.py
from celery import shared_task
from .models import Content
from .social_media import post_to_telegram, post_to_instagram, post_to_youtube

@shared_task
def publish_content(content_id, platforms):
    content = Content.objects.get(id=content_id)
    if 'telegram' in platforms:
        post_to_telegram(content)
    if 'instagram' in platforms:
        post_to_instagram(content)
    if 'youtube' in platforms:
        post_to_youtube(content)