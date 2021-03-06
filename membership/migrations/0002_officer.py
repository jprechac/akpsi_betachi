# Generated by Django 2.2.5 on 2019-09-23 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('position', models.CharField(choices=[('president', 'President'), ('evp', 'Executive Vice President'), ('vpm', 'Vice President of Membership'), ('vpf', 'Vice President of Finance'), ('vppd', 'Vice President of Professional Development'), ('vpar', 'Vice President of Alumni Relations'), ('vppr', 'Vice President of Public Relations'), ('dor', 'Director of Recruitment'), ('docr', 'Director of Corporate Relations'), ('secretary', 'Secretary'), ('mor', 'Master of Rituals'), ('treasurer', 'Treasurer'), ('social', 'Social Chair'), ('service', 'Service Chair'), ('historian', 'Historian'), ('webmaster', 'Webmaster'), ('dpr', 'Director of Public Relations'), ('warden', 'Warden')], max_length=255)),
                ('member_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akpsi_core.Member')),
                ('sem_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akpsi_core.Semester')),
            ],
        ),
    ]
