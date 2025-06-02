from transformers import AutoTokenizer,AutoModelForSequenceClassification
import torch
import gc

LABEL_AND_MODEL = {
    'hate': "facebook/roberta-hate-speech-dynabench-r4-target" ,
    'NSFW': 'michellejieli/NSFW_text_classifier',
}

# This is done so if using multiprocessing for  there is one model per process
current_model = None
current_tokenizer = None
def get_engines(model_name):
    global current_model, current_tokenizer
    if current_model is None:
        current_model = AutoModelForSequenceClassification.from_pretrained(model_name)  
        current_tokenizer = AutoTokenizer.from_pretrained(model_name)
    return current_model, current_tokenizer

def erase_engines():
    global current_model, current_tokenizer
    if current_model:
        del current_model
        del current_tokenizer
        gc.collect()
    current_model = None
    current_tokenizer = None

def calculate_score(examples, score_label):
    model_name = LABEL_AND_MODEL[score_label]
    model, tokenizer = get_engines(model_name)
    texts = examples['dedup_text']
    tokens = tokenizer(
            texts,
            add_special_tokens=True,
            truncation=True,
            padding=True,
            max_length=tokenizer.model_max_length,
            stride=32,
            return_overflowing_tokens=True,
            return_tensors="pt"
    )
    overflow_to_sample_mapping = tokens['overflow_to_sample_mapping']
    del tokens['overflow_to_sample_mapping']
    with torch.no_grad():
        probas = torch.softmax(model(**tokens).logits, dim=-1)
    scores = []
    label_idx = [k for k,v in model.config.id2label.items() if v == score_label][0]
    for i in range(len(texts)):
        score = probas[overflow_to_sample_mapping==i].max(dim=0).values[label_idx]
        scores.append( score )
        if score>0.5:
            print(score)
            print(texts[i])
            print('==================')
    examples[f'{score_label}_score']=scores
    return examples