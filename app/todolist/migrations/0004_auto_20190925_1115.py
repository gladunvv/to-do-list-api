# Generated by Django 2.2.5 on 2019-09-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_auto_20190925_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='notification_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]