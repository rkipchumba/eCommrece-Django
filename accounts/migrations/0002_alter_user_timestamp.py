# Generated by Django 4.2.5 on 2023-11-01 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
