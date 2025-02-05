# Generated by Django 5.1 on 2024-09-06 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to='audio', verbose_name='Аудио используемые в боте')),
                ('file_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='File_Id аудиофайла')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок аудио')),
                ('performer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Исполнитель аудио')),
            ],
            options={
                'verbose_name': 'аудио для бота',
                'verbose_name_plural': 'аудио для бота',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('path', models.ImageField(upload_to='image', verbose_name='Изображения используемые в боте')),
                ('file_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='File_Id изображения')),
            ],
            options={
                'verbose_name': 'изображение для бота',
                'verbose_name_plural': 'изображения для бота',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название локации')),
                ('latitude', models.DecimalField(decimal_places=16, max_digits=18, verbose_name='Координата широты локации')),
                ('longitude', models.DecimalField(decimal_places=16, max_digits=18, verbose_name='Координата долготы локации')),
            ],
            options={
                'verbose_name': 'локацию',
                'verbose_name_plural': 'локации',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position', models.IntegerField(primary_key=True, serialize=False, verbose_name='Порядок частей')),
                ('title', models.CharField(max_length=255, verbose_name='Название части')),
                ('admin_comment', models.TextField(blank=True, null=True, verbose_name='Комментарии к позиции в админ панели')),
            ],
            options={
                'verbose_name': 'позиция',
                'verbose_name_plural': 'позиции',
            },
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('path', models.ImageField(upload_to='image', verbose_name='Изображения для обложки аудио (не больше 200kb и 320wh)')),
                ('file_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='File_Id изображения')),
            ],
            options={
                'verbose_name': 'изображение для обложки трека',
                'verbose_name_plural': 'изображения для обложки трека',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Телеграм-ID пользователя')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия пользователя')),
                ('username', models.CharField(max_length=50, verbose_name='Ссылка пользователя')),
                ('is_admin', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата добавления пользователя')),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'профили пользователя',
            },
        ),
        migrations.CreateModel(
            name='BotMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=50, verbose_name='Служебная команда бота')),
                ('text', models.TextField(verbose_name='Сообщение на команду')),
                ('img', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_bot.image', verbose_name='Изображение для команды')),
            ],
            options={
                'verbose_name': 'служебное сообщение для бота',
                'verbose_name_plural': 'служебные сообщения для бота',
            },
        ),
        migrations.CreateModel(
            name='ReplyMarkup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_text', models.CharField(max_length=30, verbose_name='Текст на кнопке')),
                ('callback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='callback_positions', to='admin_bot.position', verbose_name='Ссылка на эпизод перехода')),
            ],
            options={
                'verbose_name': 'кнопку переключения на другую позицию',
                'verbose_name_plural': 'кнопки переключения на другую позицию',
            },
        ),
        migrations.CreateModel(
            name='MapMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Коммент пояснение для админ панели')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.location', verbose_name='Локация для сообщения')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.position')),
                ('reply_markup', models.ManyToManyField(to='admin_bot.replymarkup')),
            ],
            options={
                'verbose_name': 'сообщение c картой',
                'verbose_name_plural': 'сообщение с картой',
            },
        ),
        migrations.CreateModel(
            name='ImageMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Заголовок для изображения')),
                ('admin_comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Коммент пояснение для админ панели')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.image', verbose_name='Изображение для сообщения')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.position')),
                ('reply_markup', models.ManyToManyField(to='admin_bot.replymarkup')),
            ],
            options={
                'verbose_name': 'сообщение с изображением',
                'verbose_name_plural': 'сообщения с изображениями',
            },
        ),
        migrations.CreateModel(
            name='AudioMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Заголовок под аудио')),
                ('admin_comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Коммент пояснение для админ панели')),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.audio', verbose_name='Аудиофайл для сообщения')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.position')),
                ('reply_markup', models.ManyToManyField(to='admin_bot.replymarkup')),
            ],
            options={
                'verbose_name': 'сообщение с аудио',
                'verbose_name_plural': 'сообщения с аудио',
            },
        ),
        migrations.CreateModel(
            name='SimpleMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст для сообщения')),
                ('admin_comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Коммент пояснение для админ панели')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_bot.position')),
                ('reply_markup', models.ManyToManyField(to='admin_bot.replymarkup')),
            ],
            options={
                'verbose_name': 'сообщение просто с текстом',
                'verbose_name_plural': 'сообщения просто с текстом',
            },
        ),
        migrations.AddField(
            model_name='audio',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='admin_bot.thumbnail', verbose_name='Обложка для трека'),
        ),
    ]
