# Generated by Django 4.1.2 on 2022-10-29 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_comment_commenter_alter_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listing_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
    ]
