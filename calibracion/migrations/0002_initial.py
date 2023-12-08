# Generated by Django 4.2.5 on 2023-11-30 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
        ('calibracion', '0001_initial'),
        ('metrologia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EspecificacionCalibracion',
            fields=[
                ('id_equipo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='inventario.equipo')),
                ('periodo', models.IntegerField()),
                ('ultima', models.DateField()),
                ('proxima', models.DateField()),
                ('estatus', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='criterioscalibracion',
            name='cod_cer_cal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='calibracion.calibracion'),
        ),
        migrations.AddField(
            model_name='criterioscalibracion',
            name='id_criterio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='metrologia.criteriosmetrologicos'),
        ),
        migrations.AddField(
            model_name='calibracion',
            name='id_especificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calibracion.especificacioncalibracion'),
        ),
    ]
