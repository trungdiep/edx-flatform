# Generated by Django 2.2.20 on 2021-05-06 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0022_courseoverviewtab_is_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='relative',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='historicalcourseoverview',
            name='relative',
            field=models.DurationField(null=True),
        ),
    ]
