# Generated by Django 2.2.5 on 2019-09-29 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akpsi_core', '0002_officer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='akpsi_status',
            field=models.CharField(choices=[('Collegiate', 'Collegiate'), ('Alumnus', 'Alumnus'), ('LOA-Military', 'Leave of Absense - Military Leave'), ('LOA-Medical', 'Leave of Absense - Medical Leave'), ('LOA-Hardship', 'Leave of Absense - Extreme Hardship'), ('LOA-Abroad', 'Leave of Absense - Study Abroad'), ('LOA', 'LOA-Unknown'), ('Pledge', 'Pledge'), ('Suspended', 'Suspended'), ('Faculty', 'Faculty Brother'), ('Honorary', 'Honorary Brother')], db_column='akpsi_status', max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], db_column='gender', max_length=1, null=True),
        ),
    ]
