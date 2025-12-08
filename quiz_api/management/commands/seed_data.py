from django.core.management.base import BaseCommand
from quiz_api.models import Question, Category, LeaderboardEntry, CATEGORY_CHOICES


class Command(BaseCommand):
    help = 'Seeds the database with initial categories and quiz questions.'

    def handle(self, *args, **options):
        self.stdout.write("--- Seeding Initial Data ---")

        # 1. Seed Categories (Feature 2 Foundation)
        # categories_to_seed = [
        #     'Guess the Verse',
        #     'Who Said This?',
        #     'Old or New Testament',
        # ]
        # for name in categories_to_seed:
        #     Category.objects.get_or_create(name=name)
        # self.stdout.write(self.style.SUCCESS(f'Seeded {len(categories_to_seed)} Categories.'))
        Category.objects.all().delete()
        for code, name in CATEGORY_CHOICES:
            Category.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(CATEGORY_CHOICES)} Categories.'))

        # 2. Seed Questions (Core Data)
        questions_to_seed = [
            # Guess the Verse (GTV)
            {
                'text': '“For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.” Which verse is this?',
                'choices': ['Matthew 5:3', 'John 3:16', 'Romans 8:28', 'Genesis 1:1'],
                'answer': 'John 3:16',
                'category': 'GTV',
                'explanation': 'John 3:16 is often called the Gospel in a nutshell, summing up the core message of Christianity.'
            },
            {
                'text': '“I can do all things through Christ who strengthens me.”',
                'choices': ['Philippians 4:13', 'Psalm 23:1', 'Proverbs 3:5', 'Isaiah 41:10'],
                'answer': 'Philippians 4:13',
                'category': 'GTV',
                'explanation': 'This verse is a statement of faith and reliance on Christ, written by the Apostle Paul.'
            },
            # Who Said This? (WST)
            {
                'text': '“Here I am, send me!”',
                'choices': ['Moses', 'Abraham', 'Isaiah', 'Paul'],
                'answer': 'Isaiah',
                'category': 'WST',
                'explanation': 'The prophet Isaiah spoke this in response to God’s call (Isaiah 6:8).'
            },
            {
                'text': '“Am I my brother’s keeper?”',
                'choices': ['Adam', 'Cain', 'Abel', 'Lamech'],
                'answer': 'Cain',
                'category': 'WST',
                'explanation': 'Cain’s response to God after he had murdered his brother Abel (Genesis 4:9).'
            },
            # Old or New Testament (ONT)
            {
                'text': 'The Book of Exodus',
                'choices': ['Old Testament', 'New Testament'],
                'answer': 'Old Testament',
                'category': 'ONT',
                'explanation': 'Exodus is the second book of the Bible, detailing the Israelites’ escape from Egypt.'
            },
            {
                'text': 'The Sermon on the Mount',
                'choices': ['Old Testament', 'New Testament'],
                'answer': 'New Testament',
                'category': 'ONT',
                'explanation': 'The Sermon on the Mount is recorded in the Gospel of Matthew (chapters 5–7), spoken by Jesus.'
            },
            {
                'text': 'The Book of Revelation',
                'choices': ['Old Testament', 'New Testament'],
                'answer': 'New Testament',
                'category': 'ONT',
                'explanation': 'Revelation is the last book of the Bible, a prophecy about the end times.'
            },
            # Add more for a robust seed bank (total 10 for the MVP)
            {
                'text': 'The story of Jonah and the great fish.',
                'choices': ['Old Testament', 'New Testament'],
                'answer': 'Old Testament',
                'category': 'ONT',
                'explanation': 'The Book of Jonah is a minor prophet book in the Old Testament.'
            },
            {
                'text': '“Faith by itself, if it is not accompanied by action, is dead.”',
                'choices': ['James', 'Peter', 'John', 'Jude'],
                'answer': 'James',
                'category': 'WST',
                'explanation': 'This is from James 2:17, emphasizing the necessity of works to accompany true faith.'
            },
            {
                'text': '“The Lord is my shepherd; I shall not want.”',
                'choices': ['Psalm 23:1', 'Proverbs 1:1', 'Isaiah 6:1', 'John 1:1'],
                'answer': 'Psalm 23:1',
                'category': 'GTV',
                'explanation': 'This is the opening line of the famous Psalm 23, attributed to David.'
            },
        ]

        Question.objects.all().delete()
        for q_data in questions_to_seed:
            Question.objects.create(
                question_text=q_data['text'],
                choices=q_data['choices'],
                correct_answer=q_data['answer'],
                category=q_data['category'],
                explanation=q_data['explanation']
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(questions_to_seed)} Questions.'))
        
        # 3. Seed Leaderboard Entries (Feature 5 Foundation)
        LeaderboardEntry.objects.all().delete()
        LeaderboardEntry.objects.create(name='Top Learner', high_score=100)
        LeaderboardEntry.objects.create(name='Scripture Guru', high_score=95)
        self.stdout.write(self.style.SUCCESS(f'Seeded Leaderboard Entries.'))


# to run:
# py manage.py seed_data