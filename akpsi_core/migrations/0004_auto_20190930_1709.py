# Generated by Django 2.2.5 on 2019-09-30 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akpsi_core', '0003_auto_20190929_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='pledge_classification',
            field=models.CharField(blank=True, choices=[('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Grad Student', 'Graduate Student')], db_column='pledgeClass', max_length=40, null=True),
        ),
    ]
