import matplotlib.pyplot as plt
import pickle as pk
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
import modules as md
import numpy as np
import matplotlib as mpl

heat_bin_num = 40
each_num = 100
maxcol = 100

#label size
tem_size = 35
#tick size
tem_size2 = 20


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

def MyFormatter(x, lim):
    if x == 0:
        return 0
    else:
        x = str(x).split(".")
        return "$10^{" + str(x[0]) + r"}$"

# end def
majorFormatter = FuncFormatter(MyFormatter)

q_bin = md.create_q_bin(od_data, dist_data, each_num=each_bin)
m_in, m_out, Q_m, Q_std_m = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, Q_S, Q_std_S = md.calculate_sums(od_data, q_bin)
Q_GDP, Q_std_GDP = md.calculate_GDPs(od_data, GDP_dic, q_bin)

bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]


S_expect = {}
M_expect = {}
GDP_expect = {}

for i in od_data.keys():
    S_expect[i] = {}
    M_expect[i] = {}
    GDP_expect[i] = {}
    for j in od_data[i].keys():
        if i == j:
            continue
        S_expect[i][j] = sum_out[i] * sum_in[j] * Q_S[Q_call[i][j]]
        M_expect[i][j] = m_out[i] * m_in[j] * Q_m[Q_call[i][j]]
        GDP_expect[i][j] = GDP_dic[i] * GDP_dic[j] * Q_GDP[Q_call[i][j]]

l_margin = 0.07
r_margin = 0.98
b_margin = 0.18
t_margin = 0.95
w_margin = 0.28
h_margin = 0.05


label_dic  = {1:"(a)",2:'(b)',3:'(c)'}

f, axs = plt.subplots(1,3, figsize = (20,6),sharex = 'col')
f.subplots_adjust(left = l_margin,right = r_margin,hspace=h_margin, wspace = w_margin, top = t_margin, bottom=b_margin)
for mass_st_swt in range(1,4):
    xs = []
    ys = []
    for i in od_data.keys():
        for j in od_data[i].keys():
            try:
                if mass_st_swt == 2:
                    ys.append(S_expect[i][j])
                elif mass_st_swt == 3:
                    ys.append(GDP_expect[i][j])
                elif mass_st_swt == 1:
                    ys.append(M_expect[i][j])
                xs.append(od_data[i][j])
            except:
                pass

    ms = [m_in[qw] for qw in m_out.keys()]
    ss = [sum_in[qw] for qw in m_out.keys()]

    xs2 = list(max(xs) * qwe / 1000. for qwe in range(1000))

    fit_len = 200

    maxx = max(Q_S)
    for z in range(len(Q_S)):
        Q_S[z] /= maxx

    each_num2 = 100


    each_num = 500
    iter_num = 5

    x = []
    y = []

    for i in range(len(xs)):
        if xs[i] > 0.00001 and ys[i] > 0.00001:
            x.append(np.log10(xs[i]))
            y.append(np.log10(ys[i]))
            # print (xs[i],ys[i])

    if max(x) > max(y):
        min_max = max(y)
    else:
        min_max = max(x)

    x2 = [min_max * qwd / 100. for qwd in range(100)]
    y2 = [min_max * qwd / 100. for qwd in range(100)]

    path = '/Windows/Fonts/Times.ttf'
    fontprop = fm.FontProperties(fname=path, size=18)
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=heat_bin_num)
    print(np.max(heatmap))

    if name1 =="ITN":
        if mass_st_swt == 1:
            maxcol = 100
        if mass_st_swt == 2:
            maxcol = 100

    extent = [xedges[0], xedges[-1], 1, 9.2]


    cmap = plt.cm.YlGnBu
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # force the first color entry to be white
    uniform_col = 0.8
    cmaplist[0] = (uniform_col, uniform_col, uniform_col, 1.0)

    # create the new map
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

    # define the bins and normalize
    bounds = np.linspace(0, maxcol, maxcol + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    axs[mass_st_swt-1].xaxis.set_major_formatter(majorFormatter)
    axs[mass_st_swt-1].yaxis.set_major_formatter(majorFormatter)

    mpl.rcParams.update({'font.size': tem_size })
    cax = axs[mass_st_swt-1].imshow(heatmap.T, extent=extent, origin='lower', aspect='auto', interpolation='nearest', cmap=cmap, norm=norm)
    axs[mass_st_swt-1].tick_params(labelsize=tem_size2)
    axs[mass_st_swt-1].set_xlim(min(x), max(x))
    axs[mass_st_swt - 1].set_ylim(1,9.2)

    if name1 == "ITN":
        if mass_st_swt == 10:
            cbar = plt.colorbar(cax, ticks=[0, 10, 20, 30, 40 , 50])
            cbar.minorticks_off()
            cbar.ax.tick_params(labelsize=tem_size2)
            cbar.ax.set_yticklabels(['0', '10', '20','30', '40','>50'])#, '50', '60', '70', '80', '90', '>100'])  # vertically oriented colorbar
        else:
            cbar = plt.colorbar(cax, ticks=[0, 20, 40, 60, 80, 100])
            cbar.minorticks_off()
            cbar.ax.tick_params(labelsize=tem_size2 )
            cbar.ax.set_yticklabels(['0', '20', '40', '60', '80',
                                     '>100'])

    axs[mass_st_swt-1].set_xlabel(r'$f_{ij}$', fontsize=tem_size, fontproperties=fontprop)
    if mass_st_swt == 1:
        axs[mass_st_swt-1].set_ylabel(r'$\bar{f}_{ij}$', fontsize=tem_size, fontproperties=fontprop)
    elif mass_st_swt == 2:
        axs[mass_st_swt-1].set_ylabel(r'$\bar{f}_{ij}^{\; S}$', fontsize=tem_size, fontproperties=fontprop)
    elif mass_st_swt == 3:
        axs[mass_st_swt-1].set_ylabel(r'$\bar{f}_{ij}^{\; GDP}$', fontsize=tem_size, fontproperties=fontprop)

    axs[mass_st_swt-1].plot(x2, y2, '--', c='black', linewidth=3)

plt.savefig("../figure/paper/heatmap2_" + str(uniform_col) + ".svg",dpi = 300)

plt.show()