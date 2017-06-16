import parse_coc

def generate(coc_datas, template_path):
    with open(template_path, 'r') as f:
        template_text = f.read()

    keys = set()
    offset = 0
    while True:
        start_point = template_text.find('{{', offset)
        if start_point == -1:
            break
        end_point = template_text.find('}}', start_point)
        offset = end_point
        keys.add(template_text[start_point+2:end_point])

    params_to_template = {}
    for key in keys:
        params_to_template[key] = get_nested_object(coc_datas, key)

    output_text = template_text
    for key, value in params_to_template.items():
        output_text = output_text.replace('{{' + key + '}}', str(value))

    return output_text


def get_nested_object(obj, nested_key):
    splited_nested_key = nested_key.split('.')
    if len(splited_nested_key) > 1:
        key = splited_nested_key[0]
        return get_nested_object(obj[key], '.'.join(splited_nested_key[1:]))
    return obj[nested_key]
    

if __name__ == '__main__':
    coc_datas = parse_coc.parse_coc('default_skill.json', '1.txt')
    print(generate(coc_datas, 'template.txt'))
