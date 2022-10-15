# Generated by Django 4.1.2 on 2022-10-15 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=60)),
                ('main_text', models.TextField(blank=True)),
                ('language', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Hero',
        ),
    ]
