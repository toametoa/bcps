# Generated by Django 2.1.4 on 2019-04-24 05:00

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190423_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uconfig',
            field=jsonfield.fields.JSONField(blank=True, default={'emaill': 'Email Is Empty!', 'host_con': 'not ok', 'imap': 'IMAP Is Empty!', 'link1': 'example.com', 'link2': 'example.com', 'name': 'Name Is Empty!', 'pass': 'Password Is Empty!', 'port': 'Port Is Empty!', 'smtp': 'SMTP Is Empty!'}),
        ),
    ]
