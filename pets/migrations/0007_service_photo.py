# Generated by Django 4.2.23 on 2025-07-14 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0006_alter_pet_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='pets/photo')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='pets.pet')),
            ],
        ),
    ]
