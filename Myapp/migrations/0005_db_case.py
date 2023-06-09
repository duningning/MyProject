# Generated by Django 2.2 on 2023-05-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_auto_20230519_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='-', max_length=50, null=True)),
                ('platform_id', models.CharField(blank=True, max_length=20, null=True)),
                ('Concurrency', models.BooleanField(default=True)),
                ('monitor', models.BooleanField(default=True)),
                ('py', models.CharField(blank=True, max_length=20, null=True)),
                ('counts', models.IntegerField(default=1)),
            ],
        ),
    ]
