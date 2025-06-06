from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django import forms
from .models import Course, Content, PublishReport
from .forms import RegisterForm
from django.conf import settings
import os
import logging
from .instagram_upload import upload_to_instagram
from .telegram_upload import send_to_telegram
from .facebook_upload import upload_to_facebook
import asyncio
from rest_framework import generics
from .serializers import CourseSerializer, ContentSerializer

# تنظیم لاگینگ
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'content_type', 'file', 'course']

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = RegisterForm()
    return render(request, 'courses/register.html', {'form': form})

@login_required
def upload_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save()
            file_path = os.path.join(settings.MEDIA_ROOT, str(content.file))
            caption = f"新しいコンテンツ: {content.title} - {content.course.title}"
            publish_status = {
                'instagram': {'success': False, 'error': None},
                'telegram': {'success': False, 'error': None},
                'facebook': {'success': False, 'error': None}
            }

            try:
                logger.debug("شروع آپلود به اینستاگرام")
                upload_to_instagram(file_path, caption)
                publish_status['instagram']['success'] = True
                logger.info("محتوا در اینستاگرام آپلود شد")
            except Exception as e:
                publish_status['instagram']['error'] = str(e)
                logger.error(f"خطا در اینستاگرام: {e}")

            try:
                logger.debug("شروع ارسال به تلگرام")
                asyncio.run(send_to_telegram(
                    file_path,
                    caption,
                    settings.TELEGRAM_BOT_TOKEN,
                    settings.TELEGRAM_CHAT_ID
                ))
                publish_status['telegram']['success'] = True
                logger.info("محتوا در تلگرام ارسال شد")
            except Exception as e:
                publish_status['telegram']['error'] = str(e)
                logger.error(f"خطا در تلگرام: {e}")

            try:
                logger.debug("شروع آپلود به فیسبوک")
                upload_to_facebook(file_path, caption, page_id=settings.FACEBOOK_PAGE_ID)
                publish_status['facebook']['success'] = True
                logger.info("محتوا در فیسبوک آپلود شد")
            except Exception as e:
                publish_status['facebook']['error'] = str(e)
                logger.error(f"خطا در فیسبوک: {e}")

            # ذخیره گزارش در دیتابیس
            PublishReport.objects.create(
                content=content,
                instagram_success=publish_status['instagram']['success'],
                instagram_error=publish_status['instagram']['error'],
                telegram_success=publish_status['telegram']['success'],
                telegram_error=publish_status['telegram']['error'],
                facebook_success=publish_status['facebook']['success'],
                facebook_error=publish_status['facebook']['error']
            )

            # ذخیره گزارش برای نمایش در پنل
            request.session['publish_status'] = publish_status
            return redirect('publish_report')
    else:
        form = ContentForm()
    return render(request, 'courses/upload_content.html', {'form': form})

def publish_report(request):
    publish_status = request.session.get('publish_status', {})
    reports = PublishReport.objects.all().order_by('-created_at')
    return render(request, 'courses/publish_report.html', {
        'publish_status': publish_status,
        'reports': reports
    })

class CourseListAPI(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ContentListAPI(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer