# Generated by Django 2.0.5 on 2018-10-17 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=100)),
                ('content_image', models.ImageField(upload_to='images/material/content/')),
                ('content_segmap', models.ImageField(upload_to='images/material/content_segmap')),
                ('style_image', models.ImageField(upload_to='images/material/style/')),
                ('style_segmap', models.ImageField(upload_to='images/material/style_segmap')),
                ('parameters', models.TextField(blank=True)),
                ('great_result', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_image', models.ImageField(upload_to='images/result/')),
                ('iteration', models.IntegerField()),
                ('result_info', models.TextField(blank=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='neuralartcms.Material')),
            ],
        ),
    ]
