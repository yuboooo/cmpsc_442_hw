############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Yubo Jing"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os
from glob import glob

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):

    words = []
    with open(email_path, "r") as f:
        message = email.message_from_file(f)
    for line in email.iterators.body_line_iterator(message):
        words += line.split()
    return words

def words_dict(email_paths):
    # Count words and store in dictionary
    words_dictionary = {}
    for path in email_paths:
        words = load_tokens(path)
        for word in words:
            if word not in words_dictionary:
                words_dictionary[word] = 1
            else:
                words_dictionary[word] += 1
    return words_dictionary

def log_probs(email_paths, smoothing):

    words_dictionary = words_dict(email_paths)
    probs_dictionary = {}  
    for word, count in words_dictionary.items():
        # P(w) = (count(w) + a) / (sum(count(w')) + a(len(dict)) + 1)
        probs_dictionary[word] = math.log((count + smoothing) / (sum(words_dictionary.values()) + smoothing * ((len(words_dictionary) + 1.0))))
    # P(unknown) = a / (sum(count(w')) + a(len(dict)) + 1) - add a (constant count) to all words to avoid prob = 0
    probs_dictionary["<UNK>"] = math.log((smoothing) / (sum(words_dictionary.values()) + smoothing * ((len(words_dictionary) + 1.0))))

    return probs_dictionary


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_paths = list(map(lambda x: spam_dir + "/" + x, os.listdir(spam_dir)))
        ham_paths = list(map(lambda x: ham_dir + "/" + x, os.listdir(ham_dir)))

        self.spam_prob = len(spam_paths) / (len(spam_paths) + len(ham_paths))
        self.ham_prob = 1 - self.spam_prob

        self.spam_dict = log_probs(spam_paths, smoothing)
        self.ham_dict = log_probs(ham_paths, smoothing)   
    
    def is_spam(self, email_path):

        word_dictionary = words_dict([email_path])
        spam_score = math.log(self.spam_prob)
        ham_score = math.log(self.ham_prob)
        for word in word_dictionary:
            spam_score += self.spam_dict[word] if word in self.spam_dict else self.spam_dict["<UNK>"]
            ham_score += self.ham_dict[word] if word in self.ham_dict else self.ham_dict["<UNK>"]
        return spam_score > ham_score

    def most_indicative(self, n, type):

        indication = []
        if type == "spam":
            x = self.ham_dict
            y = self.spam_dict
        elif type == "ham":
            x = self.spam_dict
            y = self.ham_dict
        for word, score in x.items():
            if word in y:
                # e^x + e^y
                lnxy = math.exp(1) ** x[word] + math.exp(1) ** y[word]
            else:
                lnxy = math.exp(1) ** x[word] + math.exp(1) ** y["<UNK>"]
            indication.append((word, score - math.log(lnxy)))
        return list(map(lambda x: x[0], sorted(indication, key=lambda x: x[1], reverse=False)))[:n]

    def most_indicative_spam(self, n):

        return self.most_indicative(n, "spam")

    def most_indicative_ham(self, n):

        return self.most_indicative(n, "ham")


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
5.0
"""

feedback_question_2 = """
indicative score is hard.
"""

feedback_question_3 = """
good
"""
