import argparse

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#from app import APP_ROOT


class Summarizer:
    # __file__ refers to the file settings.py

    def getsummary(self,content):
        """ Drive the process from argument to output """
        #args = self.parse_arguments()

        #content = self.read_file(args.filepath)
        #print(content)
        #content = self.sanitize_input("Prateek test")
        #content = self.read_file(filepath)
        sentence_tokens, word_tokens = self.tokenize_content(content)
        #self.extract_actions(sentence_tokens)
        sentence_ranks = self.score_tokens(word_tokens, sentence_tokens)

        return self.summarize(sentence_ranks, sentence_tokens, 4)

    def parse_arguments(self):
        """ Parse command line arguments """
        parser = argparse.ArgumentParser()
        parser.add_argument('filepath', help='File name of text to summarize')
        parser.add_argument('-l', '--length', default=4, help='Number of sentences to return')
        args = parser.parse_args()

        return args

    def extract_actions(self,sentence_tokens):
        ret_val =[]
        action_choices = ["action item", "take note" , "actionable item" , "take offline"]
        for action in action_choices:
            sentences = process.extract(action,sentence_tokens,limit=10)
            for sentence in sentences:
                if sentence[1] > 85:
                    ret_val.append(sentence[0])
        print(list(set(ret_val)))
        return list(set(ret_val))



    def read_file(self, path):
        """ Read the file at designated path and throw exception if unable to do so """
        try:
            with open(path, 'r+') as file:
                return file.read()

        except IOError as e:
            print("Fatal Error: File ({}) could not be locaeted or is not readable.".format(path))

    def sanitize_input(self, data):
        """
        Currently just a whitespace remover. More thought will have to be given with how
        to handle sanitzation and encoding in a way that most text files can be successfully
        parsed
        """
        print("Data:::::::::,", data)
        replace = {
            ord('\f') : ' ',
            ord('\t') : ' ',
            ord('\n') : ' ',
            ord('\r') : None
        }

        return data.translate(replace)

    def tokenize_content(self,content):
        """
        Accept the content and produce a list of tokenized sentences,
        a list of tokenized words, and then a list of the tokenized words
        with stop words built from NLTK corpus and Python string class filtred out.
        """
        stop_words = set(stopwords.words('english') + list(punctuation))
        words = word_tokenize(content.lower())

        return [
            sent_tokenize(content),
            [word for word in words if word not in stop_words]
        ]

    def score_tokens(self,filterd_words, sentence_tokens):
        """
        Builds a frequency map based on the filtered list of words and
        uses this to produce a map of each sentence and its total score
        """
        word_freq = FreqDist(filterd_words)

        ranking = defaultdict(int)

        for i, sentence in enumerate(sentence_tokens):
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    ranking[i] += word_freq[word]

        return ranking

    def summarize(self,ranks, sentences, length):
        """
        Utilizes a ranking map produced by score_token to extract
        the highest ranking sentences in order after converting from
        array to string.
        """
        if int(length) > len(sentences):
            print("Error, more sentences requested than available. Use --l (--length) flag to adjust.")
            exit()

        indexes = nlargest(length, ranks, key=ranks.get)
        final_sentences = [sentences[j] for j in sorted(indexes)]
        return ' '.join(final_sentences)
