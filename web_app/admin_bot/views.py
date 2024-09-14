from django.shortcuts import render
from django.http import JsonResponse
from .models import BotMessage, Position, ReplyMarkup, UserProfile
from .models import AudioMessage, ImageMessage, MapMessage, SimpleMessage
from .models import Location, Image, Audio, Thumbnail


# admin_bot

# Create your views here.

def index(request):
    return render(request, 'admin_bot/index.html')


def bot_messages(request):
    messages_data = [item.get_dict for item in BotMessage.objects.all()]
    return JsonResponse(messages_data, safe=False, json_dumps_params={"ensure_ascii": False})


def positions(request):
    position_data = []
    for item in Position.objects.all():
        result = item.get_dict
        result['messages'] = []
        # Simple Message
        result['messages'].extend([i.get_dict for i in item.simple_message.all()])
        result['messages'].extend([i.get_dict for i in item.image_message.all()])
        result['messages'].extend([i.get_dict for i in item.audio_message.all()])
        result['messages'].extend([i.get_dict for i in item.map_message.all()])
        # sort data
        result['messages'] = sorted(result['messages'], key=lambda x: x['num_at_position'])
        position_data.append(result)
    position_data = sorted(position_data, key=lambda x: x["position"])
    return JsonResponse(position_data, safe=False, json_dumps_params={"ensure_ascii": False})


def add_user(request):
    user_id = request.GET.get('user_id')
    first_name = request.GET.get('first_name', "unknown")
    last_name = request.GET.get('last_name', "unknown")
    username = request.GET.get('username', 'unknown')

    if user_id and any((first_name, last_name, username)):
        try:
            UserProfile.objects.create(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=f"https://t.me/{username}"
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "body": f"error: {e}"},
                safe=False,
                json_dumps_params={"ensure_ascii": False}
            )

        result = {
            "status": "ok",
            "body": {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "user_name": username
            }
        }
        return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})

    return JsonResponse(
        {"status": "empty", "body": {}},
        safe=False,
        json_dumps_params={"ensure_ascii": False}
    )


def get_user(request, user_id):
    try:
        user = UserProfile.objects.get(pk=int(user_id))
        result = {
            "status": "ok",
            "body": user.get_dict
        }
        return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})
    except Exception as e:
        return JsonResponse(
            {"status": "error", "body": f"error: {e}"},
            safe=False,
            json_dumps_params={"ensure_ascii": False}
        )


def get_admins(request):
    try:
        admins_data = UserProfile.objects.filter(is_admin=True)
        result = {
            "status": "ok",
            "body": [i.user_id for i in admins_data]
        }
        return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})
    except Exception as e:
        return JsonResponse(
            {"status": "error", "body": f"error: {e}"},
            safe=False,
            json_dumps_params={"ensure_ascii": False}
        )



