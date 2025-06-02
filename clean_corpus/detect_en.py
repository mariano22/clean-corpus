import fasttext
from huggingface_hub import hf_hub_download
import gc

LANG_MODEL_PATH = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")

# This is done so if using multiprocessing for is_english there is one model per process
current_model = None
def get_model():
    global current_model
    if current_model is None:
        current_model = fasttext.load_model(LANG_MODEL_PATH)
    return current_model

def erase_model():
    global current_model
    if current_model:
        del current_model
        gc.collect()
    current_model = None

def english_proba(text):
    model = get_model()
    labels, probas = model.predict(text,k=10)
    try:
        return probas[labels.index('__label__eng_Latn')].item()
    except ValueError:
        return min(probas[9], 1.0-probas.sum()).item()

def is_english(text):
    en_proba = english_proba(text)
    return en_proba >= 0.65

def calculate_english(examples):
    examples['en_proba'] = [ detect_en.english_proba(join_lines(t)) for t in examples['text'] ]
    return examples
