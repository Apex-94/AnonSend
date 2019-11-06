# Generated by Django 2.2.6 on 2019-11-05 14:24

from django.db import migrations, models
import django.db.models.deletion
import main.helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('public_link', models.CharField(default=main.helper.gen_link, max_length=15, primary_key=True, serialize=False)),
                ('analytic_link', models.CharField(default=main.helper.gen_analytic_link, max_length=15, unique=True)),
                ('file', models.FileField(upload_to='uploaded_files/')),
                ('password', models.CharField(blank=True, max_length=100)),
                ('expires_at', models.DateTimeField(verbose_name='Expires in')),
                ('max_downloads', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1)),
                ('file_hash', models.CharField(max_length=41)),
                ('file_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ReportLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('malicious', 'Malicious file'), ('inappropriate', 'Inappropriate / Illegal Content'), ('dmca', 'DMCA violation')], default=('malicious', 'Malicious file'), max_length=10)),
                ('description', models.TextField(max_length=150)),
                ('report_time', models.DateTimeField(auto_now_add=True)),
                ('upload_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UploadFile')),
            ],
        ),
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(default='Unknown', max_length=40)),
                ('device_type', models.CharField(default='Unknown', max_length=40)),
                ('browser', models.CharField(default='Unknown', max_length=40)),
                ('country', models.CharField(default='Unknown', max_length=40)),
                ('time_clicked', models.DateTimeField(auto_now_add=True)),
                ('upload_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UploadFile')),
            ],
        ),
    ]
