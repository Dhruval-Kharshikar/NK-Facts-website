from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0002_rss_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('icon', models.CharField(default='🎙️', max_length=10)),
                ('keywords', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='podcast',
            name='category_fk',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='podcasts',
                to='podcasts.category'
            ),
        ),
        migrations.RenameField(
            model_name='podcast',
            old_name='category',
            new_name='category_old',
        ),
        migrations.RenameField(
            model_name='podcast',
            old_name='category_fk',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='category_old',
        ),
    ]
