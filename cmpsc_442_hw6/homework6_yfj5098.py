############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Yubo Jing"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import Counter
from collections import defaultdict


############################################################
# Section 1: Hidden Markov Models
############################################################
def load_corpus(last_tag):
    corpus = []
    for line in open(last_tag, 'r', encoding="utf8"):
        sentence = []
        for token in line.split():
            sentence.append(tuple(token.split("=")))
        corpus.append(sentence)
    return corpus


class Tagger(object):
    def __init__(self, sentences):
        self.tag_set = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 'CONJ', 'PRT', '.', 'X']
        self.pi, self.a, self.b = {}, {}, {}
        word_count, tag_count, init_count, transition_count, emission_count = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
        for line in sentences:
            init_count[line[0][1]] += 1
            for i in range(len(line)):
                emission_count[(line[i][1], line[i][0])] += 1
                tag_count[line[i][1]] += 1
                word_count[line[i][0]] += 1
            for i in range(len(line) - 1):
                transition_count[(line[i][1], line[i + 1][1])] += 1

        word_count["<UNK>"]=[0 for i in range(len(self.tag_set))]

        # index_map = {v: i for i, v in enumerate(tag_set)}
        # init_count = dict(sorted(init_count.items(), key=lambda pair: index_map[pair[0]]))

        # initial tag probabilities pi(ti)
        for tag in init_count:
            init_prob = (init_count[tag] + 1) / (len(sentences) + len(init_count))
            self.pi[tag] = init_prob
        
        # transition probabilities a(ti->tj)
        for (t_i, t_j) in transition_count:
            tr_prob = (transition_count[(t_i, t_j)] + 1) / (tag_count.get(t_i) + len(self.tag_set))
            self.a[(t_i, t_j)] = tr_prob
        
        # emission probabilities b(ti->wj)
        for (t, w) in emission_count:
            em_prob = (emission_count[(t, w)] + 1) / (tag_count.get(t) + len(word_count))
            self.b[(t, w)] = em_prob

        self.a.update({('X', w): 1 / (tag_count.get(t, 0) + len(self.tag_set)) for (t, w) in transition_count.keys()})
        self.b.update({('X', w): 1 / (tag_count.get(t, 0) + len(word_count)) for (t, w) in emission_count.keys()})

    def most_probable_tags(self, tokens):
        ret = []
        for t in tokens:
            temp = []
            for tag in self.tag_set:
                if (tag, t) in self.b.keys():
                    temp.append((self.b.get((tag, t), 0), tag))
                else:
                    temp.append((self.b.get(("X", tag), 0), "X"))
            ret.append(max(temp)[1])
        return ret

    def viterbi_tags(self, tokens):
        V = [{} for i in range(len(tokens))]
        for tag in self.tag_set:
            prob = self.pi.get(tag, 0) * self.b.get((tag, tokens[0]), 0)
            V[0][tag] = prob

        V_tag = [{} for i in range(len(tokens))]

        for t in range(len(tokens) - 1):
            for t_j in self.tag_set:
                max_tr_prob = []
                for t_i in self.tag_set:
                    if t_j == "X":
                        prob_i = V[t][t_i] * self.a.get((t_i, t_j), 0) * self.b.get((t_j, tokens[t + 1]), 1)
                        max_tr_prob.append((prob_i, t_i))
                    else:
                        prob_i = V[t][t_i] * self.a.get((t_i, t_j), 0) * self.b.get((t_j, tokens[t + 1]), 0)
                        max_tr_prob.append((prob_i, t_i))
                (V[t + 1][t_j], V_tag[t + 1][t_j]) = max(max_tr_prob)

        path = []
        last_tag = []
        for tag in self.tag_set:
            temp = (V[-1][tag], tag)
            last_tag.append(temp)
        last_tag = [max(last_tag)[1]]

        prev = last_tag
        path.extend(last_tag)

        for token in range(len(tokens) - 1, 0, -1):
            prev[0] = V_tag[token][prev[0]]
            path.insert(0, prev[0])
        return path



############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
8 hours
"""

feedback_question_2 = """
data structure is hard to track
"""

feedback_question_3 = """
good
"""
