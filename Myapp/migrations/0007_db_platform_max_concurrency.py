# Generated by Django 2.2 on 2023-08-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0006_db_platform_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_platform',
            name='max_Concurrency',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
