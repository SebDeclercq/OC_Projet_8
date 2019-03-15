# Generated by Django 2.1.7 on 2019-03-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='category name')),
            ],
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name', 'nutrition_grade'), 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterField(
            model_name='product',
            name='nutrition_grade',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1, verbose_name='nutrition grade'),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(unique=True, verbose_name='url'),
        ),
    ]