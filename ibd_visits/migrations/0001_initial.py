# Generated by Django 4.1.6 on 2023-02-13 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_free', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.IntegerField(choices=[(1, '8:00'), (2, '8:30'), (3, '9:00'), (4, '9:30'), (5, '10:00'), (6, '10:30'), (7, '11:00'), (8, '11:30'), (9, '12:00'), (10, '12:30'), (11, '13:00'), (12, '13:30'), (13, '14:00'), (14, '14:30'), (15, '15:00'), (16, '15:30'), (17, '16:00'), (18, '16:30'), (19, '17:00'), (20, '17:30')])),
            ],
        ),
    ]
