import streamlit as st
import pandas as pd
import numpy as np


#echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
import matplotlib.pyplot as plt

#x=[1,2,3,4,5]
#y=[5,4,4,3,2]
#plt.plot(x,y)
#print(x)


import requests, os
from gwpy.timeseries import TimeSeries
from gwosc.locate import get_urls
from gwosc import datasets
from gwosc.api import fetch_event_json

from copy import deepcopy
import base64

#from helper import make_audio_file

# Use the non-interactive Agg backend, which is recommended as a
# thread-safe backend.
# See https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads.
import matplotlib as mpl
mpl.use("agg")

##############################################################################
# Workaround for the limited multi-threading support in matplotlib.
# Per the docs, we will avoid using `matplotlib.pyplot` for figures:
# https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server.
# Moreover, we will guard all operations on the figure instances by the
# class-level lock in the Agg backend.
##############################################################################
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock


# -- Set page config
apptitle = 'HPC Quickview'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# -- Default detector list
detectorlist = ['H1','L1', 'V1']

# Title the app
st.title('Graphic interface for High Pressure Cell calculation')

st.markdown("""
 * Use the menu at left to select parameters
 * List of the cells will appear below
""")

# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Cell Parameters')
Pressure_max = st.sidebar.slider('Maximal Pressure (kbar)', 5.0, 20.0, 7.0)  # min, max, default
# dt = dtboth / 10.0


Pressure = st.slider ("Maximal pressure")
In = st.slider ("Diameter of sample chamber")
OD = st.slider ("Diameter of the cell")
#st.write(m.run(window= 

with _lock:
#    fig4 = hq.plot()
 #   ax = fig4.gca()
  #  fig4.colorbar(label="Normalised energy", vmax=vmax, vmin=0)
   # ax.grid(False)
    #ax.set_yscale('log')
    #ax.set_ylim(bottom=15)
    #st.pyplot(fig4, clear_figure=True)
      
    
    
  
    arr = np.random.normal(1, 1, size=100)
    fig4 = plt.figure()
    plt.hist(arr, bins=20)
   # #st.plotly_chart(fig4)
    st.pyplot(fig4, clear_figure=True)



 

