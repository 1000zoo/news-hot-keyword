# Generated by Django 5.0.4 on 2024-04-15 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
