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

# -- Default material list
first_material = ['CuBe', 'NiCrAl', 'Al']
second_material = ['TAV6','Al']
third_material = ['TAV6','Al']

# Title the app
st.title('Graphic interface for High Pressure Cell calculation')

st.markdown("""
 * Use the menu at left to select parameters
 * List of the cells will appear below
""")




# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Cell Parameters')
Pressure_max = st.sidebar.slider('Maximal Pressure (kbar)', 5.0, 20.0, 7.0)  # min, max, default
In = st.sidebar.slider('Diameter of sample channel', 3.0, 8.0, 6.0)  # min, max, default
OD = st.sidebar.slider('Diameter of the cell', 10.0, 100.0, 46.0)  # min, max, default



first = st.sidebar.selectbox('Select inner material', first_material)
second = st.sidebar.selectbox('Select second material', second_material)
third = st.sidebar.selectbox('Select third material', third_material)

str_t0 = st.sidebar.text_input('Energy, meV', '5')    
t0 = float(str_t0)

K = OD/In


st.write('K=a/b', K)
st.write('K=a/b', K)


with _lock:
#    fig4 = hq.plot()
 #   ax = fig4.gca()
  #  fig4.colorbar(label="Normalised energy", vmax=vmax, vmin=0)
   # ax.grid(False)
    #ax.set_yscale('log')
    #ax.set_ylim(bottom=15)
    #st.pyplot(fig4, clear_figure=True)

     Total = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    
     df = pd.DataFrame(
#           np.random.randn(3, 3),
           data=Total,
           columns=('CuBe/TAV6', 'CuBe/Al', 'NiCrAl/Al'),
           index=('Inner diameter', 'Outer diameter', 'K=a/b'))
#          columns=('CuBe/TAV6', 'CuBe/Al', 'NiCrAl/Al'))
#           columns=('cola %d' % i for i in range(5)))
st.table(df)    
  


    #arr = np.random.normal(1, 1, size=100)
    #fig4 = plt.figure()
    #plt.hist(arr, bins=20)
   # #st.plotly_chart(fig4)
    #st.pyplot(fig4, clear_figure=True)


      
 

