# Generated by Django 4.2.2 on 2023-06-13 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione_medici', '0007_commento_commento_combinazione_medico_commentatore'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commento',
            options={'ordering': ['-data'], 'verbose_name_plural': 'Commenti'},
        ),
        migrations.AlterField(
            model_name='commento',
            name='data',
            field=models.DateField(auto_now_add=True),
        ),
    ]
