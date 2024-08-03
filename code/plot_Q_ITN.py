import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle as pk
import modules as md

label_font = 25
tick_font = 20

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

m_in, m_out, Q_hist_m, Q_std_m = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, Q_hist_S, Q_std_S = md.calculate_sums(od_data, q_bin)
Q_hist_GDP, Q_std_GDP = md.calculate_GDPs(od_data, GDP_dic, q_bin)

max_Q_S = max(Q_hist_S)
max_Q_GDP = max(Q_hist_GDP)

for i in range(len(Q_hist_S)):
    Q_hist_S[i] /= max_Q_S
    Q_std_S[i] /= max_Q_S
    Q_hist_GDP[i] /= max_Q_GDP
    Q_std_GDP[i] /= max_Q_GDP


hists = [Q_hist_m, Q_hist_S, Q_hist_GDP]
stds = [Q_std_m, Q_std_S, Q_std_GDP]

markers = ['o','o','o','','']
line_styles =  ['','','','--','--']
line_colors = ['#228B22','#4169E1','#8A2BE2','#D2691E','k']
labels = [r"$\bar{Q}_{m}(d)$",r"$\bar{Q}_{S}(d)$",r"$\bar{Q}_{GDP}(d)$"]
label_dic2  = {0:"(a)",1:'(b)',2:'(c)'}

l_margin = 0.1
r_margin = 0.95
b_margin = 0.15
t_margin = 0.95
w_margin = 2
h_margin = 0.05

f, axs = plt.subplots(1,3, figsize = (18,6),sharex = 'col')
f.subplots_adjust(left = l_margin,right = r_margin,hspace=h_margin, wspace = w_margin, top = t_margin, bottom=b_margin)

bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]

for i,now_hist in enumerate(hists):

    xs = [bin_mid[qwe] for qwe in range(len(bin_mid))]
    ys = now_hist

    line_fitter = LinearRegression()
    line_fitter.fit(np.log(np.array(xs).reshape(-1, 1)), np.log(np.array(ys)))

    xlim_min = min(xs)
    xlim_max = max(xs)

    ylim_min = min(ys)
    ylim_max = max(ys)

    xs2 = np.array([xlim_min + qwe * (xlim_max - xlim_min) / 100 for qwe in range(100)]).reshape(-1, 1)
    ys2 = np.exp(line_fitter.predict(np.log(list(xs2))))
    axs[i].plot(list(xs2), list(ys2), '--', c='k', linewidth=2.5, alpha=1)

    now_score = line_fitter.score(np.log(np.array(xs).reshape(-1, 1)), np.log(ys))
    print(now_score)
    axs[i].text(0.05, 0.12, r"$R^2 = $" + str(round(now_score,3)), transform=axs[i].transAxes, fontsize=label_font,
                       va='top')

    axs[i].errorbar(xs,ys,yerr = stds[i], c = 'purple', capsize = 3, marker = markers[i],
                    elinewidth = 1.3, linewidth = 0, markersize = 6, label = labels[i])

    axs[i].set_xlabel('d (km)',style='italic',fontsize = label_font)
    if i !=1000:
        axs[i].tick_params(which = 'both', direction = 'in', labelsize=tick_font)
        axs[i].set_yticks([1,0.1,0.01])
    else:
        axs[i].tick_params(which = 'both', axis = 'y',labelleft = 0, right = 0)
        axs[i].tick_params(which = 'both', axis = 'both', direction = 'in', labelsize=tick_font)

    axs[i].set_xscale('log')
    axs[i].set_yscale('log')
    axs[i].set_ylim(0.007,1.3)

labels = [r"$\bar{Q}_{m}(d)$",r"$\bar{Q}_{S}(d)$",r"$\bar{Q}_{GDP}(d)$"]
axs[0].set_ylabel(r"$\bar{Q}_{m}(d)$", style='italic',fontsize = label_font)
axs[1].set_ylabel(r"$\bar{Q}_{S}(d)$", style='italic',fontsize = label_font)
axs[2].set_ylabel(r"$\bar{Q}_{GDP}(d)$", style='italic',fontsize = label_font)

plt.xticks(fontsize = tick_font)
current_values = plt.gca().get_yticks()

plt.tight_layout()
plt.savefig("../figure/paper/ITN_Q.svg",dpi = 300)
plt.show()