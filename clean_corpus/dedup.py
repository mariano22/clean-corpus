from collections import defaultdict
import unicodedata
import re

from utils import normalize_for_hashing

def apply_normalization(examples, text_field='text', sentences_field = 'sentences', sentences_normalized_field='sentences_normalized'):
    sts = []
    sts_norm = []
    for text in examples[text_field]:
        sentences_norm = []
        sentences = sent_tokenize(text)
        for s in sentences:
            s = normalize_for_hashing(s)
            sentences_norm.append(s)
        sts_norm.append(sentences_norm)
        sts.append(sentences)
    examples[sentences_field]=sts
    examples[sentences_normalized_field]=sts_norm
    return examples

def join_3gram(sts):
    return '<SEP>'.join(sts)
    
def generate_3grams_sentences_groups(sts):
    n = len(sts)
    n_padding = ( 3 - n%3 ) % 3
    for _ in range(n_padding):
        sts.append('<PAD>')
    grouped_sentences = []
    for i in range(0,n,3):
        grouped_sentences.append(sts[i:i+3])
    for _ in range(n_padding):
        sts.pop()
    return grouped_sentences

global_sentence_count = None
def calculate_sentence_count():
    global sentence_count
    assert global_sentence_count is None
    global_sentence_count = defaultdict(int)
    for x in tqdm(ds):
        sts_grouped = generate_3grams_sentences_groups(x['sentences_normalized'])
        for sts_group in sts_grouped:
            global_sentence_count[join_3gram(sts_group)]+=1

def erase_duplicates(examples):
    assert len(global_sentence_count)>0
    dedup_texts = []
    erased_dedups = []
    diffs = []
    for text, sts, nsts in zip(examples['text'], examples['sentences'], examples['sentences_normalized']):
        dedup_text = text
        diff = text
        n_padding = ( 3 - len(nsts)%3 ) % 3
        sts_grouped = generate_3grams_sentences_groups(nsts)
        erased_sentences = []
        i = 0
        for sts_group in sts_grouped:
            three_sentences = join_3gram(sts_group)
            if global_sentence_count[three_sentences]>2:
                erased = sts[i:min(len(sts),i+3)]
                erased_sentences.append('>>'+''.join(erased))
                for sentence in erased:
                    assert sentence in dedup_text
                    dedup_text=dedup_text.replace(sentence,'')
                    diff=diff.replace(sentence,f'ERASED_BY_DEDUP<|{sentence}]|>')
            i += 3
        dedup_texts.append(dedup_text)
        diffs.append(diff)
        erased_dedups.append('\n'.join(erased_sentences))
    examples['dedup_text']=dedup_texts
    examples['erased_dedup']=erased_dedups
    examples['dedup_diff']=diffs
    return examples

def erase_duplicates_fuzzy(examples):
    global already_print
    assert len(adj)>0
    new_texts = []
    erased_dedups = []
    diffs = []
    iter_fields = zip(examples['id'], examples['dedup_text'], examples['dedup_sentences'], examples['dedup_sentences_normalized'])
    for entry_id, text, sts, nsts in iter_fields:
        new_text = text
        diff_text = text
        sts_grouped = generate_3grams_sentences_groups(nsts)
        erased_sentences = []
        i = 0
        for sts_id, sts_group in enumerate(sts_grouped):
            sts_key = str(entry_id)+'-'+str(sts_id)
            three_sentences = join_3gram(sts_group)
            if is_repated(sts_key):
                erased = sts[i:min(len(sts),i+3)]
                erased_sentences.append('>>'+''.join(erased))
                for sentence in erased:
                    new_text=new_text.replace(sentence,'')
                    diff_text=diff_text.replace(sentence,f'ERASED_BY_DEDUP_LSH<|{sentence}]|>')
            i += 3
        new_texts.append(new_text)
        diffs.append(diff_text)
        erased_dedups.append('\n'.join(erased_sentences))
    examples['dedup_lsh_text']=new_texts
    examples['erased_dedup_lsh']=erased_dedups
    examples['dedup_lsh_diff']=diffs
    return examples