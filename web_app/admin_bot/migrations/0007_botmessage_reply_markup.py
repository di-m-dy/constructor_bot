# Generated by Django 5.1 on 2024-09-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_bot', '0006_alter_audiomessage_position_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='botmessage',
            name='reply_markup',
            field=models.ManyToManyField(blank=True, to='admin_bot.replymarkup'),
        ),
    ]
