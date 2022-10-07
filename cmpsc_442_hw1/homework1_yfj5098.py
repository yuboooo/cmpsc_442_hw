############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Yubo Jing"

############################################################
# Section 1: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [x for tup in seqs for x in tup]

def transpose(matrix):
    return list(map(list,zip(*matrix)))

############################################################
# Section 2: Sequence Slicing
############################################################

def copy(seq):
    return seq[0:]

def all_but_last(seq):
    return seq[0:-1]

def every_other(seq):
    return seq[0::2]

############################################################
# Section 3: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[0:i]

def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]

def slices(seq):
    for i in range(len(seq)):
        for j in range(i + 1, len(seq) + 1):
            yield seq[i:j]

############################################################
# Section 4: Text Processing
############################################################

def normalize(text):
    return text.lower().strip()

def no_vowels(text):
    vowels = "aeiouAEIOU"
    return ''.join([l for l in text if l not in vowels])

def digits_to_words(text):
    digit = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    result = [f"{digit[char]}" for char in text if char in digit]
    return " ".join(result)

def to_mixed_case(name):
    ans = ""
    for i in name:
        if i == "_":
            ans += " "
        else:
            ans += i
    ans = ans.title().split()
    return f"{ans[0].lower()}{''.join(ans[1:])}"

############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        return Polynomial([(-i[0], i[1]) for i in self.polynomial])
        
    def __add__(self, other):
        add = [i for i in self.polynomial]
        add.extend(i for i in other.polynomial)
        return Polynomial(add)

    def __sub__(self, other):
        sub = [i for i in self.polynomial]
        sub.extend((-i[0], i[1]) for i in other.polynomial)
        return Polynomial(sub)

    def __mul__(self, other):
        return Polynomial([(i[0] * j[0], i[1] + j[1]) for i in self.polynomial for j in other.polynomial])

    def __call__(self, x):
        return sum(i[0] * (x ** i[1]) for i in self.polynomial)

    def simplify(self):
        simplify = {}
        for i in self.polynomial:
            if i[1] not in simplify:
                simplify[i[1]] = i[0]
            else:
                simplify[i[1]] += i[0]
        lst = [(v,k) for k,v in simplify.items() if v != 0]
        if len(lst) == 0:
            self.polynomial = ((0, 0),)
        else:
            self.polynomial = tuple(sorted(lst, key = lambda x:x[1], reverse=True))


    def __str__(self):
        string = ""
        for i in self.polynomial:
            const = "" if i[0] == 1 or i[0] == -1 else abs(i[0])
            sign = '+' if i[0] >= 0 else '-'
            if i[1] == 0:
                string += f" {sign} {abs(i[0])}"
            elif i[1] == 1:
                string += f" {sign} {const}x"
            else:
                string += f" {sign} {const}x^{i[1]}"
        return string[3:] if string[1] == "+" else string[1]+string[3:]

############################################################
# Section 6: Feedback
############################################################

feedback_question_1 = """2.0"""

feedback_question_2 = "Problem 5, spend some time on trying to figure out __str__"

feedback_question_3 = "It makes me get more familiar with list comprehension and make me review some concepts of OOP(Class)"
