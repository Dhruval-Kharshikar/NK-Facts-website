from django.db import migrations


DEFAULT_CATEGORIES = [
    {
        'name': 'Nature',
        'slug': 'nature',
        'icon': '🌿',
        'order': 1,
        'keywords': 'nature, animal, plant, forest, ocean, river, mountain, wildlife, bird, fish, insect, flower, tree, jungle, desert, ecosystem, environment, climate, weather, earth, coral, reef, wolf, lion, tiger, whale, migration, habitat, species, predator, prey',
    },
    {
        'name': 'Science',
        'slug': 'science',
        'icon': '🔬',
        'order': 2,
        'keywords': 'science, biology, chemistry, physics, experiment, laboratory, dna, evolution, atom, molecule, quantum, gravity, theory, research, discovery, fossil, cell, bacteria, virus, vaccine, gene, element',
    },
    {
        'name': 'History',
        'slug': 'history',
        'icon': '📜',
        'order': 3,
        'keywords': 'history, ancient, war, empire, kingdom, civilization, pharaoh, roman, greek, medieval, revolution, dynasty, century, historical, artifact, archaeology, mythology, legend, battle, king, queen, emperor, pyramid',
    },
    {
        'name': 'Technology',
        'slug': 'technology',
        'icon': '💻',
        'order': 4,
        'keywords': 'technology, tech, computer, robot, ai, artificial intelligence, internet, software, coding, programming, machine learning, invention, engineer, digital, innovation, app, gadget, electric, device, algorithm, data, cyber',
    },
    {
        'name': 'Health & Wellness',
        'slug': 'health',
        'icon': '💚',
        'order': 5,
        'keywords': 'health, wellness, medicine, brain, body, mental health, exercise, nutrition, diet, sleep, stress, heart, disease, cure, therapy, doctor, medical, immune, fitness, yoga, mindfulness, cancer, pain',
    },
    {
        'name': 'Culture',
        'slug': 'culture',
        'icon': '🎭',
        'order': 6,
        'keywords': 'culture, art, music, language, tradition, festival, food, cuisine, society, religion, belief, ritual, tribe, custom, dance, literature, poetry, film, story, folklore, myth, heritage, human',
    },
    {
        'name': 'Mystery',
        'slug': 'mystery',
        'icon': '🔮',
        'order': 7,
        'keywords': 'mystery, unsolved, strange, weird, unexplained, conspiracy, paranormal, ghost, secret, hidden, forbidden, curse, haunted, disappear, ufo, alien, cryptid, bermuda, cold case, phenomenon, supernatural',
    },
    {
        'name': 'Space',
        'slug': 'space',
        'icon': '🌌',
        'order': 8,
        'keywords': 'space, galaxy, universe, planet, star, nasa, cosmos, asteroid, comet, black hole, solar system, astronaut, orbit, telescope, mars, moon, satellite, nebula',
    },
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model('podcasts', 'Category')
    for data in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(slug=data['slug'], defaults=data)


def remove_categories(apps, schema_editor):
    Category = apps.get_model('podcasts', 'Category')
    Category.objects.filter(slug__in=[c['slug'] for c in DEFAULT_CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0003_category_model'),
    ]

    operations = [
        migrations.RunPython(seed_categories, remove_categories),
    ]
