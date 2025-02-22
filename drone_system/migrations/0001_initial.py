# Generated by Django 3.1.4 on 2020-12-28 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_system', '0008_delete_locations'),
    ]

    operations = [
        migrations.CreateModel(
            name='locations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='world_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.TextField()),
                ('data', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='routes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('distance', models.PositiveSmallIntegerField()),
                ('city_a', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='city_b', to='drone_system.locations')),
                ('city_b', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='city_a', to='drone_system.locations')),
            ],
        ),
        migrations.CreateModel(
            name='future_bookings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_start_time', models.DateTimeField()),
                ('job_duration', models.PositiveIntegerField(null=True)),
                ('job_finish_time', models.DateTimeField(null=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin', to='drone_system.locations')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination', to='drone_system.locations')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drone_system.routes')),
                ('user', models.ForeignKey(on_delete=models.SET(0), to='user_system.users')),
            ],
        ),
        migrations.CreateModel(
            name='drones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job', models.BooleanField()),
                ('job_start_time', models.DateTimeField(null=True)),
                ('job_duration', models.PositiveIntegerField(null=True)),
                ('job_finish_time', models.DateTimeField(null=True)),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origin_id', to='drone_system.locations')),
                ('future_booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drone_system.future_bookings')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='drone_system.locations')),
                ('origin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='destination_id', to='drone_system.locations')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='drone_system.routes')),
                ('user', models.ForeignKey(null=True, on_delete=models.SET(0), to='user_system.users')),
            ],
        ),
    ]
