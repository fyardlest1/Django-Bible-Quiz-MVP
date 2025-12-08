import json
import random

def create_ont_quiz_seed(input_file, output_file='ont_quiz_data.py', limit=50):
    """
    Reads the UKJV.json file and converts it into Old vs New Testament (ONT) questions.
    
    Args:
        input_file (str): Path to UKJV.json.
        output_file (str): Path to save the output.
        limit (int or None): Max number of questions. If None, returns all Book questions + Event questions.
                            If limit > 70, generic verse questions are added to fill the quota.
    """
    
    NEW_TESTAMENT_BOOKS = {
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', 
        '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', 
        '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 
        'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', 
        '2 John', '3 John', 'Jude', 'Revelation'
    }

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    questions_pool = []
    
    # --- 1. Generate "Book of..." Questions (66 Items) ---
    books_data = data.get('books', [])
    for book in books_data:
        book_name = book['name']
        is_nt = book_name in NEW_TESTAMENT_BOOKS
        testament = 'New Testament' if is_nt else 'Old Testament'
        count = '27' if is_nt else '39'
        
        questions_pool.append({
            'text': f'The Book of {book_name}',
            'choices': ['Old Testament', 'New Testament'],
            'answer': testament,
            'category': 'ONT',
            'explanation': f'The book of {book_name} is one of the {count} books of the {testament}.'
        })

    # --- 2. Add Special "Event" Questions (Hardcoded Variety) ---
    event_questions = [
        {'text': 'The Sermon on the Mount', 'answer': 'New Testament', 'explanation': 'Found in Matthew 5-7.'},
        {'text': 'The story of Noah’s Ark', 'answer': 'Old Testament', 'explanation': 'Found in Genesis 6-9.'},
        {'text': 'The parting of the Red Sea', 'answer': 'Old Testament', 'explanation': 'Found in Exodus 14.'},
        {'text': 'The Day of Pentecost', 'answer': 'New Testament', 'explanation': 'Found in Acts 2.'}
    ]
    
    for eq in event_questions:
        questions_pool.append({
            'text': eq['text'],
            'choices': ['Old Testament', 'New Testament'],
            'answer': eq['answer'],
            'category': 'ONT',
            'explanation': eq['explanation']
        })

    # --- 3. Fill remaining quota with "Verse" Questions ---
    # If the limit requested is higher than what we have (approx 70), 
    # we pull actual verses from the JSON to create more ONT questions.
    
    if limit and limit > len(questions_pool):
        needed = limit - len(questions_pool)
        
        # Flatten all verses
        all_verses = []
        for book in books_data:
            b_name = book['name']
            is_nt = b_name in NEW_TESTAMENT_BOOKS
            t_ment = 'New Testament' if is_nt else 'Old Testament'
            
            for chapter in book['chapters']:
                for verse in chapter['verses']:
                    # Filter out very short/metadata verses if necessary
                    if len(verse['text']) > 20: 
                        all_verses.append({
                            'text': verse['text'].strip(),
                            'book': b_name,
                            'answer': t_ment
                        })
        
        # Randomly select the needed amount
        if needed > len(all_verses):
            selected_verses = all_verses # Take all if not enough
        else:
            selected_verses = random.sample(all_verses, needed)
            
        for v in selected_verses:
            questions_pool.append({
                'text': f'“{v["text"]}”',
                'choices': ['Old Testament', 'New Testament'],
                'answer': v['answer'],
                'category': 'ONT',
                'explanation': f'This verse is found in {v["book"]}, which is in the {v["answer"]}.'
            })

    # --- 4. Finalize List ---
    # Shuffle and trim to exact limit
    random.shuffle(questions_pool)
    
    if limit:
        questions_pool = questions_pool[:limit]

    # Save
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("ont_questions_to_seed = " + json.dumps(questions_pool, indent=4))
        
    print(f"Generated {len(questions_pool)} ONT questions in '{output_file}' (Limit: {limit})")

# Example Usage:
# create_ont_quiz_seed('UKJV.json', 'ont_quiz_data.py', limit=30)
# create_ont_quiz_seed('UKJV.json', 'ont_quiz_data.py', limit=None)