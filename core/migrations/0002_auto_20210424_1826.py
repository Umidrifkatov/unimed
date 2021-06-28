# Generated by Django 3.1.7 on 2021-04-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brochure',
            field=models.FileField(blank=True, null=True, upload_to='product_brochures', verbose_name='Брошюра'),
        ),
        migrations.AlterField(
            model_name='product',
            name='commercial_proposal_file',
            field=models.FileField(blank=True, null=True, upload_to='commercial_proposals', verbose_name='Файл КП'),
        ),
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True, verbose_name='Общее описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, verbose_name='Короткое описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='standard_of_equipment',
            field=models.FileField(blank=True, null=True, upload_to='product_standards_of_equipment', verbose_name='Стандарт оснащения'),
        ),
    ]
