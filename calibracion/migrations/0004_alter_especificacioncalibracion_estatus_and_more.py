# Generated by Django 4.2.5 on 2023-12-01 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calibracion', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especificacioncalibracion',
            name='estatus',
            field=models.CharField(default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='especificacioncalibracion',
            name='proxima',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='especificacioncalibracion',
            name='ultima',
            field=models.DateField(blank=True, null=True),
        ),
    ]