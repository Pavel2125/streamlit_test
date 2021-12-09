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
Attenuation_length = np.random.randn(2,4)
Attenuation_length[0,0]=  0.09885926    #Attenuation length TAV6 5.1 meV
Attenuation_length[1,0]=  0.06022102    #Attenuation length TAV6 20 meV
Attenuation_length[0,1]=  0.1089454     #Attenuation length CuBe 5.1meV
Attenuation_length[1,1]=  0.1195674     #Attenuation length CuBe 20 meV
Attenuation_length[0,2]=  0.01237508    #Attenuation length Al 5.1meV
Attenuation_length[1,2]=  0.008164399   #Attenuation length Al 20.4meV
Attenuation_length[0,3]=  0.1467938     #Attenuation length NiCrAl 5.1meV
Attenuation_length[1,3]=  0.1783196     #Attenuation length NiCrAl 20.4meV
  
  
Total = np.random.randn(6, 3)
Total[0,]=In
Total[1,]=OD
Total[2,]=K
Total[3,]=Pressure_max
st.write('K=a/b', K)
#st.write('K=a/b', K)

df2 = pd.DataFrame(
  data=Attenuation_length,
  columns=('TAV6','CuBe','Al', 'NiCrAl'),
  index = ('Attenuation length 5.1 meV','Attenuation length 20 meV'))
  
  
 
st.table(df2)

Total[5,0]= Attenuation_length[0,1]
#*(exp(-Attenuation_length[0,0]))
#<-(exp(-A_CuBe_5*(c[k,i]-a[k])))*(exp(-A_TAV6_5*((K[k,i,j]*a[k])-c[k,i]))

with _lock:
#    fig4 = hq.plot()
 #   ax = fig4.gca()
  #  fig4.colorbar(label="Normalised energy", vmax=vmax, vmin=0)
   # ax.grid(False)
    #ax.set_yscale('log')
    #ax.set_ylim(bottom=15)
    #st.pyplot(fig4, clear_figure=True)



    
     df2 = pd.DataFrame(
        data=Total,
           columns=('CuBe/TAV6', 'CuBe/Al', 'NiCrAl/Al'),
           index=('Inner diameter', 'Outer diameter', 'K=a/b', 'Maximal pressure', 'Transmisson at 5 meV', 'Transmission at 20 meV'))
#          columns=('CuBe/TAV6', 'CuBe/Al', 'NiCrAl/Al'))
#           columns=('cola %d' % i for i in range(5)))
st.table(df2)    
  


    #arr = np.random.normal(1, 1, size=100)
    #fig4 = plt.figure()
    #plt.hist(arr, bins=20)
   # #st.plotly_chart(fig4)
    #st.pyplot(fig4, clear_figure=True)


      
 

