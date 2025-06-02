import nltk

GOPHER_ERROR = ['few_words', 'many_words', 'short_words', 'long_words', 'ellipsis', 'few_alpha' ]

def at_least_one_alpha(word):
    for char in word:
        if char.isalpha():
            return True
    return False

def gopher_quality_filter(text):
    words = nltk.word_tokenize(text)
    if len(words) < 50:
        return 'few_words'
    if len(words) > 100_000:
        return 'many_words'
    mean_word_length = sum(len(word) for word in words) / len(words)
    if mean_word_length < 3:
        return 'short_words'
    if mean_word_length > 10:
        return 'long_words'
    lines = text.split("\n")
    ellipsis_lines = [line for line in lines if line.endswith("...")]
    if len(ellipsis_lines) / len(lines) > 0.3:
        return 'ellipsis'
    alpha_words = [word for word in words if at_least_one_alpha(word)]
    if len(alpha_words) / len(words) < 0.8:
        return 'few_alpha'
    return 'ok'

def calculate_gopher(examples):
    examples['gopher_verdict'] = []
    for t in examples['text']:
        examples['gopher_verdict'].append(gopher_filter.gopher_quality_filter(t))
    return examples