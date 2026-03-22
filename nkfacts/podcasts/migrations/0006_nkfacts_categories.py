from django.db import migrations


NK_FACTS_CATEGORIES = [
    {
        'name': 'Psychology & Human Behavior',
        'slug': 'psychology',
        'icon': '🧠',
        'order': 1,
        'keywords': 'psychology, human behavior, emotions, mind, mental health, fear, happiness, sadness, anxiety, stress, depression, joy, love, relationships, trust, confidence, motivation, imagination, creativity, dreams, memory, learning, thinking, decision making, choices, personality, introvert, extrovert, emotions control, feelings, behavior pattern, neural response, brain function, psychological effect, phobia, trauma, therapy, counseling, mindfulness, meditation, consciousness, awareness, self-esteem, emotional intelligence, empathy, compassion, kindness, gratitude, forgiveness, resilience, coping, adaptation, adjustment, growth, transformation, change, inspiration, positive thinking, optimism, pessimism, attitude, perspective, perception, reality, illusion, manipulation, brainwashing, stress management, panic attack, anxiety disorder, mood, temperament, personality type, behavioral psychology, cognitive psychology, developmental psychology, social psychology, abnormal psychology, organizational behavior, decision theory, reasoning, logic, problem solving, conflict resolution, human nature, social behavior, group dynamics, leadership, motivation theory, learning theory, memory formation, attention, cognitive bias',
    },
    {
        'name': 'Animals & Wildlife',
        'slug': 'animals',
        'icon': '🐾',
        'order': 2,
        'keywords': 'animals, wildlife, creatures, insects, fish, birds, mammals, reptiles, amphibians, snails, species, species identification, endangered, extinct, habitat, ecosystem, nature reserve, safari, jungle, forest, ocean, aquatic, terrestrial, arachnids, spiders, butterflies, beetles, ants, bees, vegetation, flora, fauna, biodiversity, conservation, protection, rare species, unique species, animal behavior, hunting, survival, evolution, adaptation, migration, camouflage, defense mechanism, communication, social structure, family, mating, reproduction, predator, prey, ecosystem balance, food chain, food web, animal species list, bird watching, wildlife photography, animal sanctuary, zoology, ornithology, entomology, marine life, aquatic animals, domestic animals, wild animals, animal classification, animal kingdom, vertebrates, invertebrates, animal sounds, animal communication, ecological role, predator-prey relationship, animal intelligence, animal instinct, pack behavior, shark, owl, chicken, snail, bird, spider, bug, creature, beast, insect',
    },
    {
        'name': 'Science & Natural Phenomena',
        'slug': 'science',
        'icon': '🔬',
        'order': 3,
        'keywords': 'science, physics, chemistry, biology, natural phenomenon, weather, climate, temperature, snow, ice, frost, freeze, water, ocean, sea, nature, ecosystem, environment, climate change, global warming, ice formations, crystals, patterns, frost flowers, arctic, discovery, experiment, research, observation, data, analysis, theory, hypothesis, proof, evidence, explanation, understanding, knowledge, education, investigation, technology, innovation, development, advancement, progress, thermodynamics, energy, force, motion, gravity, light, sound, matter, atom, molecule, element, compound, chemical reaction, physics law, natural law, quantum mechanics, relativity, geophysics, atmospheric science, meteorology, oceanography, seismology, geology, fossil, mineral, rock, plate tectonics, weather system, storm, hurricane, tornado, precipitation, wind, pressure system, plutonium, lazarus, acid, volcano, crater, depression, frozen, arctic',
    },
    {
        'name': 'Health & Medicine',
        'slug': 'health',
        'icon': '💊',
        'order': 4,
        'keywords': 'health, medicine, medical, disease, illness, disorder, symptoms, treatment, cure, therapy, drug, medication, vaccination, immune system, immunity, infection, virus, bacteria, antibody, white blood cell, red blood cell, cell, organ, transplant, donation, blood, heart, brain, lung, kidney, liver, body system, nutrition, diet, exercise, fitness, wellness, wellbeing, mental health, physical health, healthcare, hospital, doctor, nurse, medical professional, medical science, anatomy, physiology, pathology, diagnosis, prognosis, recovery, healing, surgery, surgical, prevention, preventive care, chronic disease, acute disease, autoimmune disease, genetic disease, blood disorder, neurological disease, cardiovascular disease, respiratory disease, digestive disease, mental disorder, brain function, organ function, immune response, healing process, prescription, clinic, emergency room, patient care, physician, medical technology, medical equipment, disease prevention, health screening, medical procedure, medical intervention, killer cells, blood group, jaw, vein, tarsorrhaphy, awake surgery',
    },
    {
        'name': 'Geography & Travel',
        'slug': 'geography',
        'icon': '🌍',
        'order': 5,
        'keywords': 'geography, location, place, country, city, continent, region, landscape, terrain, mountain, valley, river, lake, ocean, beach, island, desert, forest, jungle, cave, waterfall, bridge, monument, landmark, tourist attraction, wonder, natural wonder, man-made wonder, architecture, structure, building, construction, engineering, design, beauty, scenic, view, destination, journey, travel, exploration, adventure, discovery, topography, climate zone, weather pattern, latitude, longitude, coordinates, map, route, path, direction, navigation, tourism, resort, hotel, accommodation, transportation, flight, railway, highway, waterway, road, trail, heritage site, world heritage, geological formation, national park, wildlife reserve, sanctuary, cultural site, archaeological site, historical site, geographic feature, terrain type, geological wonder, mountain range, ocean current, coastal region, inland region, polar region, tropical region, canyon, dead sea, island, library, waterslide, floating road, firefall, yosemite, china, sommaroy',
    },
    {
        'name': 'History & Culture',
        'slug': 'history',
        'icon': '📜',
        'order': 6,
        'keywords': 'history, culture, tradition, custom, festival, celebration, holiday, heritage, legacy, ancient, medieval, modern, civilization, society, people, community, ethnic, nationality, religion, belief, mythology, folklore, story, tale, legend, historical event, war, peace, revolution, independence, freedom, rights, law, justice, ethics, morality, values, human rights, child rights, convention, agreement, treaty, ritual, ceremony, cultural significance, historical significance, background, origin, beginning, evolution, development, transformation, era, epoch, time period, dynasty, empire, kingdom, nation, cultural exchange, cultural diversity, cultural preservation, historical documentation, ancient civilization, medieval period, modern era, renaissance, enlightenment, historical figure, cultural heritage, intangible heritage, cultural artifact, archaeological finding, cultural practice, social norm, belief system, religious tradition, historical monument, preserved heritage, cultural identity, tradition preservation, halloween, left-handed, forbidden, colors, netherlands, game, rights, convention',
    },
    {
        'name': 'Plants & Botanical Science',
        'slug': 'plants',
        'icon': '🌿',
        'order': 7,
        'keywords': 'plants, trees, flowers, herbs, shrubs, vegetation, greenery, botanical, botany, flora, leaf, stem, root, flower, seed, fruit, tree species, plant species, plant identification, flowering plant, non-flowering plant, herbaceous plant, woody plant, tropical plant, temperate plant, desert plant, aquatic plant, terrestrial plant, carnivorous plant, medicinal plant, poisonous plant, edible plant, ornamental plant, endangered plant, extinct plant, plant habitat, plant adaptation, plant reproduction, photosynthesis, plant growth, plant classification, plant kingdom, plant anatomy, plant physiology, plant ecology, plant conservation, native plant, exotic plant, invasive plant, plant disease, plant pest, gardening, horticulture, agriculture, landscape, forest, woodland, botanical garden, herbarium, plant research, plant diversity, plant life cycle, plant structure, plant function, flower structure, seed dispersal, plant nutrition, plant defense, skeleton flower, dynamite tree, poison ivy, poison oak, poison sumac, strangest plants, botanical oddities',
    },
    {
        'name': "Nature's Wonders & Anomalies",
        'slug': 'wonders',
        'icon': '✨',
        'order': 8,
        'keywords': 'wonder, anomaly, mystery, unusual, strange, rare, unique, extraordinary, spectacular, amazing, interesting, incredible, surprising, fascinating, phenomenon, occurrence, event, happening, effect, reaction, result, consequence, cause, reason, explanation, purpose, function, feature, characteristic, property, quality, attribute, trait, natural, artificial, man-made, creation, formation, development, growth, change, transformation, mutation, variation, diversity, variety, difference, similarity, comparison, contrast, unusual behavior, unexpected, astonishing, remarkable, notable, outstanding, exceptional, special, distinct, particular, specific, classified, categorized, identified, recognized, discovered, explored, investigated, studied, analyzed, understood, explained, documented, unexpected discovery, surprising fact, remarkable feature, curious phenomenon, fascinating occurrence, strange behavior, odd characteristic, unusual adaptation, rare sighting, mysterious happening, unexplained phenomenon, natural mystery, scientific wonder, magnificent, overpass, difficult, navigate, frost flower, arctic, frozen, kissing bug',
    },
    {
        'name': 'Miscellaneous & Special Topics',
        'slug': 'miscellaneous',
        'icon': '🎯',
        'order': 9,
        'keywords': 'miscellaneous, special topics, food, cuisine, restaurant, travel guide, adventure, entertainment, statistics, probability, supernatural, ghost, paranormal, mystery, urban legend, facts, trivia, technology, innovation, social impact, accessibility, disability, education, learning, knowledge, skills, hobbies, lifestyle, fashion, trends, internet, social media, communication, language, linguistics, philosophy, ethics, spirituality, religion, science fiction, futurism, future technology, artificial intelligence, automation, robotics, space exploration, astronomy, cosmology, sports, games, recreation, hobby, craft, cooking, nutrition, wellness, self-improvement, personal development, relationship, communication skills, public speaking, writing, storytelling, entertainment value, social phenomenon, cultural trend, viral topic, popular culture, entertainment industry, media, broadcasting, music, cinema, literature, humor, comedy, inspiration, motivation, success stories, human interest, daily life, lifestyle tips, practical knowledge, useful information, everyday facts, surprising trivia, braille, manifestation, barnacles, cheap eats, ghost hunting, world bank',
    },
]


def set_nkfacts_categories(apps, schema_editor):
    Category = apps.get_model('podcasts', 'Category')

    # Delete ALL existing categories cleanly
    Category.objects.all().delete()

    # Insert NK Facts specific categories
    for data in NK_FACTS_CATEGORIES:
        Category.objects.create(**data)


def revert_categories(apps, schema_editor):
    Category = apps.get_model('podcasts', 'Category')
    Category.objects.filter(slug__in=[c['slug'] for c in NK_FACTS_CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0005_review'),
    ]

    operations = [
        migrations.RunPython(set_nkfacts_categories, revert_categories),
    ]