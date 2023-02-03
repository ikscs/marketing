#encoding: utf-8
CONFIG = {'subject_id': 'DEADBEEF', 'subject_role': 4, 'get_all_prices': True,}

def adapt_product(data_list):
    sep = ' / '
    product_lists = []
    for idx, e in enumerate(data_list):
        adapted = dict()

        adapted['subject_id'] = e['store'] if e['store'] else CONFIG['subject_id']
        adapted['adapter_key'] = idx
        adapted['subject_role'] = CONFIG['subject_role']
        adapted['product_group'] = sep.join((adapted['subject_id'], e['seller']))
        adapted['product_id'] = e['article']
        adapted['manuf'] = None
        adapted['article'] = e['article']
        adapted['name'] = e['title']
        adapted['quantity'] = 1
        adapted['currency'] = 'UAH'
        adapted['ControlRRP'] = None
        adapted['rrp'] = None
        adapted['price_buy'] = e['price']
        adapted['price_sell'] = None
        adapted['product_pic_url'] = e['url']
        adapted['eu'] = None
        adapted['site_prod_id'] = None
        adapted['product_exists'] = 1
        adapted['gtin'] = None

        if CONFIG['get_all_prices'] or adapted['quantity']:
            product_lists.append(adapted)

    return product_lists

def adapt_group(data_list):
    sep = ' / '
    group_dict = dict()
    for row in data_list:
        subject_id = row['store']
        seller = row['seller']
        article = row['article']
        parent = sep.join((subject_id, seller))
        group = sep.join((parent, seller))
        if not parent in group_dict:
            group_dict[parent] = {'parent_group': None, 'product_group': parent, 'name': seller, 'subject_id': subject_id}
#        if not group in group_dict:
#            group_dict[group] = {'parent_group': parent, 'product_group': group, 'name': seller, 'subject_id': subject_id}

    group_lists = {'subject_id': [], 'parent_group': [], 'product_group': [], 'name': [],}

    for e in group_dict:
        group_lists['subject_id'].append(group_dict[e]['subject_id'])
        group_lists['parent_group'].append(group_dict[e]['parent_group'])
        group_lists['product_group'].append(group_dict[e]['product_group'])
        group_lists['name'].append(group_dict[e]['name'])

    return group_lists

def beautify(data_list):
    return data_list

def group_rebuid(groups):
    #dummy
    return False

if __name__ == '__main__':
    #Implementation example
    Timestamp = lambda x: x
    with open('price_marketing.txt', 'r', encoding='utf-8') as f:
        dict_responce = eval(f.read())
    data_list = dict_responce['data']

    groups = adapt_group(data_list)
    #print(groups)
    n = len(groups['subject_id'])
    print(n)
    h = set()
    for i in range(n):
        print(groups['subject_id'][i], '\t', groups['parent_group'][i], '\t', groups['product_group'][i], '\t', groups['name'][i])
        h.add(f"{groups['subject_id'][i]}:{groups['parent_group'][i]}:{groups['product_group'][i]}")

    print(n, len(h))

    for i in range(3):
        print(data_list[i]['article'], ':', data_list[i]['store'], ':', data_list[i]['seller'])
    
    die
    products = adapt_product(data_list)
    print(products)
