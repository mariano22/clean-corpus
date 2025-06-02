
nsfw_lines = None
def load_nsfw_lines():
    global nsfw_lines
    with open('../data/en_nsfw.txt', 'r', encoding='utf-8') as file:
        nsfw_lines = file.readlines()
    nsfw_lines = [' '+l.strip()+' ' for l in nsfw_lines]

def check_is(examples):
    global nsfw_lines
    is_presents = []
    for sts in examples['sentences_normalized']:
        ntxt = ' '+' '.join(sts)+' '
        is_present = [l in ntxt for l in nsfw_lines]
        is_presents.append(is_present)
    examples['is_present']=is_presents
    return examples