import pandas as pd
from collections import Counter
import re
import json
import os
from exclude_words import get_exclude_words

class ContentClassifier:
    def __init__(self, df):
        self.df = df.copy()
        self.frequent_words = None
        self.manual_categories = {}

        # Path for saving manual categorizations
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.categories_file = os.path.join(project_root, 'data', 'manual_categories.json')

        # You can modify this list to add or remove categories
        self.available_categories = [
            'Entertainment',
            'Education',
            'History',
            'Architecture',
            'Lifestyle',
            'Tech Reviews',
            'Sports',
            'Music',
            'Movie',
            'Food',
            'Programming',
            'Other'
        ]

    def get_frequent_words(self, min_frequency=75):
        """Extract words that appear more than min_frequency times"""
        # Get exclude words from our module
        exclude_words = get_exclude_words()

        all_words = []
        for title in self.df['title']:
            # Convert to lowercase and remove special characters
            title = str(title).lower()
            title = re.sub(r'[^\w\s]', ' ', title)
            words = title.split()

            # Only include words that are not in exclude_words and are at least 2 characters long
            words = [word for word in words
                     if word not in exclude_words
                     and len(word) > 1
                     and not word.isdigit()]
            all_words.extend(words)

        # Count word frequencies
        word_freq = Counter(all_words)

        # Filter words that appear at least min_frequency times
        self.frequent_words = {word: count for word, count
                               in word_freq.items()
                               if count >= min_frequency}

        # Sort by frequency
        self.frequent_words = dict(sorted(self.frequent_words.items(),
                                          key=lambda x: x[1],
                                          reverse=True))

        # Load any existing manual categories
        self.load_manual_categories()
        return self.frequent_words

    def save_manual_categories(self):
        """Save manual categorizations to a JSON file"""
        os.makedirs(os.path.dirname(self.categories_file), exist_ok=True)
        with open(self.categories_file, 'w') as f:
            json.dump(self.manual_categories, f, indent=2)

    def load_manual_categories(self):
        """Load manual categorizations from JSON file"""
        if os.path.exists(self.categories_file):
            with open(self.categories_file, 'r') as f:
                self.manual_categories = json.load(f)

    def show_available_categories(self):
        """Display available categories"""
        print("\nAvailable categories:")
        for i, category in enumerate(self.available_categories, 1):
            print(f"{i}. {category}")

    def interactive_categorization(self):
        """Interactive process to categorize words"""
        if not self.frequent_words:
            self.get_frequent_words()

        print("\nStarting interactive categorization process...")
        print("Type 'quit' at any time to stop")

        # Show all uncategorized words first
        uncategorized = self.get_uncategorized_words()
        if not uncategorized:
            print("All words have been categorized!")
            return

        print(f"\nYou have {len(uncategorized)} words to categorize.")

        for word in uncategorized:
            count = self.frequent_words[word]
            print(f"\nWord: '{word}' (appears {count} times)")

            # Show available categories
            self.show_available_categories()

            # Get category choice
            while True:
                choice = input("\nEnter category number (or 'quit' to stop): ").strip()

                if choice.lower() == 'quit':
                    return

                try:
                    category_idx = int(choice) - 1
                    if 0 <= category_idx < len(self.available_categories):
                        category = self.available_categories[category_idx]
                        self.add_manual_category(word, category)
                        break
                    else:
                        print("Invalid category number. Please try again.")
                except ValueError:
                    print("Please enter a valid number or 'quit'")

    def add_manual_category(self, word, category):
        """Add or update a manual category for a word"""
        if word not in self.frequent_words:
            print(f"Warning: '{word}' is not in the list of frequent words")
            return False

        self.manual_categories[word] = category
        self.save_manual_categories()
        print(f"Added '{word}' to category '{category}'")
        return True

    def get_uncategorized_words(self):
        """Get list of frequent words that haven't been manually categorized"""
        return [word for word in self.frequent_words.keys()
                if word not in self.manual_categories]

    def show_categorization_status(self):
        """Show current categorization status"""
        print("\nCurrent Categorization Status:")
        print("-" * 40)

        # Group words by category
        categorized = {}
        for word, category in self.manual_categories.items():
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(word)

        # Show words in each category
        for category in self.available_categories:
            words = categorized.get(category, [])
            if words:
                print(f"\n{category} ({len(words)} words):")
                for word in sorted(words):
                    count = self.frequent_words.get(word, 0)
                    print(f"  - {word} ({count} times)")

        # Show uncategorized count
        uncategorized = self.get_uncategorized_words()
        print(f"\nUncategorized words remaining: {len(uncategorized)}")


def main():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        data_path = os.path.join(project_root, 'data', 'raw', 'watch-history.csv')

        print(f"Loading data from: {data_path}")
        df = pd.read_csv(data_path)

        print("Creating classifier instance...")
        classifier = ContentClassifier(df)

        # Start interactive categorization
        classifier.interactive_categorization()

        # Show final status
        classifier.show_categorization_status()

    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()