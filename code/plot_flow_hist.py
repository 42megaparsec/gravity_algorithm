import pickle as pk
import os
import matplotlib.pyplot as plt
import numpy as np

now_size = 18
tick_size = 13

def log_binning(data, base=10):
    # 최소값과 최대값을 계산
    min_val = np.min(data)
    max_val = np.max(data)

    # 최소값과 최대값이 양수가 아니라면 log_binning을 적용할 수 없음
    if min_val <= 0 or max_val <= 0:
        raise ValueError("All data must be positive for log binning.")

    # bin 경계를 로그 스케일로 계산
    log_min = np.log(min_val) / np.log(base)
    log_max = np.log(max_val) / np.log(base)
    bins = np.logspace(log_min, log_max, num=int(log_max - log_min) + 1, base=base)

    # np.histogram을 사용하여 bin counts를 계산
    counts, bin_edges = np.histogram(data, bins=bins)

    return bin_edges, counts

name1 = "ITN"
name2 = "ITN2019"
each_bin = 500

f = open("../data/" + name2 + "_flow.txt", "rb")
stt_end2 = pk.load(f)
f.close()

data = []
data2 = []
now_data = stt_end2

for i in now_data.keys():
    for j in now_data[i].keys():
        if now_data[i][j] > 0:
            data2.append(np.log(abs(now_data[i][j])))
            data.append(now_data[i][j])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # 10x5 inches figure size, for example
plt.subplots_adjust(left = 0.1, bottom= 0.15, right=0.98, top=0.9, wspace=0.3, hspace=0.1)

counts, bins  = np.histogram(data, density = 1)
ax1.plot(bins[:-1], counts)
#plt.yscale('log')
#plt.xlabel(r'$ln(f_{ij})$', fontsize = now_size)
#plt.ylabel(r'$ln(p(f_{ij}))$', fontsize = now_size)
ax1.set_xlabel(r'$f_{ij}$', fontsize = now_size)
ax1.set_ylabel(r'$p(f_{ij})$', fontsize = now_size)

counts, bins = np.histogram(data2, density=1)
ax2.plot(bins[:-1], counts)
ax2.set_yscale('log')  # Set y-axis to log scale
ax2.set_xlabel(r'$\ln(f_{ij})$', fontsize=now_size)
ax2.set_ylabel(r'$\ln(p(f_{ij}))$', fontsize=now_size)
#ax2.set_title('(b)', loc='left')  # Title on the top-left as label

ax1.tick_params(axis='both', which='major', labelsize=tick_size)
ax2.tick_params(axis='both', which='major', labelsize=tick_size)

ax1.xaxis.get_offset_text().set_fontsize(tick_size)
ax1.yaxis.get_offset_text().set_fontsize(tick_size)

# ax1.text(0.07, 0.9, "(a)", transform=ax1.transAxes,
#                                     fontsize=now_size)
# ax2.text(0.07, 0.9, "(b)", transform=ax2.transAxes,
#                                     fontsize=now_size)

ax1.text(-0.18, 1.1, "a", transform=ax1.transAxes, fontsize=1.8*now_size, va='top' ,weight='bold')
ax2.text(-0.18, 1.1, "b", transform=ax2.transAxes, fontsize=1.8*now_size, va='top' ,weight='bold')


plt.savefig("../figure/paper/flow_hist.pdf",dpi = 600)
plt.show()