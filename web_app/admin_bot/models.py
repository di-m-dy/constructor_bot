from django.db import models
import os
import requests

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = os.path.join(ROOT_DIR, "media")
TG_TOKEN = os.getenv("TG_TOKEN")
GOD_ID = os.getenv("GOD_ID")


# Create your models here.

class Position(models.Model):
    position = models.IntegerField(primary_key=True, verbose_name='Порядок частей')
    title = models.CharField(max_length=255, verbose_name='Название части')
    admin_comment = models.TextField(null=True, blank=True, verbose_name="Комментарии к позиции в админ панели")

    @property
    def inline_command(self):
        return f"position_{self.position}"

    @property
    def get_dict(self):
        result = {
            "position": self.position,
            "inline_command": self.inline_command
        }
        return result

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'позиция'
        verbose_name_plural = 'позиции'


class Thumbnail(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    path = models.ImageField(upload_to='image',
                             verbose_name='Изображения для обложки аудио (не больше 200kb и 320wh)'
                             )
    file_id = models.CharField(max_length=255, verbose_name='File_Id изображения', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
        file_path = f"{MEDIA_DIR}/{self.path}"
        url = f'https://api.telegram.org/bot{TG_TOKEN}/sendPhoto'
        files = {'photo': open(file_path, 'rb')}
        data = {'chat_id': GOD_ID}
        response = requests.post(url, files=files, data=data, timeout=30)
        if response.status_code == 200 and response.json()['ok']:
            self.file_id = response.json()['result']['photo'][-1]["file_id"]
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )
            params = {
                "chat_id": GOD_ID,
                "text": f"Success add/update thumbnail: {self.name}"
            }
            requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)
        else:
            self.file_id = None
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )
            params = {
                "text": f"Error add/update file: {self.name}",
                "chat_id": GOD_ID,
            }
            requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)

    @property
    def get_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "path": f"{MEDIA_DIR}/{self.path}",
            "file_id": self.file_id
        }
        return result

    class Meta:
        verbose_name = 'изображение для обложки трека'
        verbose_name_plural = 'изображения для обложки трека'


class Image(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    path = models.ImageField(upload_to='image',
                             verbose_name='Изображения используемые в боте'
                             )
    file_id = models.CharField(max_length=255, verbose_name='File_Id изображения', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
        file_path = f"{MEDIA_DIR}/{self.path}"
        url = f'https://api.telegram.org/bot{TG_TOKEN}/sendPhoto'
        files = {'photo': open(file_path, 'rb')}
        data = {'chat_id': GOD_ID}
        response = requests.post(url, files=files, data=data, timeout=30)
        if response.status_code == 200 and response.json()['ok']:
            self.file_id = response.json()['result']['photo'][-1]["file_id"]
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )
            params = {
                "chat_id": GOD_ID,
                "text": f"Success add/update image: {self.name}"
            }
            requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)
        else:
            self.file_id = None
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )
            params = {
                "text": f"Error add/update file: {self.name}",
                "chat_id": GOD_ID,
            }
            requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)

    @property
    def get_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "path": f"{MEDIA_DIR}/{self.path}",
            "file_id": self.file_id
        }
        return result

    class Meta:
        verbose_name = 'изображение для бота'
        verbose_name_plural = 'изображения для бота'


class Audio(models.Model):
    path = models.FileField(upload_to='audio',
                            verbose_name='Аудио используемые в боте'
                            )
    file_id = models.CharField(max_length=255, verbose_name='File_Id аудиофайла', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок аудио", null=True, blank=True)
    performer = models.CharField(max_length=255, verbose_name="Исполнитель аудио", null=True, blank=True)
    thumbnail = models.ForeignKey(
        Thumbnail,
        verbose_name="Обложка для трека",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title if self.title else self.path

    def save(
            self,
            *args,
            update_file_id=False,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
        file_path = f"{MEDIA_DIR}/{self.path}"
        url = f'https://api.telegram.org/bot{TG_TOKEN}/sendAudio'
        files = {'audio': open(file_path, 'rb')}
        if self.thumbnail:
            thumbnail_path = f"{MEDIA_DIR}/{self.thumbnail.path}"
            files['thumb'] = open(thumbnail_path, 'rb')
        data = {'chat_id': GOD_ID}
        params = {"title": self.title, "performer": self.performer}
        response = requests.post(url, files=files, data=data, params=params, timeout=30)
        if response.status_code == 200 and response.json()['ok']:
            self.file_id = response.json()['result']['audio']["file_id"]
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )
            params = {
                "chat_id": GOD_ID,
                "text": f"Success add/update audio: {self.title}"
            }
            requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)
        else:
            self.file_id = None
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )
            params = {
                "text": f"Error add/update audio: {self.title}",
                "chat_id": GOD_ID,
            }
            requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)

    @property
    def get_dict(self):
        result = {
            "id": self.id,
            "title": self.title,
            "performer": self.performer,
            "thumbnail": self.thumbnail.get_dict,
            "path": f"{MEDIA_DIR}/{self.path}",
            "file_id": self.file_id
        }
        return result

    class Meta:
        verbose_name = 'аудио для бота'
        verbose_name_plural = 'аудио для бота'


