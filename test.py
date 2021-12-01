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
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

@st.cache(ttl=3600, max_entries=10)   #-- Magic command to cache data
def load_gw(t0, detector, fs=4096):
    strain = TimeSeries.fetch_open_data(detector, t0-14, t0+14, sample_rate = fs, cache=False)
    return strain

#@st.cache(ttl=3600, max_entries=10)   #-- Magic command to cache data
#def get_eventlist():
 #   allevents = datasets.find_datasets(type='events')
  #  eventset = set()
   # for ev in allevents:
    #    name = fetch_event_json(ev)['events'][ev]['commonName']
     #   if name[0:2] == 'GW':
      #      eventset.add(name)
    #eventlist = list(eventset)
    #eventlist.sort()
    #return eventlist
    
st.sidebar.markdown("## Select Data Time and Detector")

# -- Get list of events
# eventlist = get_eventlist()

