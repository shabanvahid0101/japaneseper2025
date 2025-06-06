from instagrapi import Client
from django.conf import settings
import os
from moviepy.editor import VideoFileClip

def upload_to_instagram(file_path, caption):
    cl = Client()
    cl.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        cl.photo_upload(file_path, caption)
    elif file_path.endswith(('.mp4', '.mov')):
        clip = VideoFileClip(file_path)
        if clip.duration <= 60:  # حداکثر 60 ثانیه برای پست
            cl.video_upload(file_path, caption)
        else:
            raise ValueError("ویدیو باید کمتر از 60 ثانیه باشد")
    return True