# Generated by Django 5.1.6 on 2025-03-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacto', '0013_producto_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opcionproducto',
            name='precio_extra',
        ),
        migrations.AddField(
            model_name='producto',
            name='tiene_opciones',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='opcionproducto',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='opcionproducto',
            name='valor',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_base',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='tipo',
            field=models.CharField(choices=[('general', 'General'), ('extintor', 'Extintor'), ('plano_3d', 'Plano 3D')], default='general', max_length=20),
        ),
    ]
