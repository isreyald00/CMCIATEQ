# Generated by Django 4.2.5 on 2023-11-30 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calibracion',
            fields=[
                ('cod_cer_cal', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('fecha_cap', models.DateField(auto_now_add=True)),
                ('proveedor', models.CharField(max_length=50)),
                ('id_patron', models.CharField(max_length=100)),
                ('doc', models.FileField(upload_to='docs/calibracion')),
                ('dictamen', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='CriteriosCalibracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=10)),
            ],
        ),
    ]
