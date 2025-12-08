"""
Since the Bible contains over 31,000 verses, converting the entire file into a single list would result in a massive dataset. 
The script below includes a limit parameter to generate a sample (e.g., 50 questions) or process the whole book if set to None. 
It primarily generates "Guess the Verse" (GTV) questions using the text provided in your file.
"""

import json
import random

def create_bible_quiz_seed(input_file, output_file, limit=50):
    """
    Reads the UKJV.json file and converts it into a questions_to_seed list.
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions_to_seed = []
    
    # 1. Flatten all verses to make selecting distractors (wrong answers) easier
    all_verses_flat = []
    for book in data['books']:
        book_name = book['name']
        for chapter in book['chapters']:
            ch_num = chapter['chapter']
            for verse in chapter['verses']:
                verse_ref = f"{book_name} {ch_num}:{verse['verse']}"
                verse_text = verse['text'].strip()
                all_verses_flat.append({
                    'ref': verse_ref,
                    'text': verse_text,
                    'book': book_name
                })

    # 2. Generate Questions
    # If limit is set, we shuffle the whole bible and pick 'limit' verses. 
    # If limit is None, we iterate through order.
    
    target_verses = all_verses_flat[:]
    if limit:
        random.shuffle(target_verses)
        target_verses = target_verses[:limit]

    for item in target_verses:
        correct_ref = item['ref']
        text_content = item['text']
        
        # Generate 3 unique distractors
        choices = [correct_ref]
        while len(choices) < 4:
            distractor = random.choice(all_verses_flat)['ref']
            # Ensure unique and not the correct answer
            if distractor not in choices:
                choices.append(distractor)
        
        random.shuffle(choices)

        # Build the question object
        q = {
            'text': f'“{text_content}”',
            'choices': choices,
            'answer': correct_ref,
            'category': 'GTV',
            # Generic explanation since the source file does not contain commentary
            'explanation': f'This verse is found in the book of {item["book"]}.'
        }
        questions_to_seed.append(q)

    # 3. Save or Print
    # Saving to a .py file so it can be imported directly as python code
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("gtv_questions_to_seed = " + json.dumps(questions_to_seed, indent=4))
        
    print(f"Successfully created {len(questions_to_seed)} questions in {output_file}")

# Example Usage:
# create_bible_quiz_seed('UKJV.json', 'gtv_quiz_data.py', limit=30)
# create_bible_quiz_seed('UKJV.json', 'gtv_quiz_data.py', limit=None)


