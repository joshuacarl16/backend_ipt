# Generated by Django 4.2 on 2023-06-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_reply_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='showReply',
        ),
        migrations.AddField(
            model_name='comment',
            name='replies',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
