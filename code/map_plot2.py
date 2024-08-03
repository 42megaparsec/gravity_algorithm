# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import pickle as pk
import math
import modules as md

each_num = 500

pre_name = "ITN"
year = 2019

now_line_width = 0.3
now_fontsize = 18

convert_name = {'Korea, Republic of':'South Korea',"United States of America":'United States','Viet Nam':'Vietnam',"Hong Kong China":"Hong Kong", "Macedonia, North":'Macedonia (FYROM)','Russian Federation':'Russia',
                "Brunei Darussalam": 'Brunei',"Macedonia": "North Macedonia", "Côte d'Ivoire": "Ivory Coast", "Czech Republic": "Czechia"}

name1 = "ITN"
name2 = "ITN2019"
each_bin = 500

f = open("../data/" + name1 + "_dis.txt","rb")
dist_data = pk.load(f)
f.close()

f = open("../data/" + name2 + "_flow.txt", "rb")
od_data = pk.load(f)
f.close()

f = open("../data/ITN_pos.txt", "rb")
pos_dic = pk.load(f)
f.close()

q_bin = md.create_q_bin(od_data, dist_data, each_num=each_bin)
m_in, m_out, Q, Q_std_m = md.calculate_mass(od_data, q_bin, iter_step=5)
sum_in, sum_out, Q_S, Q_std_S = md.calculate_sums(od_data, q_bin)

bin_mid = q_bin["bin_mid"]
Q_call = q_bin["call_dic"]

def plotCountryPatch( axes, country_name, fcolor ):
    if country_name == 'USA':
        country_name = 'United States of America'
    if country_name == 'Czech Republic':
        country_name = 'Czechia'
    if country_name == 'Dominican Republic':
        country_name = 'Dominican Rep.'
    if country_name == 'Congo (DRC)':
        country_name = 'Dem. Rep. Congo'
    if country_name == 'Myanmar (Burma)':
        country_name = 'Myanmar'
    if country_name == "URK":
        country_name = "Ukraine"
    if country_name == "UK":
        country_name = "United Kingdom"
    if country_name == "Viet Nam":
        country_name = "Vietnam"
    if country_name == "Macedonia":
        country_name = "North Macedonia"


    try:
        nami = world[world.name == country_name]
        if (len(nami)) == 0:
            print ("c",country_name)

        namigm = nami.__geo_interface__['features']  # geopandas's geo_interface
        for feature in namigm:
            namig = {'type': feature['geometry']['type'], 'coordinates': feature['geometry']['coordinates']}
            axes.add_patch(PolygonPatch(namig, fc=fcolor, ec="black", alpha=1, zorder=2, linewidth=0.3))
    except:
        print ("a",country_name)


ratio_out = {}
ratio_in = {}
for i in m_in.keys():
    if m_in[i] != 0:
        ratio_in[i] = sum_in[i] / m_in[i]
    if m_out[i] != 0:
        ratio_out[i] = sum_out[i] / m_out[i]

names = ['USA', 'Germany', 'China']

# for name in names:
#     print (name)
#     print (sum_out[name]/m_out[name])
#     print (sum_in[name]/m_in[name])
#     print (sum_out[name] * m_in[name]/(m_out[name]*sum_in[name]))
#     print (m_in[name]/m_out[name])

sorted_keys_out = sorted(ratio_out, key=ratio_out.get, reverse=True)
sorted_keys_in = sorted(ratio_in, key=ratio_in.get, reverse=True)


from descartes import PolygonPatch




share_dict = {qw:math.log((sum_in[qw]/m_in[qw])) for qw in m_in.keys()}

share_list = list(share_dict.values())


norm = mpl.colors.Normalize(vmin = np.min(share_list), vmax = np.max(share_list))

colors = ["#f7770f","#1592ff"]
nodes = [0.0,1.0]

now_vmax = max(share_list)
now_vmin = min(share_list)

print (len(share_list),now_vmax,now_vmin)
cmap = plt.get_cmap('RdYlBu')

share_colors = cmap(norm(share_list))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[world.name !="Antarctica"]


base = world.plot(color ='white', edgecolor='k', linewidth = 0.3)

country_names = world['name'].unique()

exponent = 1.0

def create_map(ax, share_dict, world, cmap, norm, exponent, now_line_width, now_fontsize, label):
    base = world.plot(ax=ax, color='white', edgecolor='k', linewidth=now_line_width)
    for i in m_out.keys():
        plotCountryPatch(base, i, cmap((norm(share_dict[i])) ** exponent))
    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', shrink=0.6,
                        pad=-0.01)
    cbar.outline.set_linewidth(0.3)
    cbar.set_label(label, fontsize=now_fontsize, rotation=270, labelpad=30)
    ax.axis('off')


pdf_path = "../figure/paper/rinout_plots.pdf"

#with PdfPages(pdf_path) as pdf:
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # 두 개의 서브플롯 생성
ax1.text(0.025, 1.01, "a", transform=ax1.transAxes, fontsize=1.5*now_fontsize, va='top' ,weight='bold')
ax2.text(0.025, 1.01, "b", transform=ax2.transAxes, fontsize=1.5*now_fontsize, va='top' ,weight='bold')


norm_out = mpl.colors.Normalize(vmin=min(share_dict.values()), vmax=max(share_dict.values()))
create_map(ax1, share_dict, world, cmap, norm_out, exponent, now_line_width, now_fontsize, r'$ln(r_{i}^{ in})$')

share_dict_in = {qw: math.log((sum_out[qw] / m_out[qw])) for qw in m_out.keys() if m_in[qw] != 0}
norm_in = mpl.colors.Normalize(vmin=min(share_dict_in.values()), vmax=max(share_dict_in.values()))


create_map(ax2, share_dict_in, world, cmap, norm_in, exponent, now_line_width, now_fontsize, r'$ln(r_{i}^{ out})$')

plt.tight_layout()
plt.subplots_adjust(left = 0, right = 1.05, top = 1.05, bottom = -0.05, hspace=-0.2)  # 서브플롯 간의 수직 간격 조정

plt.savefig(pdf_path,dpi = 600)  # PDF에 저장
plt.show()