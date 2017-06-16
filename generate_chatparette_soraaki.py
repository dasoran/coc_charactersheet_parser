import parse_coc


def generate_status(coc_datas):
    output_text = ''
    t_datas = coc_datas['basic_status']
    edu_5 = t_datas['edu'] * 5
    if edu_5 > 99:
        edu_5 = 99
    output_text += '1d100<=({{SAN}}) {0}{1}\n'.format(t_datas['name'], 'SAN値C')
    output_text += 'ccb<=({0}) {1}{2}\n'.format(t_datas['int'] * 5, t_datas['name'], 'アイディア')
    output_text += 'ccb<=({0}) {1}{2}\n'.format(t_datas['pow'] * 5, t_datas['name'], '幸運')
    output_text += 'ccb<=({0}) {1}{2}\n'.format(edu_5, t_datas['name'], '知識')
    output_text += 'ccb<=({0}) {1}{2}\n'.format(edu_5, t_datas['name'], '母国語')
    output_text += '\n'
    output_text += '↓「5」を書き換えてステータスダイスが振れる\n'
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['str'], t_datas['name'], 'STR')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['con'], t_datas['name'], 'CON')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['pow'], t_datas['name'], 'POW')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['dex'], t_datas['name'], 'DEX')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['app'], t_datas['name'], 'APP')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['siz'], t_datas['name'], 'SIZ')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['int'], t_datas['name'], 'INT')
    output_text += 'ccb<=({0}*5) {1}{2}ダイス\n'.format(t_datas['edu'], t_datas['name'], 'EDU')
    output_text += '\n'
    output_text += '↓抵抗表　Aに自分の技能値、BにKPの値\n'
    output_text += 'resb(A-B)\n'
    output_text += '\n'
    output_text += '↓組み合わせロール　A、Bそれぞれに値\n'
    output_text += 'cbrb(A-B)\n'
    return output_text


def generate_skills(coc_datas, generate_type):
    output_text = ''
    name = coc_datas['basic_status']['name']
    target_datas = coc_datas[generate_type]
    for key, value in target_datas.items():
        output_text += 'ccb<=({0}+{1}) {2}{3}\n'.format(value['default'], value['grow'], name, key)
    return output_text


if __name__ == '__main__':
    coc_datas = parse_coc.parse_coc('default_skill.json', '1.txt')
    print(generate_status(coc_datas))
    print(generate_skills(coc_datas, 'buttle_skills'))
    print(generate_skills(coc_datas, 'explore_skills'))
    print(generate_skills(coc_datas, 'action_skills'))
    print(generate_skills(coc_datas, 'communicate_skills'))
    print(generate_skills(coc_datas, 'knowledge_skills'))
