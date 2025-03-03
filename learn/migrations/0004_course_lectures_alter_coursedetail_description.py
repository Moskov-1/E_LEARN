# Generated by Django 5.1.4 on 2025-01-04 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_remove_instructor_description_instructor_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='lectures',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coursedetail',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
