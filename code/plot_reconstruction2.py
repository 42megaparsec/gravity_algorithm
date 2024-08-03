import matplotlib.pyplot as plt
import pickle as pk
def plot_data(dat_name, names, max_idx, ax, max_lines):
    for tem_idx in range(max_idx):
        filename = f"../result/{dat_name}/Reconst_{tem_idx}.txt"
        f = open(filename,"rb")
        now_perf = pk.load(f)

        xs = [qw*0.05 for qw in range(len(now_perf))]
        ys = now_perf[:]
        if dat_name == "ITN2019":
            ax.plot(xs[:9], ys[:9], label=names[tem_idx])
        else:
            ax.plot(xs, ys, label=names[tem_idx])

label_size = 18

# Create figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Plot data for the first dataset
dat_name1 = "ITN-model"
names1 = [r"$m$",r"$S$",r"$GDP$"]
plot_data(dat_name1, names1, 2, ax1, 19)
ax1.set_xlabel('proportion of validation set', fontsize=label_size)
ax1.set_ylabel(r"$SSI$", fontsize=label_size)
ax1.legend(fontsize=label_size)
#ax1.set_title(dat_name1)

# Plot data for the second dataset
dat_name2 = "ITN2019"
names2 = [r"$m$",r"$S$",r"$GDP$"]
plot_data(dat_name2, names2, 3, ax2, 11)
ax2.set_xlabel('proportion of validation set', fontsize=label_size)
ax2.set_ylabel(r"$SSI$", fontsize=label_size)
ax2.set_xticks([i * 0.1 for i in range(5)])
ax2.legend(fontsize=label_size)
#ax2.set_title(dat_name2)

ax1.text(-0.15, 1.05, "a", transform=ax1.transAxes, fontsize=1.5*label_size, va='top' ,weight='bold')
ax2.text(-0.15, 1.05, "b", transform=ax2.transAxes, fontsize=1.5*label_size, va='top' ,weight='bold')

# Adjust layout and data the figure
plt.tight_layout()
plt.savefig("../figure/paper/R2.pdf", dpi=300)
plt.show()