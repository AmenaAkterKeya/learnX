# Generated by Django 5.0.6 on 2024-07-12 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='course/img/default.jpg', upload_to='course/course_pic/', verbose_name='Image'),
        ),
    ]
