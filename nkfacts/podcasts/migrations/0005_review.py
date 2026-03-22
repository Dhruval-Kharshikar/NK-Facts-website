from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0004_seed_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='podcasts.podcast')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
