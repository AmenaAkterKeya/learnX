# Generated by Django 5.0.6 on 2024-07-12 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]