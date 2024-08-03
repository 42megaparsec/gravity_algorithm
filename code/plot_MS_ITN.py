import matplotlib.pyplot as plt
import pickle as pk
import math
import numpy as np
from sklearn.linear_model import LinearRegression
import modules as md

name1 = "ITN"
name2 = "ITN2019"
each_bin = 500

f = open("../data/" + name1 + "_dis.txt","rb")
line_dist = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

# size of country label
name_size = 15

#size of labels in first fig
f_size = 20
tic_size = 17

#size of labels in second
f_size2 = 15

r_posx = 0.76
r_posy = 0.12


col_dic = {}
cmap = plt.get_cmap('tab10')

f2 = open("../data/ITN_cont.txt", "r")
lines = f2.readlines()
for line in lines:
    a = line[:-1].split(";")
    col_dic[a[0]] = int(a[1])

col_dic["Côte d'Ivoire"] = 1

max_dis = 40000

each_num = 500

od_data = md.filter_data(od_data, line_dist)

q_bin = md.create_q_bin(od_data, line_dist, each_num=each_bin)
m_in, m_out, Q_hist, Q_std = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, _, _, = md.calculate_sums(od_data, q_bin)

bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]

l_margin = 0
r_margin = 0.9
b_margin = 0.1
t_margin = 0.93
h_margin = 0.55
w_margin = -1

f3, (axs) = plt.subplots(2, 2, figsize = (12.0,7.8))
f3.subplots_adjust(left = l_margin,right = r_margin,hspace=h_margin, top = t_margin, bottom=b_margin, wspace = w_margin)

xs2 = []
ys2 = []
ns = []

cont_names = {1:'Africa&Oceania', 3:"Asia",4:"Europe", 5:"NA",6:"America",7:"Oceania"}

name_list = ['USA', "China"]

al = 0.9
cmap2 = [0,'#385663',1,'#A4A68A','#3EB595','#FFB26D','#FF7F60','#812F33']

cols = [[0.7, 0. , 0. ], [0.75, 0.75, 0.  ], [0. , 0.8, 0. ],[0.  , 0.85, 0.85], [0. , 0. , 0.9], [0.95, 0.  , 0.95]]

sorted_col_dic = {1:'#FF4500', 3:'#C8B400', 4:'#9370DB' , 6: '#32CD32',7:'#FFA500'}

