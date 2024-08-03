import modules as md
import pickle as pk
import time as tm
import random as rm
import math

name1 = "ITN"
name2 = "ITN2019"
each_bin = 500
ensem_num = 200
tem_idx = 0

print (name2,tem_idx)

f = open("../data/" + name1 + "_dis.txt","rb")
dist_data = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

f = open("../data/GDP_pk.txt", "rb")
GDP_dic = pk.load(f)
f.close()

funcs = [md.calculate_mass,md.calculate_sums, md.calculate_GDPs]


perf_list = []

tot_len = 19
if name2 == "ITN2019":
    tot_len = 11
for t in range(tot_len):
    now_rmv = round(t*0.05,2)

    tem_r = 0
    tem_SSI = 0


    tot_MAE = 0
    for z in range(ensem_num):

        test_set = {}
        veri_set = {}

        if t == 0:
            for i in od_data.keys():
                test_set[i] = od_data[i].copy()
                veri_set[i] = od_data[i].copy()
        else:
            for i in od_data.keys():
                test_set[i] = {}
                veri_set[i] = {}
                for j in od_data[i].keys():
                    if (rm.random() > now_rmv):
                        test_set[i][j] = od_data[i][j]
                    else:
                        veri_set[i][j] = od_data[i][j]

        q_bin = md.create_q_bin(test_set, dist_data, each_num=each_bin)
        if tem_idx < 2:
            m_in, m_out, Q, Q_std = funcs[tem_idx](test_set, q_bin)
        else:
            m_out = {}
            m_in = {}
            Q, Q_std = funcs[tem_idx](test_set, GDP_dic, q_bin)
            for i in GDP_dic.keys():
                m_out[i] = GDP_dic[i]
                m_in[i] = GDP_dic[i]

        Q_call = q_bin["call_dic"]


        #verification
        tem_sum = 0
        tem_squ = 0
        tem_diff = 0
        tem_num = 0

        tem_MAE = 0

        SSI1 = 0
        SSI2 = 0
        for i in veri_set.keys():
            for j in veri_set[i].keys():
                if i not in m_out.keys():
                    continue
                if j not in m_in.keys():
                    continue
                if od_data[i][j] ==0:
                    continue

                now_idx = md.cal_bindex(dist_data[i][j], q_bin)
                predict = m_out[i] * m_in[j] * Q[now_idx]
                real = od_data[i][j]

                tem_MAE += abs(predict - real)

                tem_sum += real
                tem_squ += real ** 2
                tem_diff += (real-predict) ** 2
                tem_num += 1
                SSI1 += 2* min([predict,real])
                SSI2 += predict+real

        tem_r += 1 - tem_diff / (tem_squ  - tem_sum**2/tem_num)
        tot_MAE += tem_r/tem_num
        tem_SSI += SSI1/SSI2
    print(now_rmv, tem_SSI/ensem_num)
    perf_list.append(tem_SSI/ensem_num)


f = open("../result/" + name2 + "/Reconst_" + str(tem_idx) + ".txt","wb")
pk.dump(perf_list,f)
f.close()