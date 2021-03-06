# Generated by Django 3.0.3 on 2020-03-15 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('employee_id', models.CharField(max_length=255, unique=True)),
                ('data_status', models.BooleanField(default=False)),
                ('department', models.CharField(max_length=255, null=True)),
                ('post', models.CharField(blank=True, max_length=255)),
                ('active_status', models.BooleanField(default=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(null=True)),
                ('entry_time', models.TimeField(null=True)),
                ('exit_date', models.DateField(null=True)),
                ('exit_time', models.TimeField(null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Employees')),
            ],
        ),
    ]
