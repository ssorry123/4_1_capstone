# Generated by Django 3.0.5 on 2020-06-10 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sg', '0004_auto_20200602_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='writing',
            name='category',
            field=models.CharField(default='', max_length=50, verbose_name='카테고리'),
        ),
    ]
