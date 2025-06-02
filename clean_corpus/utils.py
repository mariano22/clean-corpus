import os
import json
from tqdm import tqdm
import tiktoken
from collections import Counter
import random
from dataclasses import dataclass
from urllib.parse import urlparse
import unicodedata
import re
from datasketch import MinHash

def site(x):
    return urlparse(x['url']).netloc

PRINT_KEYS = ['en_proba','erased_mail','erased_phone','gopher_verdict']

def pprint(x, body_field='text', **kwargs):
    print(f"SITE: {site(x)}", **kwargs)
    print(f"URL: {x['url']}", **kwargs)
    for key in PRINT_KEYS:
        if key in x:
            print(f"{key.upper()}: {x[key]}", **kwargs)
    print(x[body_field], **kwargs)
    print('==========================', **kwargs)

@dataclass
class DSConfig:
    path: str
    pickup_p: float = 1

# Set for reproducibility
RANDOM_SEED = 22

FIELDS = ['text', 'url']

DSS = {
    'small': DSConfig(path='../data/webz_2008_01-2013_12', pickup_p=1),
    'big-5p': DSConfig(path='../data/webz_2022_01-2023_10', pickup_p=0.05),
    'big': DSConfig(path='../data/webz_2022_01-2023_10', pickup_p=1),
}

def get_all_filenames(path):
    paths = []
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            paths.append(os.path.join(path, filename))
    return paths

def load(line):
    d = json.loads(line)
    return { k: d[k] for k in FIELDS } 

def get_data_f(file, ds_config):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if ds_config.pickup_p == 1:
                yield load(line)
            elif random.uniform(0, 1) < ds_config.pickup_p:
                yield load(line)
    
def get_data_fs(fs, ds_config):
    random.seed(RANDOM_SEED)
    if ds_config.pickup_p == 1:
        print('Picking all')
    else:
        print(f'Picking only {ds_config.pickup_p*100}%')
    for p in tqdm(fs):
        yield from get_data_f(p,ds_config)

def load_ds(ds_name):
    ds_config = DSS[ds_name]
    fs = get_all_filenames(ds_config.path)
    yield from get_data_fs(fs, ds_config)
    

def join_lines(text):
    return ''.join(text.split('\n'))

def normalize_for_hashing(text):
    text = text.replace('<SEP>', ' ')
    text = text.replace('<PAD>', '')
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.strip()
    text = text.lower()
    return text

def jaccard_sets(t):
    t = normalize_for_hashing(t)
    n_gram_set = get_n_gram_set(t, num_words_n_gram=3)
    return n_gram_set

def jaccard_texts(t1,t2):
    s1 = jaccard_sets(t1)
    s2 = jaccard_sets(t2)
    return jaccard_similarity(s1,s2)

def get_n_gram_set(text, num_words_n_gram):
    words = text.split()
    out = set()
    for i in range(len(words) - num_words_n_gram + 1):
        n_gram = " ".join(words[i : i + num_words_n_gram])
        out.add(n_gram)
    return out

def create_minhash(normalized_text, num_perm, num_words_n_gram):
    m = MinHash(num_perm=num_perm)
    ngrams_set = get_n_gram_set(normalized_text, num_words_n_gram)
    for ngram in ngrams_set:
        m.update(ngram.encode('utf8'))
    return 

def jaccard_similarity(set1, set2):
    """Jaccard similarity of two sets."""
    return len(set1 & set2) / len(set1 | set2)