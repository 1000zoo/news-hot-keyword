# Generated by Django 5.0.4 on 2024-04-18 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_wordclouds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordclouds',
            name='wordcloud_img',
            field=models.ImageField(null=True, upload_to='wordcloud_pngs'),
        ),
    ]