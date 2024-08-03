import matplotlib.pyplot as plt
import pickle as pk
import numpy as np
from sklearn.linear_model import LinearRegression
import modules as md

ticksize = 19
labelsize= 24

name1 = "ITN"
name2 = "ITN-model"
each_bin = 500

f = open("../data/" + name1 + "_dis.txt","rb")
line_dist = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

fol_name = "../result/" + name2

f = open(fol_name + "/m_in_true.txt", "rb")
m_in_true = pk.load(f)
f.close()

f = open(fol_name + "/m_out_true.txt", "rb")
m_out_true = pk.load(f)
f.close()

od_data = md.filter_data(od_data, line_dist)

q_bin = md.create_q_bin(od_data, line_dist, each_num=each_bin)
m_in, m_out, Q_hist, Q_std = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, _, _, = md.calculate_sums(od_data, q_bin)

plot_data = {}

share_keys=  m_out.keys()

plot_data[0] = {'xs' : [m_out_true[qw] for qw in share_keys],'ys' : [m_out[qw] for qw in share_keys]}
plot_data[1] = {'xs' : [m_in_true[qw] for qw in share_keys],'ys' : [m_in[qw] for qw in share_keys]}
plot_data[2] = {'xs' : [m_out_true[qw] for qw in share_keys],'ys' :[sum_out[qw] for qw in share_keys]}
plot_data[3] = {'xs' : [m_in_true[qw] for qw in share_keys],'ys' : [sum_in[qw] for qw in share_keys]}

l_margin = 0.15
r_margin = 0.85
b_margin = 0.15
t_margin = 0.95
w_margin = 0.05
h_margin = 0.05

f, axs = plt.subplots(2, 2, figsize = (9,7.8),sharex = 'col')
f.subplots_adjust(left = l_margin,right = r_margin,hspace=h_margin, wspace = w_margin, top = t_margin, bottom=b_margin)

label_dic = {0:"(a)",1:"(b)",2:"(c)",3:"(d)"}

for i in range(2):
    for j in range(2):
        now_idx = i*2 + j
        if i == 0:
            #axs[i,j].scatter(plot_data[now_idx]['xs'],plot_data[now_idx]['ys'], s = 25, edgecolor = '#9370DB',marker = 's', linewidth = 1.5,c = 'w')
            axs[i, j].scatter(plot_data[now_idx]['xs'], plot_data[now_idx]['ys'], s=30, edgecolor='cornflowerblue', marker='s',
                              linewidth=1.5, c='w',alpha = 0.9)

        else:
            axs[i,j].scatter(plot_data[now_idx]['xs'],plot_data[now_idx]['ys'],s = 25, edgecolor ='#3CB371',marker = 'D',linewidth = 1.5, c = 'w')
        xs = plot_data[now_idx]['xs']
        ys = plot_data[now_idx]['ys']

        line_fitter = LinearRegression()
        line_fitter.fit(np.log(np.array(xs).reshape(-1,1)), np.log(np.array(ys)))

        xlim_min = min(xs)
        xlim_max = max(xs)

        ylim_min = min(ys)
        ylim_max = max(ys)
        print (i,j, xlim_min, xlim_max, ylim_min, ylim_max)
        xs2 = np.array([0.01] + [xlim_min + qwe * (xlim_max - xlim_min)/100 for qwe in range(100)] + [2]).reshape(-1,1)
        ys2 = np.exp(line_fitter.predict(np.log(list(xs2))))
        if i == 0:
            axs[i,j].plot(list(xs2), list(ys2), '--', c='k', linewidth=1.3,alpha = 1)
        now_score = line_fitter.score(np.log(np.array(xs).reshape(-1,1)),np.log(ys))
        print (now_score)
        if i == 0:
            axs[i,j].text(0.5, 0.11, r"$R^2 > 1 - 10^{-4}$", transform=axs[i,j].transAxes, fontsize=15, va='top')
        axs[i,j].set_xlim(0.52,1.45)
        if i == 0:
            axs[i, j].set_ylim(0.52, 1.45)
        else:
            axs[i,j].set_ylim(15,85)

xticks1 =  np.arange(0.6,1.42,0.2)

axs[0,0].tick_params(axis ='both', direction = 'in' ,labelsize = ticksize)

axs[1,0].set_ylabel(r'$S^{\mathrm{out}}$',fontsize = labelsize,labelpad = 0)
axs[1,0].tick_params(axis ='both', direction = 'in' ,labelsize = ticksize)


axs[1,1].set_ylabel(r'$S^{\mathrm{in}}$',fontsize = labelsize, rotation = 270,labelpad = 15)
axs[1,1].tick_params(axis ='both',  direction = 'in',labelsize = ticksize)
axs[1,1].yaxis.tick_right()
axs[1,1].yaxis.set_label_position("right")


axs[1,0].set_xlabel(r'$\tilde{m}^{\mathrm{out}}$',fontsize = labelsize)
axs[1,0].set_xticks(xticks1)
axs[1,0].tick_params(axis ='both',  direction = 'in',labelsize = ticksize)
axs[0,0].set_yticks(xticks1)
axs[0,0].set_ylabel(r'$\bar{m}^{\mathrm{out}}$',fontsize = labelsize)


axs[1,1].set_xlabel(r'$\tilde{m}^{\mathrm{in}}$',fontsize = labelsize)
axs[1,1].set_xticks(xticks1)
axs[0,1].tick_params(axis ='both', direction = 'in',labelsize = ticksize)
axs[0,1].set_yticks(xticks1)
axs[0,1].yaxis.tick_right()
axs[0,1].yaxis.set_label_position("right")
axs[0,1].set_ylabel(r'$\bar{m}^{\mathrm{in}}$',fontsize = labelsize,rotation = 270,labelpad = 25)

plt.savefig("../figure/paper/model_MS.svg",dpi = 1200)
plt.show()