import sqlite3
import pymorphy2
from wiki_ru_wordnet import WikiWordnet

class SearchSynonyms:
    FILENAME = 'synonyms.txt'

    def __init__(self):
        self.create_connection()
        self.search_synonyms_words()

    def create_connection(self):
        self.connection = sqlite3.connect("C:/Users/T/PycharmProjects/pythonProject/shop.db")
        self.cursor = self.connection.cursor()

    def search_synonyms_words(self):
        self.cursor.execute("SELECT description FROM products")
        descriptions = self.cursor.fetchall()
        descriptions = descriptions

        words = self.split_words(descriptions)
        normalize_words = self.normalize_words(words)
        normalize_unique_words = self.search_unique_words(normalize_words)

        wikiwordnet = WikiWordnet()
        all_synonyms = []
        for word in normalize_unique_words:
            synsets = wikiwordnet.get_synsets(word)
            if len(synsets) != 0:
                synsets = synsets[0]
                synsets = [word.lemma() for word in synsets.get_words()]
                if len(synsets) > 1:
                    synsets.remove(word)
                    synsets = word + ', ' + ', '.join(synsets)
                    all_synonyms.append(synsets)

        self.create_file_with_synonyms(all_synonyms)

    def split_words(self, descriptions):
        all_words = []
        for description in descriptions:
            description = str(description).lower()
            words = description.split()
            words = [word.strip('.,!?:;()[]\'"-~\\/') for word in words]
            all_words += words
        return all_words

    def normalize_words(self, words):
        morph = pymorphy2.MorphAnalyzer()
        normalize_word = [morph.parse(word)[0].normal_form for word in words]
        return normalize_word

    def search_unique_words(self, words):
        unique_words = []

        for word in words:
            if word not in unique_words:
                unique_words.append(word)

        unique_words.sort()
        return unique_words

    def create_file_with_synonyms(self, synonyms):
        with open(self.FILENAME, "w", encoding="utf-8") as file:
            for synonym in synonyms:
                file.write(synonym + "\n")
