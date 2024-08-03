import pickle as pk
import random as rm
import math
import os
import modules as md

each_bin = 500

name1 = "ITN"
name2 = "ITN-model"

#distance between each station pair
filename = "../data/" + name1 + "_dis.txt"
f = open(filename,"rb")
dist_dic = pk.load(f, encoding = 'latin1')
f.close()

m_in = {}
m_out = {}
model_flow = {}

clique_flow = {}

for i in dist_dic.keys():
    tem_m1 = rm.gauss(1,0.2)
    tem_m2 = rm.gauss(1,0.2)
    if tem_m1 < 0 or tem_m2 < 0:
        print ("a")
    m_in[i] = tem_m1
    m_out[i] = tem_m2
    clique_flow[i] = {}
    for j in dist_dic.keys():
        if i != j:
            clique_flow[i][j] = 1

q_bin = md.create_q_bin(clique_flow, dist_dic, each_num=each_bin)
bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]

Q = [math.exp(-0.0001*bin_mid[qwe]) for qwe in range(len(bin_mid))]
max_Q = max(Q)
for i in range(len(Q)):
    Q[i] /= max_Q

for i in dist_dic.keys():
    model_flow[i] = {}
    for j in dist_dic[i].keys():
        if i == j:
            continue
        model_flow[i][j] = m_out[i] * m_in[j] * Q[Q_call[i][j]]




fol_name = "../result/" + name2

if not os.path.exists(fol_name):
    os.makedirs(fol_name)

f = open(fol_name + "/m_out_true.txt","wb")
pk.dump(m_out,f)
f.close()

f = open(fol_name + "/m_in_true.txt","wb")
pk.dump(m_in,f)
f.close()

f = open("../data/" + name2 + "_flow.txt","wb")
pk.dump(model_flow,f)
f.close()

f = open(fol_name + "/Q_bin_" + str(each_bin) + "_true.txt","wb")
pk.dump(q_bin,f)
f.close()

f = open(fol_name + "/Q_result_" + str(each_bin) + "_true.txt","wb")
pk.dump(Q,f)
f.close()
