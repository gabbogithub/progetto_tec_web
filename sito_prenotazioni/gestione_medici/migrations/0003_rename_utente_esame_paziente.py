# Generated by Django 4.2.1 on 2023-05-28 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione_medici', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='esame',
            old_name='utente',
            new_name='paziente',
        ),
    ]
