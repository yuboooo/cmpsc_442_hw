from homework6_yfj5098 import load_corpus, Tagger

def test_load_corpus():
    c = load_corpus("brown-corpus.txt")
    # TEST 1
    assert c[1402] == [('It', 'PRON'), ('made', 'VERB'), ('him', 'PRON'), ('human', 'NOUN'), ('.', '.')]
    # TEST 2
    assert c [1799] == [('The', 'DET'), ('prospects', 'NOUN'), ('look', 'VERB'), ('great', 'ADJ'), ('.', '.')]
    # TEST 3
    assert c [0] == [('The', 'DET'), ('Fulton', 'NOUN'), ('County', 'NOUN'), ('Grand', 'ADJ'), ('Jury', 'NOUN'), ('said', 'VERB'), ('Friday', 'NOUN'), ('an', 'DET'), ('investigation', 'NOUN'), ('of', 'ADP'), ("Atlanta's", 'NOUN'), ('recent', 'ADJ'), ('primary', 'NOUN'), ('election', 'NOUN'), ('produced', 'VERB'), ('``', '.'), ('no', 'DET'), ('evidence', 'NOUN'), ("''", '.'), ('that', 'ADP'), ('any', 'DET'), ('irregularities', 'NOUN'), ('took', 'VERB'), ('place', 'NOUN'), ('.', '.')]

def test_most_probable_tags():
    c = load_corpus("brown-corpus.txt")
    t = Tagger(c)
    # TEST 1
    assert t.most_probable_tags(["The", "man", "walks", "."]) == ['DET', 'NOUN', 'VERB', '.']
    # TEST 2
    assert t.most_probable_tags(["The", "blue", "bird", "sings"]) == ['DET', 'ADJ', 'NOUN', 'VERB']

def test_viterbi_tags():
    c = load_corpus("brown-corpus.txt")
    t = Tagger(c)
    # TEST 1
    s = "I am waiting to reply".split()
    assert t.most_probable_tags(s) == ["PRON", "VERB", "VERB", "PRT", "NOUN"]
    assert t.viterbi_tags(s) == ["PRON", "VERB", "VERB", "PRT", "VERB"]
    # TEST 2
    s = "I saw the play".split()
    assert t.most_probable_tags(s) == ["PRON", "VERB", "DET", "VERB"]
    assert t.viterbi_tags(s) == ["PRON", "VERB", "DET", "NOUN"]
    # TEST 3
    s = "I am bla bla, the fastest man alive in the world oh yeah, i saw the play , i am waiting to reply".split()
    assert t.most_probable_tags(s) == ['PRON', 'VERB', 'X', 'X', 'DET', 'ADJ', 'NOUN', 'ADJ', 'ADP', 'DET', 'NOUN', 'PRT', 'X', 'NOUN', 'VERB', 'DET', 'VERB', '.', 'NOUN', 'VERB', 'VERB', 'PRT', 'NOUN']
    assert t.viterbi_tags(s) == ['PRON', 'VERB', 'X', 'X', 'DET', 'ADJ', 'NOUN', 'ADJ', 'ADP', 'DET', 'NOUN', 'PRT', 'X', 'NOUN', 'VERB', 'DET', 'NOUN', '.', 'NOUN', 'VERB', 'VERB', 'PRT', 'VERB']