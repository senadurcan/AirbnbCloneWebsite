# Generated by Django 3.2.16 on 2023-05-05 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_yorum'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='yildiz',
            field=models.IntegerField(null=True),
        ),
    ]