import re
import phonenumbers
from phonenumbers import PhoneNumberMatcher

email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
email_regex_compiled = re.compile(email_regex)

def mask_emails(text: str) -> tuple[str, int]:
    masked_text = email_regex_compiled.sub("<|EMAIL_ADDRESS|>", text)
    mails = [m[0] for m in email_regex_compiled.finditer(text)]
    return masked_text, len(mails), mails

def mask_phone_numbers(text):
    matches = PhoneNumberMatcher(text, "US", leniency=phonenumbers.Leniency.POSSIBLE)
    phones = []
    for match in matches:
        phones.append(match.raw_string)
        text = text.replace(match.raw_string, "<|PHONE_NUMBER|>")
    return text, len(phones), phones

MASK_ENTITIES = {
    'mail':mask_emails,
    'phone':mask_phone_numbers,
}

def calculate_masked_pii(examples, mask_entity):
    newtexts = []
    examples[f'erased_{mask_entity}'] = []
    examples[f'n_erased_{mask_entity}'] = []
    for e in examples['text']:
        new_text, _, erased_subtexts = mask_pii.MASK_ENTITIES[mask_entity](e)
        examples[f'erased_{mask_entity}'].append(erased_subtexts)
        examples[f'n_erased_{mask_entity}'].append(len(erased_subtexts))
        newtexts.append(new_text)
    examples['text']=newtexts
    return examples