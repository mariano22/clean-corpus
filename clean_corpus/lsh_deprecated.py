import mmh3
import itertools

def get_min_hash_sig(set_of_n_grams, num_hashes):
    """Returns min-hash signature of set of n-grams."""
    min_hash_sig = []
    for i in range(num_hashes):
        min_hash = None
        for n_gram in set_of_n_grams:
            hash_ = mmh3.hash(n_gram, i)
            if min_hash is None or hash_ < min_hash:
                min_hash = hash_
        min_hash_sig.append(min_hash)
    return min_hash_sig

num_hashes=128
num_bands=16
num_words_n_gram=3
jaccard_threshold=0.7

assert num_hashes % num_bands == 0
band_size = num_hashes // num_bands
band_wise_bucket_dict = [defaultdict(list) for _ in range(num_bands)]
for idx,text in enumerate(data):
    text = normalize_for_hashing(text)
    n_gram_set = get_n_gram_set(text, num_words_n_gram)
    min_hash_sig = get_min_hash_sig(n_gram_set, num_hashes)

    for band_idx in range(num_bands):
        hash_beg_idx = band_idx * band_size
        hash_end_idx = (band_idx + 1) * band_size
        key = tuple(min_hash_sig[hash_beg_idx:hash_end_idx])
        band_wise_bucket_dict[band_idx][key].append(idx)

candidate_pairs = set()
for bucket_dict in band_wise_bucket_dict:
    for bucket in bucket_dict.values():
        if len(bucket) == 1:
            continue
        for pair in itertools.combinations(bucket, 2):
            candidate_pairs.add(pair)

if jaccard_threshold is None:
    jaccard_threshold = (1 / num_bands) ** (1 / band_size)

similar_pairs = []
for pair in candidate_pairs:
    ngram_sets = []
    for i in range(2):
        idx = pair[i]
        text = normalize_for_hashing(data[idx])
        ngram_set = get_n_gram_set(text, num_words_n_gram)
        ngram_sets.append(ngram_set)
    
    sim = jaccard_similarity(ngram_sets[0], ngram_sets[1])
    print(sim)
    if sim > jaccard_threshold:
        similar_pairs.append(pair)