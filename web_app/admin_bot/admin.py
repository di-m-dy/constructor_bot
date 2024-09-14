from django.contrib import admin
from .models import BotMessage, Position, ReplyMarkup, UserProfile
from .models import AudioMessage, ImageMessage, MapMessage, SimpleMessage
from .models import Location, Image, Audio, Thumbnail

admin.site.site_header = "Admin for Himmash Promenade Bot "
admin.site.site_title = "Admin HimmashPromenade"
admin.site.index_title = "Добро пожаловать в админ панель бота"


class SimpleMessageInline(admin.StackedInline):
    model = SimpleMessage
    extra = 0


class ImageMessageInline(admin.StackedInline):
    model = ImageMessage
    extra = 0


class AudioMessageInline(admin.StackedInline):
    model = AudioMessage
    extra = 0


class MapMessageInline(admin.StackedInline):
    model = MapMessage
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'latitude',
        'longitude'
    ]
    ordering = ['name']


@admin.register(BotMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = [
        'command',
        'text',
        'img'
    ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        'inline_command',
        'title',
    ]
    ordering = ['position']
    inlines = [SimpleMessageInline, ImageMessageInline, AudioMessageInline, MapMessageInline]


@admin.register(ReplyMarkup)
class ReplyMarkupAdmin(admin.ModelAdmin):
    list_display = [
        'button_text',
        'callback'
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'username',
        'created_at'
    ]
    ordering = ['created_at']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    readonly_fields = ['file_id']


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]
    readonly_fields = ['file_id']


@admin.register(Thumbnail)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    readonly_fields = ['file_id']


@admin.register(SimpleMessage)
class SimpleMessageAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'admin_comment'
    ]


@admin.register(ImageMessage)
class ImageMessageAdmin(admin.ModelAdmin):
    list_display = [
        'image'
    ]


@admin.register(AudioMessage)
class AudioMessageAdmin(admin.ModelAdmin):
    list_display = [
        'audio'
    ]


@admin.register(MapMessage)
class MapMessageAdmin(admin.ModelAdmin):
    list_display = [
        'location'
    ]
