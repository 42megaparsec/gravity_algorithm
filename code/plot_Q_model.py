import matplotlib.pyplot as plt
import pickle as pk
import modules as md

name1 = "ITN"
name2 = "ITN-model"
each_bin = 500

f = open("../data/" + name1 + "_dis.txt","rb")
dist_data = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

fol_name = "../result/" + name2

f = open(fol_name + "/Q_bin_" + str(each_bin) + "_true.txt", "rb")
q_bin = pk.load(f)
f.close()

f = open(fol_name + "/Q_result_" + str(each_bin) + "_true.txt", "rb")
Q_hist_real = pk.load(f)
f.close()

label_font = 20
tick_font = 18

bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]

markers = ['s','^','o','','']
line_styles =  ['','','','--','--']
line_colors = ['#228B22','#4169E1','#8A2BE2','#D2691E','k']

legends = [r"$\bar{Q}(d;n=1)$", r"$\bar{Q}(d;n=2)$", r"$\bar{Q}(d;n=5)$", r"$\bar{Q}_{S}(d)$", r"$\tilde{Q}(d)$"]

plt.figure(figsize = (8,6))

xs = [bin_mid[qwe]/100 for qwe in range(len(bin_mid))]
ys = [1 for qwd in range(len(xs))]
plt.plot(xs,ys,markersize = 7,marker='o',linestyle = '',color = '#A52A2A',
         markerfacecolor='none', markeredgewidth = 1.5, label = r"$\bar{Q}(d;n=0)$", linewidth  = 5)


#Qs from my model
for i, iter_num in enumerate([1,2,5]):
    m_in, m_out, Q_hist, Q_std = md.calculate_mass(od_data, q_bin, iter_step=iter_num)
    plt.plot(xs, Q_hist, markersize=8, marker=markers[i], linestyle=line_styles[i], color=line_colors[i],
             markerfacecolor='none', markeredgewidth=1.7, label=legends[i])
#Q from strength model
sum_in, sum_out, Q_hist, Q_std = md.calculate_sums(od_data, q_bin)

max_Q_S = max(Q_hist)
for i in range(len(Q_hist)):
    Q_hist[i] /= max_Q_S


plt.plot(xs, Q_hist, markersize=8, marker=markers[3], linestyle=line_styles[3], color=line_colors[3],
             markerfacecolor='none', markeredgewidth=1.7, label=legends[3])
plt.plot(xs, Q_hist_real, markersize=8, marker=markers[4], linestyle=line_styles[4], color=line_colors[4],
             markerfacecolor='none', markeredgewidth=1.7, label=legends[4])


plt.yscale('log')
plt.yticks([0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], fontsize = tick_font)
plt.xticks(fontsize = tick_font)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.1f}'.format(x) for x in current_values])

plt.xlabel('d (100km)',style='italic',fontsize = label_font)
plt.ylabel('Q(d)', style='italic',fontsize = label_font)

plt.legend(fontsize = tick_font)
plt.tight_layout()
plt.savefig("../figure/paper/model_Q.svg",dpi = 300)
plt.show()