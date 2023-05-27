# Generated by Django 4.2.1 on 2023-05-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Esame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipologia', models.CharField(choices=[('ematochimica', 'Ematochimica'), ('urine', 'Urine'), ('oculistica', 'Oculistica'), ('radiografia', 'Radiografia'), ('ginecologia', 'Ginecologia'), ('ecografia', 'Ecografia'), ('risonanza_magnetica', 'Risonanza magnetica'), ('cardiologia', 'Cardiologia'), ('allergologia', 'Allergologia'), ('gastroenterologia', 'gastroenterologia'), ('urologia', 'Urologia'), ('psichiatria', 'Psichiatria'), ('pediatria', 'Pediatria'), ('otorinolaringologia', 'Otorinolaringologia'), ('neurologia', 'Neurologia'), ('dermatologia', 'Dermatologia'), ('endocrinologia', 'Endocrinologia'), ('angiologia', 'Angiologia')], max_length=30)),
                ('data', models.DateTimeField()),
                ('stato', models.CharField(choices=[('disponibile', 'Disponibile'), ('prenotato', 'Prenotato'), ('eseguito', 'Eseguito'), ('cancellato', 'Cancellato')], default='disponibile', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Esami',
                'ordering': ['data'],
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Medici',
            },
        ),
    ]
