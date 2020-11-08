import spacy 
from textblob import TextBlob #Textblob is used for creating bigrams and trigrams
import numpy
import re

# Spacy needs a model for finding named entities
nlp = spacy.load("en_core_web_sm")

class NERSummarizer():

    def __init__(self):
        pass

    #Printing named entities from the given document
    def list_named_entities(self, document_text):
        doc = nlp(document_text)
        #Create an array for named entities with ORG or PERSON label and populate it
        entity_list = []
        for ent in doc.ents:
            if ent.label_ == "ORG" or ent.label_ == "PERSON":
                entity_list.append(ent.text)
        return entity_list

    def original_text_sentences(self, original_text):
        textblob = TextBlob(original_text)
        sentence_list = []
        for sentence in textblob.sentences:
            sentence_list.append(sentence)
        return sentence_list

    def sentence_named_entities(self, sentence_text, named_entity):
        times_found = len(re.findall(named_entity, str(sentence_text)))
        return times_found

    def NER_scoring_for_sentence(self, sentence, NE_list):
        NER_score = 0
        for NE in NE_list:
            NER_score = NER_score + self.sentence_named_entities(sentence, NE)
        return NER_score

    def NER_scoring(self, sentence_list,NE_list):
        NER_scores = []
        for sentence in sentence_list:
            NER_scores.append(self.NER_scoring_for_sentence(sentence,NE_list))
        return NER_scores

    def highest_NER_scores(self, score_list, score_amount):
        s = numpy.array(score_list)
        #Sort the score list by highest score in descending order and store the index in a list
        sorted_index_list = numpy.argsort(s)[::-1]
        return_list = []
        #Return the amount that's asked in the score_amount
        if score_amount > len(sorted_index_list):
            score_amount = len(sorted_index_list)
        for i in range(0,score_amount):
            return_list.append(sorted_index_list[i])
        return return_list

    def NER_summary(self, sentence_list,score_list):
        #Sort the highest scored sentences to the original order as they appear in the article
        sorted_score_list = numpy.sort(score_list)
        NER_summary = []
        for i in sorted_score_list:
            NER_summary.append(str(sentence_list[i]))
        return NER_summary

    def Named_Entity_Summary(self, article, length):
        sentences = self.original_text_sentences(article)
        sentence_score_list = self.NER_scoring(sentences, self.list_named_entities(article))
        summary = self.NER_summary(sentences, self.highest_NER_scores(sentence_score_list, length))
        return summary
