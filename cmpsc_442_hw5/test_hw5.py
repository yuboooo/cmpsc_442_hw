from homework5_yfj5098 import *


def test_load_token():
    ham_dir = "homework5_data/train/ham/"
    assert (load_tokens(ham_dir + "ham1")[200:204]) == [
        "of",
        "my",
        "outstanding",
        "mail",
    ]

def test_log_probs():
    paths = ["homework5_data/train/ham/ham%d" % i for i in range(1,11)]
    p = log_probs(paths, 1e-5)
    assert p["the"] == -3.6080194731874062
    assert p["line"] == -4.272995709320345

    paths = ["homework5_data/train/spam/spam%d" % i for i in range(1,11)]
    p = log_probs(paths, 1e-5)
    assert p["Credit"] == -5.837004641921745
    assert p["<UNK>"] == -20.34566288044584

def test_is_spam():
    sf=SpamFilter("homework5_data/train/spam","homework5_data/train/ham",1e-5)
    assert sf.is_spam("homework5_data/train/spam/spam1") == True
    assert sf.is_spam("homework5_data/train/spam/spam2") == True
    assert sf.is_spam("homework5_data/train/ham/ham1") == False
    assert sf.is_spam("homework5_data/train/ham/ham2") == False