import facebook
from django.conf import settings

def upload_to_facebook(file_path, caption, page_id=None, group_id=None):
    try:
        print(f"Page ID: {page_id}, Access Token: {settings.FACEBOOK_ACCESS_TOKEN}")
        graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN, version='2.12')  # نسخه API به‌روز
        if page_id:
            if file_path.endswith(('.jpg', '.jpeg', '.png')):
                with open(file_path, 'rb') as file:
                    graph.put_photo(image=file, message=caption, page_id=page_id)
            elif file_path.endswith(('.mp4', '.mov')):
                with open(file_path, 'rb') as file:
                    graph.put_video(page_id=page_id, source=file, description=caption)
        elif group_id:
            if file_path.endswith(('.jpg', '.jpeg', '.png')):
                with open(file_path, 'rb') as file:
                    graph.put_photo(image=file, message=caption, album_path=f"{group_id}/photos")
            elif file_path.endswith(('.mp4', '.mov')):
                with open(file_path, 'rb') as file:
                    graph.put_video(group_id=group_id, source=file, description=caption)
        return True
    except facebook.GraphAPIError as e:
        raise Exception(f"خطا در آپلود به فیسبوک: {str(e)}")
    except Exception as e:
        raise Exception(f"خطا در آپلود به فیسبوک: {str(e)}")