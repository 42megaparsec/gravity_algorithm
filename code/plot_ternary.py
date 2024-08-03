
import ternary
import matplotlib.pyplot as plt
import pickle as pk
import math
import matplotlib as mpl
import modules as md

name1 = "ITN"
name2 = "ITN2019"
each_bin = 500

# size of country label
name_size = 142
fontsize = 25
#size of labels in second
f_size2 = 16
tick_size = 20
label_margin = 0.25

f = open("../data/" + name1 + "_dis.txt","rb")
dist_data = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

od_data = md.filter_data(od_data, dist_data)
q_bin = md.create_q_bin(od_data, dist_data, each_num=each_bin)
m_in, m_out, Q, Q_std_m = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, Q_S, Q_std_S = md.calculate_sums(od_data, q_bin)

bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]

power_list = ['USA', 'China','Germany']

for i in power_list:
    print (i, sum_out[i], sum_in[i], m_out[i], m_in[i], sum_out[i]/m_out[i], sum_in[i]/m_in[i], sum_out[i]/sum_in[i], m_in[i]/m_out[i])

fig, axes = plt.subplots(1,3, figsize = (24,6))
plt.subplots_adjust(wspace = 1)


coun1 = 0
coun2 = 0
for r_idx in range(3):
    #figure, tax = ternary.
    now_ax = axes[r_idx]
    tax = ternary.TernaryAxesSubplot(scale = 1, ax = now_ax)
    tax.boundary(linewidth=2.0)
    tax.get_axes().axis('off')
    tax.clear_matplotlib_ticks()


    tem_ticks = [0.2*qw for qw in range(6)]
    tax.ticks(ticks=tem_ticks, multiple = 0.2, linewidth = 1, offset = 0.035, tick_formats = "%.1f",fontsize = tick_size)


    tax.left_axis_label(r"$\tilde{Q}(d_{i,Germany})$", fontsize=fontsize, offset=label_margin)
    tax.bottom_axis_label(r"$\tilde{Q}(d_{i,USA})$", fontsize=fontsize, offset=label_margin)
    tax.right_axis_label(r"$\tilde{Q}(d_{i,China})$", fontsize=fontsize, offset=label_margin)
    tax._redraw_labels()

    xs = []
    ys = []
    zs = []
    cs = []
    ns = []

    for i in m_in.keys():
        try:
            tem_x = Q[Q_call[i][power_list[0]]]
        except:
            #print(i,"tem_x")
            tem_x = 1
        try:
            tem_y = Q[Q_call[i][power_list[1]]]
        except:
            #print(i, "tem_y")
            tem_y = 1
        try:
            tem_z =  Q[Q_call[i][power_list[2]]]
        except:
            #print(i, "tem_z")
            tem_z = 1

        xs.append(tem_x)
        ys.append(tem_y)
        zs.append(tem_z)
        if r_idx == 0:
            now_cs = math.log(sum_in[i]/m_in[i])
        elif r_idx == 1:
            now_cs = math.log(sum_out[i]/m_out[i])
        elif r_idx == 2:
            now_cs = math.log(sum_out[i]*m_in[i]/(m_out[i]*sum_in[i]))
        cs.append(now_cs)
        ns.append(i)

    max_x = max(xs)
    max_y = max(ys)
    max_z = max(zs)
    data_point = []
    for i in range(len(xs)):
        tem_sum =xs[i] + ys[i] + zs[i]

        xs[i] /= tem_sum
        ys[i] /= tem_sum
        zs[i] /= tem_sum

        data_point.append([xs[i],ys[i],zs[i]])

    now_vmax = max(cs)
    now_vmin = min(cs)
    if r_idx == 2:
        now_vmax = 0.3
        now_vmin = -0.3
    print (len(cs),now_vmin,now_vmax)

    now_cmap = mpl.colormaps['RdYlBu']
    tax.scatter(data_point, alpha=0.9,c = cs, cmap = now_cmap, s = 100,edgecolors= "black",linewidth = 1,vmax=  now_vmax,vmin = now_vmin)

    sm = plt.cm.ScalarMappable(cmap=now_cmap, norm=plt.Normalize(vmin = now_vmin, vmax=now_vmax))
    sm._A = []
    norm = mpl.colors.Normalize(vmin = now_vmin, vmax = now_vmax)
    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=now_cmap),orientation='vertical', shrink = 0.9, pad = 0.1, ax = axes[r_idx])
    cbar.ax.tick_params(labelsize=tick_size)

    pads = 40
    if r_idx == 0:
        cbar.set_label(r'$ln(r_{i}^{in})$', fontsize = fontsize, rotation = 270,labelpad = pads)
    elif r_idx == 1:
        cbar.set_label(r'$ln(r_{i}^{out})$', fontsize = fontsize, rotation = 270,labelpad = pads)
    elif r_idx == 2:
        cbar.set_label(r'$ln(R_{i})$', fontsize = fontsize, rotation = 270,labelpad = pads)

x_pos = 0.025
y_pos = 0.95

axes[0].text(0.025, 0.95, "a", transform=axes[0].transAxes, fontsize=fontsize*2.0, va='top' ,weight='bold')
axes[1].text(0.025, 0.95, "b", transform=axes[1].transAxes, fontsize=fontsize*2.0, va='top' ,weight='bold')
axes[2].text(0.025, 0.95, "c", transform=axes[2].transAxes, fontsize=fontsize*2.0, va='top' ,weight='bold')


plt.tight_layout(rect=(0,0.05,1,1),w_pad = -2)
plt.savefig("../figure/paper/ternary.svg",dpi = 600)
plt.show()