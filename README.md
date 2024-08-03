# Gravity Model Project

## Overview
This project contains the code and data used in my research on gravity models in international trade networks. The project is organized into various Python scripts, data files, result files, and figures that help in analyzing and visualizing the network's properties and behaviors.

## Setup
To set up the environment, install the required dependencies using the following command:

```bash
pip install -r requirements.txt

Files and Directories

Code Directory

-main.py: Uses functions from modules.py to calculate and output the mass of each node and the deterrence function in file format.
-modules.py: A collection of necessary functions used throughout the project.
-map_plot.py, map_plot2.py: Plot geographic distributions (Figure 4 and Figure S2).
-model_network.py: Contains network model functions.
-plot_flow_hist.py: Produces distribution graphs of the actual data (Figure S1).
-plot_ITN_flow.py: Compares actual and reconstructed flows of the trade network (Figure 2).
-plot_MS_ITN.py, plot_MS_model.py: Generate comparison figures of the model network's deterrence function, mass, and strength (Figure 1).
-plot_Q_ITN.py: Generates the deterrence function of the actual trade network (Figure 2).
-plot_Q_model.py: Generates the deterrence function of the model network (Figure 1).
-plot_reconstruction.py, plot_reconstruction2.py: Validate the results (Figure S3).
-plot_ternary.py: Generates ternary plots (Figure 4).
-print_table.py: Outputs key attributes of each country (Supplement Table 1).


Data Directory

-ne_110m_admin_0_countries: Data files used by Geopandas to represent the world map.
-GDP_pk.txt: A dictionary of each country's GDP for the year 2019.
-ITN2019_flow.txt, ITN-model_flow.txt: Double dictionaries containing the flow volumes of the actual and model networks, respectively, in the format flow[st][ed] = volume.
-ITN_cont.txt: Information about which continent each country belongs to.
-ITN_pos.txt: A dictionary of the centroid positions of each country.
-ITN_dis.txt: A double dictionary of geodesic distances between the centroids of countries.