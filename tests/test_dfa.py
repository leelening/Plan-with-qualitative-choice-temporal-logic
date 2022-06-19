from dfa import examples


def test_dfa_1():
    for example in dir(examples):
        if example.startswith("DFA_"):
            dfa = getattr(examples, example)
            dfa.validate()
