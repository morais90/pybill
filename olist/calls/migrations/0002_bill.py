# Generated by Django 2.2.2 on 2019-06-15 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('end_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_record_bill', to='calls.CallRecord')),
                ('start_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_record_bill', to='calls.CallRecord')),
            ],
        ),
    ]
