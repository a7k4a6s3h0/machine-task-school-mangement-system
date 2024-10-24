# Generated by Django 5.1.2 on 2024-10-21 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklist',
            name='description',
            field=models.CharField(default='No description available', max_length=50),
        ),
        migrations.AddField(
            model_name='booklist',
            name='image',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booklist',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booklist',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]
