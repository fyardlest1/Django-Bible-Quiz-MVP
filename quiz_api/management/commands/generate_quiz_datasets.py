
import os
from django.conf import settings
from django.core.management.base import BaseCommand

# Import the conversion functions
# Ensure bible_dataset has an __init__.py file to be importable
from bible_dataset.dataset_conversion_gtv import create_bible_quiz_seed
from bible_dataset.dataset_conversion_ont import create_ont_quiz_seed

class Command(BaseCommand):
    help = 'Generates python data files (gtv_quiz_data.py and ont_quiz_data.py) from UKJV.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Number of questions to generate per category'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='If set, generates questions for ALL available data (ignores limit)'
        )
        

    def handle(self, *args, **options):
        # 1. Setup Paths
        # Update: Pointing to bible_dataset folder for the input file
        input_file = os.path.join(settings.BASE_DIR, 'bible_dataset', 'UKJV.json')
        
        # Output files will still go to the project Root so your seed_db command can find them easily
        gtv_output = os.path.join(settings.BASE_DIR, 'bible_dataset/gtv_quiz_data.py')
        ont_output = os.path.join(settings.BASE_DIR, 'bible_dataset/ont_quiz_data.py')

        # 2. Determine Limit
        limit = options['limit']
        if options['all']:
            limit = None 

        self.stdout.write(f"--- Looking for source data at: {input_file} ---")
        
        if not os.path.exists(input_file):
            self.stdout.write(self.style.ERROR(f"✘ Error: Could not find file at {input_file}"))
            return

        # 3. Run GTV Generation
        self.stdout.write("Generating Guess The Verse (GTV) data...")
        try:
            create_bible_quiz_seed(input_file, gtv_output, limit=limit)
            self.stdout.write(self.style.SUCCESS(f"✔ Created {gtv_output}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✘ Error generating GTV: {e}"))

        # 4. Run ONT Generation
        self.stdout.write("Generating Old vs New Testament (ONT) data...")
        try:
            create_ont_quiz_seed(input_file, ont_output, limit=limit)
            self.stdout.write(self.style.SUCCESS(f"✔ Created {ont_output}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✘ Error generating ONT: {e}"))


# to run:
# Generate 50 questions (default)
# python manage.py generate_quiz_datasets

# Generate 200 questions
# python manage.py generate_quiz_datasets --limit 200

# Generate EVERYTHING (Warning: Large file):
# python manage.py generate_quiz_datasets --all
