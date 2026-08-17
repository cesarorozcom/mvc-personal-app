from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MovementImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='queued', max_length=32)),
                ('image_key', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImportedMovementProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('currency', models.CharField(blank=True, default='', max_length=3)),
                ('requires_review', models.BooleanField(default=False)),
                ('is_duplicate', models.BooleanField(default=False)),
                ('duplicate_reason', models.TextField(blank=True, default='')),
                ('confirmed', models.BooleanField(default=False)),
                ('discarded', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movement_import', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='movements.movementimport')),
            ],
        ),
    ]
