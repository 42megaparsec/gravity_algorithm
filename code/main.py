import numpy as np
import pickle as pk
import modules as md
import os

each_bin = 500

name1 = "ITN"
name2 = "ITN-model"

f = open("../data/" + name1 + "_dis.txt","rb")
line_dist = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

od_data = md.filter_data(od_data, line_dist)

q_bin = md.create_q_bin(od_data, line_dist, each_num=each_bin)
m_in, m_out, Q_hist, Q_std = md.calculate_mass(od_data, q_bin, iter_step=5)

fol_name = "../result/" + name2

if not os.path.exists(fol_name):
    os.makedirs(fol_name)

f = open(fol_name + "/m_out.txt","wb")
pk.dump(m_out,f)
f.close()

f = open(fol_name + "/m_in.txt","wb")
pk.dump(m_in,f)
f.close()

f = open(fol_name + "/Q_bin_" + str(each_bin) + ".txt","wb")
pk.dump(q_bin,f)
f.close()

f = open(fol_name + "/Q_result_" + str(each_bin) + ".txt","wb")
pk.dump(Q_hist,f)
f.close()