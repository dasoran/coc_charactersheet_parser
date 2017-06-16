
import csv
import json


def parse_coc(default_skills_path, character_sheet_path, append_default_skills_path=None):
    """キャラクター保管所のキャラシをパースする"""
    # 初期値読み込み
    with open(default_skills_path, 'r') as f:
        default_skills = json.load(f)
    if append_default_skills_path is not None:
        with open(append_default_skills_path, 'r') as f:
            reader = csv.reader(f)
        for row in reader:
            default_skills[row[0]] = row[1]

    # キャラシ読み込み
    with open(character_sheet_path, encoding='cp932') as f:
        lines = f.readlines()
    raw_basic_status = lines[2:20]
    raw_buttle_skills = read_skills(lines, '戦闘系技能')
    raw_explore_skills = read_skills(lines, '探索系技能')
    raw_action_skills = read_skills(lines, '行動系技能')
    raw_communicate_skills = read_skills(lines, '交渉系技能')
    raw_knowledge_skills = read_skills(lines, '知識系技能')

    coc_datas = {}
    # 基本情報パース
    coc_datas['basic_status'] = basic_status_to_dict(raw_basic_status)

    # 技能値パース
    coc_datas['buttle_skills'] = skill_to_dict(raw_buttle_skills, default_skills)
    coc_datas['explore_skills'] = skill_to_dict(raw_explore_skills, default_skills)
    coc_datas['action_skills'] = skill_to_dict(raw_action_skills, default_skills)
    coc_datas['communicate_skills'] = skill_to_dict(raw_communicate_skills, default_skills)
    coc_datas['knowledge_skills'] = skill_to_dict(raw_knowledge_skills, default_skills)

    return coc_datas


def get_value_in_status_line(line):
    return line.split('：')[1][:-1]


def get_values_in_status_line(line):
    values = []
    for status_line in line[:-1].split(' / '):
        values.append(status_line.split('：')[1])
    return values


def basic_status_to_dict(raw_texts):
    """キャラクター保管所のCoCキャラシのスキル以外の部分のテキストを抽出する"""
    basic_status = {}
    basic_status['name'] = get_value_in_status_line(raw_texts[0])
    basic_status['job'] = get_value_in_status_line(raw_texts[1])
    old_and_sex = get_values_in_status_line(raw_texts[2])
    basic_status['old'] = old_and_sex[0]
    basic_status['sex'] = old_and_sex[1]
    basic_status['born_at'] = get_value_in_status_line(raw_texts[3])
    appear_feature = get_values_in_status_line(raw_texts[4])
    basic_status['color_of_hear'] = appear_feature[0]
    basic_status['color_of_eye'] = appear_feature[1]
    basic_status['color_of_face'] = appear_feature[2]
    basic_status['height'] = get_value_in_status_line(raw_texts[5])
    basic_status['weight'] = get_value_in_status_line(raw_texts[6])

    basic_status['hp'] = {}
    basic_status['mp'] = {}
    basic_status['san'] = {}
    statuses = [status for status in raw_texts[17][:-1].split('　') if status != ''][1:]
    basic_status['str'] = int(statuses[0])
    basic_status['con'] = int(statuses[1])
    basic_status['pow'] = int(statuses[2])
    basic_status['dex'] = int(statuses[3])
    basic_status['app'] = int(statuses[4])
    basic_status['siz'] = int(statuses[5])
    basic_status['int'] = int(statuses[6])
    basic_status['edu'] = int(statuses[7])
    basic_status['hp']['max'] = int(statuses[8])
    basic_status['mp']['max'] = int(statuses[9])
    basic_status['hp']['now'] = int(get_value_in_status_line(raw_texts[9]))
    basic_status['mp']['now'] = int(get_value_in_status_line(raw_texts[10]))
    san = get_value_in_status_line(raw_texts[11]).split('/')
    if san[0] == '':
        basic_status['san']['now'] = basic_status['pow'] * 5
    else:
        basic_status['san']['now'] = san[0]
    basic_status['san']['max'] = int(san[1])

    return basic_status


def read_skills(lines, header_text):
    """キャラクター保管所のCoCキャラシの該当スキル部分のテキストを抽出する"""
    offset_point = 0
    for i, line in enumerate(lines):
        if line.find(header_text) > 0:
            offset_point = i + 2

    raw_skills_texts = []
    for line in lines[offset_point:]:
        if line.replace('\n', '') == '':
            break
        raw_skills_texts.append(line)
    return raw_skills_texts


def skill_to_dict(raw_texts, default_skills):
    """スキルのテキストをパースしてdictにする"""
    splited_texts = []
    for raw_text in raw_texts:
        filtered_text = raw_text.replace('●', '')\
                            .replace('《', '')\
                            .replace('》', ' ')\
                            .replace('％', '')\
                            .replace('　', ' ')
        tmp_splited_text = [text for text in filtered_text.split(' ') if len(text) > 0]
        splited_text = tmp_splited_text[:-1]
        if len(tmp_splited_text[-1][:-1]) > 0:
            splited_text.append(tmp_splited_text[-1][:-1])
        splited_texts.extend(splited_text)

    skill_hash = {}
    for i in range(0, len(splited_texts), 2):
        skill_name = splited_texts[i]
        skill_value = int(splited_texts[i + 1])
        if skill_name.find('()') != -1:
            continue
        skill_hash[skill_name] = {}
        if skill_name in default_skills:
            default_value = default_skills[skill_name]
        else:
            default_value = 0
        skill_hash[skill_name]['default'] = default_value
        skill_hash[skill_name]['grow'] = skill_value - default_value

    return skill_hash


if __name__ == '__main__':
    coc_datas = parse_coc('default_skill.json', '1.txt')
    print(coc_datas['basic_status'])
    print(coc_datas['buttle_skills'])
    print(coc_datas['explore_skills'])
    print(coc_datas['action_skills'])
    print(coc_datas['communicate_skills'])
    print(coc_datas['knowledge_skills'])
