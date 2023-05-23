# Generated by Django 2.2 on 2023-05-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0003_auto_20230510_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='db_platform',
            old_name='url',
            new_name='host',
        ),
        migrations.AddField(
            model_name='db_platform',
            name='monitor_email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='db_platform',
            name='monitor_feishu',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='db_platform',
            name='monitor_phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='db_platform',
            name='monitor_time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]