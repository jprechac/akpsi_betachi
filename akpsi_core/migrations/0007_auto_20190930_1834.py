# Generated by Django 2.2.5 on 2019-09-30 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akpsi_core', '0006_auto_20190930_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='position',
            field=models.CharField(choices=[('president', 'President'), ('evp', 'Executive Vice President'), ('vpm', 'Vice President of Membership'), ('vpf', 'Vice President of Finance'), ('vppd', 'Vice President of Professional Development'), ('vpar', 'Vice President of Alumni Relations'), ('vppr', 'Vice President of Public Relations'), ('dor', 'Director of Recruitment'), ('docr', 'Director of Corporate Relations'), ('secretary', 'Secretary'), ('mor', 'Master of Rituals'), ('pledgeEd', 'Pledge Educator'), ('treasurer', 'Treasurer'), ('social', 'Social Chair'), ('service', 'Service Chair'), ('fund', 'Fundraising Chair'), ('historian', 'Historian'), ('webmaster', 'Webmaster'), ('dpr', 'Director of Public Relations'), ('warden', 'Warden')], max_length=255),
        ),
    ]