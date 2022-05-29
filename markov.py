import io

import markovify


def train(file: io.TextIOWrapper):
    markov_text = markovify.NewlineText(file, state_size=1)
    return markov_text


def generate(markov_text: markovify.Text):
    markov_message = markov_text.make_short_sentence(500, 5, test_output=False, tries=100)
    if markov_message is None:
        return None
    else:
        return markov_message


def markov_message_gen(file: io.TextIOWrapper):
    return generate(train(file))
