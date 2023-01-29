#encoding: utf-8
def Timestamp(s):
    return s

def dict2data(dict_responce):
    data = dict_responce['data']
    subject_ids = get_subject_ids(data)
    return {'data': data, 'subject_ids': subject_ids}

def get_subject_ids(data):
    subject_ids = set()
    for e in data:
        subject_ids.add(e['store'])
    return subject_ids

if __name__ == '__main__':
    #Implementation example
    with open('price_marketing.txt', 'r', encoding='utf-8') as f:
        dict_responce = eval(f.read())
    data = dict2data(dict_responce)
    print(data['subject_ids'])
