# Generated by Django 4.1.5 on 2023-01-19 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='tstamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='댓글등록일시'),
        ),
    ]