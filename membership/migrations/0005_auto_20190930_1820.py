# Generated by Django 2.2.5 on 2019-09-30 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0004_auto_20190930_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='chapter_status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('senior', 'Distinguished Senior'), ('ti', 'Temporary Inactive')], db_column='chapter_status', max_length=255, null=True),
        ),
    ]
