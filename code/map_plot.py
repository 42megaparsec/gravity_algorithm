# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import pickle as pk
import numpy as np
import pickle
import modules as md


now_line_width = 0.3
now_fontsize = 20

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


for i in m_out.keys():
    if i in convert_name.keys():
        i = convert_name[i]
from descartes import PolygonPatch

def plotCountryPatch( axes, country_name, fcolor ):

    if country_name in convert_name.keys():
        country_name = convert_name[country_name]

    if country_name == 'USA':
        country_name = 'United States of America'
    if country_name == 'Czech Republic':
        country_name = 'Czechia'
    if country_name == 'Congo (DRC)':
        country_name = 'Dem. Rep. Congo'
    if country_name == 'UK':
        country_name = 'United Kingdom'
    if country_name == 'Macedonia':
        country_name = 'North Macedonia'
    if country_name == "Côte d'Ivoire":
        country_name = 'Ivory Coast'
    if country_name == 'Myanmar (Burma)':
        country_name = 'Myanmar'
    if country_name == 'Dominican Rep.':
        country_name = 'Dominican Republic'
    if country_name == "Macedonia":
        country_name = "North Macedonia"

    try:
        nami = world[world['ADMIN'] == country_name]  # 'ADMIN' 필드를 사용하여 국가 검색
        namigm = nami.__geo_interface__['features']  # geopandas의 geo_interface
        namig0 = {'type': namigm[0]['geometry']['type'], 'coordinates': namigm[0]['geometry']['coordinates']}
        axes.add_patch(PolygonPatch(namig0, fc=fcolor, ec="black", alpha=1, zorder=1))
    except:
        print(country_name)


share_dict = {qw:np.log(sum_out[qw]*m_in[qw]/(sum_in[qw]*m_out[qw])) for qw in m_out.keys()}
share_list = list(share_dict.values())

norm = mpl.colors.Normalize(vmin = np.min(share_list), vmax = np.max(share_list))

colors = ["#f7770f","#1592ff"]
nodes = [0.0,1.0]


now_vmax = max(share_list)
now_vmin = min(share_list)

print (len(share_list),now_vmax,now_vmin)
cmap = mpl.colormaps['RdYlBu']


share_colors = cmap(norm(share_list))

world = gpd.read_file("../data/ne_110m_admin_0_countries")
world = world[world['NAME'] != 'Antarctica']
exponent = 1.0
fig, ax = plt.subplots(figsize=(15, 7.5))
world.plot(ax=ax, color='none', edgecolor='k')
plt.axis('off')

for i in m_out.keys():
    plotCountryPatch(ax, i, cmap((norm(share_dict[i]))**exponent))
cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', shrink=0.6, pad=-0.01)
cbar.outline.set_linewidth(0.3)
cbar.set_label(r'$ln(R_{i})$', fontsize=now_fontsize, rotation=270, labelpad=30)

plt.tight_layout()
plt.savefig("../figure/paper/inout.svg", dpi=800)
plt.show()