class Location(models.Model):
    """
    example:
    56.75774806685926, 60.69723453599406
    """
    name = models.CharField(max_length=250, verbose_name='Название локации')
    latitude = models.DecimalField(max_digits=18, decimal_places=16, verbose_name='Координата широты локации')
    longitude = models.DecimalField(max_digits=18, decimal_places=16, verbose_name='Координата долготы локации')

    @property
    def get_dict(self):
        result = {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        return result

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'локацию'
        verbose_name_plural = 'локации'


class ReplyMarkup(models.Model):
    button_text = models.CharField(max_length=30, verbose_name='Текст на кнопке')
    callback = models.ForeignKey(
        Position,
        related_name='callback_positions',
        on_delete=models.CASCADE,
        verbose_name='Ссылка на эпизод перехода'
    )

    @property
    def get_dict(self):
        result = {
            "button_text": self.button_text,
            "callback": self.callback.inline_command
        }
        return result

    def __str__(self):
        return f"{self.button_text}"

    class Meta:
        verbose_name = 'кнопку переключения на другую позицию'
        verbose_name_plural = 'кнопки переключения на другую позицию'


class SimpleMessage(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='simple_message'
    )
    num_at_position = models.IntegerField(verbose_name='Порядковый номер в позиции', default=1)
    reply_markup = models.ManyToManyField(
        ReplyMarkup,
        blank=True
    )
    text = models.TextField(verbose_name='Текст для сообщения')
    admin_comment = models.CharField(
        max_length=100,
        verbose_name='Коммент пояснение для админ панели',
        null=True,
        blank=True
    )

    @property
    def get_dict(self):
        result = {
            'type': 'simple',
            'num_at_position': self.num_at_position,
            "text": self.text,
            "reply_markup": [i.get_dict for i in self.reply_markup.all()]
        }
        return result

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'сообщение просто с текстом'
        verbose_name_plural = 'сообщения просто с текстом'


class ImageMessage(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='image_message'
    )
    num_at_position = models.IntegerField(verbose_name='Порядковый номер в позиции', default=1)
    reply_markup = models.ManyToManyField(
        ReplyMarkup,
        blank=True
    )
    image = models.ForeignKey(
        Image,
        verbose_name='Изображение для сообщения',
        on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=1000, verbose_name='Заголовок для изображения', null=True, blank=True)
    admin_comment = models.CharField(
        max_length=100,
        verbose_name='Коммент пояснение для админ панели',
        null=True,
        blank=True
    )

    @property
    def get_dict(self):
        result = {
            'type': 'image',
            'num_at_position': self.num_at_position,
            "image": self.image.get_dict,
            "caption": self.caption,
            "reply_markup": [i.get_dict for i in self.reply_markup.all()]
        }
        return result

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = 'сообщение с изображением'
        verbose_name_plural = 'сообщения с изображениями'


class AudioMessage(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='audio_message'
    )
    num_at_position = models.IntegerField(verbose_name='Порядковый номер в позиции', default=1)
    reply_markup = models.ManyToManyField(
        ReplyMarkup,
        blank=True
    )
    audio = models.ForeignKey(
        Audio,
        verbose_name='Аудиофайл для сообщения',
        on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=1000, verbose_name='Заголовок под аудио', null=True, blank=True)
    admin_comment = models.CharField(
        max_length=100,
        verbose_name='Коммент пояснение для админ панели',
        null=True,
        blank=True
    )

    @property
    def get_dict(self):
        result = {
            'type': 'audio',
            'num_at_position': self.num_at_position,
            "audio": self.audio.get_dict,
            "caption": self.caption,
            "reply_markup": [i.get_dict for i in self.reply_markup.all()]
        }
        return result

    def __str__(self):
        return str(self.audio)

    class Meta:
        verbose_name = 'сообщение с аудио'
        verbose_name_plural = 'сообщения с аудио'


class MapMessage(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='map_message'
    )
    num_at_position = models.IntegerField(verbose_name='Порядковый номер в позиции', default=1)
    reply_markup = models.ManyToManyField(
        ReplyMarkup,
        blank=True
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Локация для сообщения',
        on_delete=models.CASCADE
    )
    admin_comment = models.CharField(
        max_length=100,
        verbose_name='Коммент пояснение для админ панели',
        null=True,
        blank=True
    )

    @property
    def get_dict(self):
        result = {
            'type': 'map',
            'num_at_position': self.num_at_position,
            "location": self.location.get_dict,
            "reply_markup": [i.get_dict for i in self.reply_markup.all()]
        }
        return result

    def __str__(self):
        return str(self.location)

    class Meta:
        verbose_name = 'сообщение c картой'
        verbose_name_plural = 'сообщение с картой'


class BotMessage(models.Model):
    command = models.CharField(max_length=50, verbose_name='Служебная команда бота')
    text = models.TextField(verbose_name='Сообщение на команду')
    img = models.ForeignKey(
        Image,
        verbose_name="Изображение для команды",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    reply_markup = models.ManyToManyField(
        ReplyMarkup,
        blank=True
    )

    @property
    def get_dict(self):
        result = {
            "command": self.command,
            "text": self.text,
            "img": self.img.get_dict if self.img else None,
            "reply_markup": [i.get_dict for i in self.reply_markup.all()]
        }
        return result

    def __str__(self):
        return f"{self.command}"

    class Meta:
        verbose_name = 'служебное сообщение для бота'
        verbose_name_plural = 'служебные сообщения для бота'


class UserProfile(models.Model):
    user_id = models.IntegerField(primary_key=True, verbose_name='Телеграм-ID пользователя')
    first_name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия пользователя')
    username = models.CharField(max_length=50, verbose_name='Ссылка пользователя')
    is_admin = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата добавления пользователя')

    def __str__(self):
        sep = ' ' if (self.first_name and self.last_name) else ''
        first_name = self.first_name or ''
        last_name = self.last_name or ''
        return f"{first_name}{sep}{last_name}"

    @property
    def get_dict(self):
        result = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "created_at": self.created_at
        }
        return result

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователя'
