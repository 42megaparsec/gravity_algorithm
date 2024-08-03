# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

import pickle as pk
import modules as md


name1 = "ITN"
name2 = "ITN2019"
each_bin = 500

f = open("../data/" + name1 + "_dis.txt","rb")
dist_data = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

f = open("../data/GDP_pk.txt", "rb")
GDP_dic = pk.load(f)
f.close()

fol_name = "../result/" + name2

f = open(fol_name + "/Q_bin_" + str(each_bin) + ".txt", "rb")
q_bin = pk.load(f)
f.close()

od_data = md.filter_data(od_data, dist_data)
m_in, m_out, Q_hist_m, Q_std_m = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, Q_hist_S, Q_std_S = md.calculate_sums(od_data, q_bin)


now_line_width = 0.3
now_fontsize = 18

convert_name = {'Korea, Republic of':'South Korea',"United States of America":'United States','Viet Nam':'Vietnam',"Hong Kong China":"Hong Kong", "Macedonia, North":'Macedonia (FYROM)','Russian Federation':'Russia',
                "Brunei Darussalam": 'Brunei',"Macedonia": "North Macedonia", "Côte d'Ivoire": "Ivory Coast", "Czech Republic": "Czechia"}

filename = "../data/GDP_pk.txt"
f = open(filename,"rb")
GDP_dic = pk.load(f)
f.close()


def round_first_four_digits(number):
    # 숫자가 음수인지 확인
    is_negative = number < 0
    number = abs(number)

    # 숫자를 문자열로 변환
    number_str = str(number)

    # 소수점 위치 찾기
    if '.' in number_str:
        integer_part, fractional_part = number_str.split('.')
    else:
        integer_part, fractional_part = number_str, ''

    # 정수부 길이에 따른 처리
    if len(integer_part) >= 4:
        # 정수부가 4자리 이상인 경우 정수부만 처리
        result = round(number, -(len(integer_part) - 4))
    else:
        # 정수부가 4자리 미만인 경우 소수부 포함 처리
        total_digits = 4
        result = round(number, total_digits - len(integer_part))
        # 유효숫자 4개로 맞추기 위해 필요한 0 추가
        if len(integer_part) < 4:
            result = f"{result:.{total_digits - len(integer_part)}f}"

    # 결과가 정수이면 소수점 이하를 제거
    if isinstance(result, float) and result.is_integer():
        result = int(result)

    # 음수인 경우 부호를 다시 붙이기
    if is_negative:
        result = -result

    return result


names = sorted(GDP_dic.items(), key=lambda x: x[1], reverse=1)

for ori_name in names:
    name = ori_name[0]
    tem_list = []
    tem_list.append(name)
    tem_list.append(GDP_dic[name]/1000)
    tem_list.append(sum_out[name]/1000)
    tem_list.append(m_out[name])
    tem_list.append(sum_in[name]/1000)
    tem_list.append(m_in[name])

    tem_list2 = [name]
    for qw in tem_list[1:]:
        tem_list2.append(round_first_four_digits(qw))

    print (",".join([str(qw) for qw in tem_list2]))