for plot_swt in range(2):
    for out_swt in range(2):

        xs = []
        ys = []
        ratios = []
        labels = []
        widths = []

        c_list = []
        a_list = []

        for i in m_out.keys():
            if out_swt == 0:
                if plot_swt == 0:
                    xs.append(m_out[i])
                    ys.append(sum_out[i])
                elif plot_swt == 1:
                    xs.append(m_in[i])
                    ys.append(sum_in[i])
            else:
                if plot_swt == 0:
                    xs.append(m_out[i])
                    ys.append(sum_out[i]/m_out[i])

                elif plot_swt == 1:
                    xs.append(sum_in[i])
                    ys.append(sum_in[i]/m_in[i])

            if plot_swt == 0 and out_swt == 0:
                xs2.append(m_in[i])
                ys2.append(sum_in[i])
                ns.append(str(i))
                ratios.append(sum_out[i])
                labels.append(i)
            if col_dic[i] == 7:
                col_dic[i] = 1
            if col_dic[i] == 5:
                col_dic[i] = 6
            c_list.append(col_dic[i])

            if i in name_list:
                widths.append(0.5)
                labelx = xs[-1]
                labely = ys[-1]
                if plot_swt == 0 and out_swt == 0:
                    if i == "USA":
                        labelx *= 0.61
                        labely *= 0.3
                    if i == "China":
                        labelx *= 0.6
                        labely *= 1.5
                elif plot_swt == 1 and out_swt == 0:
                    if i == "USA":
                        labelx *= 0.65
                        labely *= 1.5
                    if i == "China":
                        labelx *= 0.6
                        labely *= 0.4
                elif out_swt == 1:
                    if plot_swt == 0:
                        if i == "USA":
                            labelx *= 0.88
                            labely *= 0.99
                        if i == "China":
                            labelx *= 0.47
                            labely *= 0.8
                    if i == "USA":
                        labelx *= 0.71
                        labely *= 0.7
                    if i == "China":
                        labelx *= 0.55
                        labely *= 1.14
                #label of China and USA
                axs[plot_swt,out_swt].text(labelx, labely, i, fontsize=name_size)#, weight = 'bold')
            else:
                widths.append(0.5)
        sort_xs = {}
        sort_ys = {}
        for i in range(len(xs)):
            now_c = c_list[i]
            if now_c not in sort_xs.keys():
                sort_xs[now_c] = []
                sort_ys[now_c] = []
            sort_xs[now_c].append(xs[i])
            sort_ys[now_c].append(ys[i])

        dummy_x = [-100]
        dummy_y = [-100]

        mark_wid = 1.2
        mark_dic = {1:'o',3:'D',4:'h',5:'s',6:'s',7:'p'}
        for i in sort_xs.keys():
            if i == 3:
                axs[plot_swt,out_swt].scatter(sort_xs[i], sort_ys[i], c='none', linewidths=mark_wid, edgecolors=[sorted_col_dic[i] for dw in range(len(sort_xs[i]))], marker=mark_dic[i])
            else:
                axs[plot_swt,out_swt].scatter(sort_xs[i], sort_ys[i], c='none', linewidths=mark_wid, edgecolors=[sorted_col_dic[i] for dw in range(len(sort_xs[i]))], marker=mark_dic[i])
            if out_swt != 0:
                geometric_mean_y = np.exp(np.mean(np.log(np.array(sort_ys[i]))))
                axs[plot_swt,out_swt].axhline(geometric_mean_y, color=sorted_col_dic[i], linestyle='--', linewidth = 2)  # 기하평균 가로 점선을 플롯합니다.

        margin = 0.3
        margin2 = 0.6
        if out_swt == 0:
            xlim_min = min(xs) * 0.3
            xlim_max = max(xs) / 0.3
            ylim_min = min(ys) * 0.3
            ylim_max = max(ys) / 0.3
        else:
            xlim_min = min(xs) * margin2
            xlim_max = max(xs) / margin2
            ylim_min = min(ys) * margin2
            ylim_max = max(ys) / margin2

        axs[plot_swt,out_swt].set_xlim(xlim_min, xlim_max)
        axs[plot_swt,out_swt].set_ylim(ylim_min, ylim_max)

        if out_swt == 0:
            line_fitter = LinearRegression()
            line_fitter.fit(np.log(np.array(xs).reshape(-1,1)), np.log(np.array(ys)))
            xs2 = np.array([xlim_min + qwe * (xlim_max - xlim_min)/100 for qwe in range(100)]).reshape(-1,1)
            ys2 = np.exp(line_fitter.predict(np.log(list(xs2))))

            print(plot_swt, line_fitter.coef_, line_fitter.intercept_)
            coef = line_fitter.coef_[0]

            ys3 = [math.exp(line_fitter.intercept_) for qss in range(100)]

            now_score = line_fitter.score(np.log(np.array(xs).reshape(-1,1)),np.log(ys))


            print(line_fitter.coef_, line_fitter.intercept_, now_score)


        for i in [1, 3, 4,  6]:
                        axs[plot_swt, out_swt - 1].scatter(dummy_x, dummy_y, c='none', marker=mark_dic[i],
                                               linewidths=mark_wid, edgecolors=[sorted_col_dic[i]], label=cont_names[i])


        axs[plot_swt,out_swt].set_xscale('log')
        axs[plot_swt,out_swt].set_yscale('log')
        axs[plot_swt,out_swt].tick_params(axis='both', which='both', direction='in', labelsize=tic_size)


axs[0,0].text(0.025, 0.95, "a", transform=axs[0,0].transAxes, fontsize=f_size*1.5, va='top' , weight='bold')
axs[0,1].text(0.025, 0.95, "b", transform=axs[0,1].transAxes, fontsize=f_size*1.5, va='top' , weight='bold')
axs[1,0].text(0.025, 0.95, "c", transform=axs[1,0].transAxes, fontsize=f_size*1.5, va='top' , weight='bold')
axs[1,1].text(0.025, 0.95, "d", transform=axs[1,1].transAxes, fontsize=f_size*1.5, va='top' , weight='bold')

axs[0,0].legend(bbox_to_anchor = (0.05,0.99),loc='lower left',fontsize = f_size, frameon = 0,ncol = 4)

axs[0,0].set_ylabel("$S_{i}^{out}$", fontsize=f_size)
axs[0,0].set_xlabel(r"$\bar{m}_{i}^{out}$", fontsize=f_size)
axs[1,0].set_ylabel("$S_{i}^{in}$", fontsize=f_size)
axs[1,0].set_xlabel(r"$\bar{m}_{i}^{in}$", fontsize=f_size)

axs[0,1].set_ylabel("$r_{i}^{out}$", fontsize=f_size)
axs[0,1].set_xlabel(r"$\bar{m}_{i}^{out}$", fontsize=f_size)
axs[1,1].set_ylabel("$r_{i}^{in}$", fontsize=f_size)
axs[1,1].set_xlabel(r"$\bar{m}_{i}^{in}$", fontsize=f_size)

plt.tight_layout()
plt.savefig("../figure/paper/ITN_MS.pdf",dpi = 300)
plt.show()
