# Generated by Django 5.0 on 2025-04-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_usuario_reservacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservaciones',
            name='desde',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservaciones',
            name='hasta',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
