import streamlit as st
import pandas as pd
import numpy as np


#echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
import matplotlib.pyplot as plt



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
#st.write('K=a/b', K)

Attenuation_length = np.random.randn(3,4)
Attenuation_length[0,0]=  0.09885926    #Attenuation length TAV6 5.1 meV
Attenuation_length[1,0]=  0.06022102    #Attenuation length TAV6 20 meV

Attenuation_length[0,1]=  0.1089454     #Attenuation length CuBe 5.1meV
Attenuation_length[1,1]=  0.1195674     #Attenuation length CuBe 20 meV

Attenuation_length[0,2]=  0.01237508    #Attenuation length Al 5.1meV
Attenuation_length[1,2]=  0.008164399   #Attenuation length Al 20.4meV

Attenuation_length[0,3]=  0.1467938     #Attenuation length NiCrAl 5.1meV
Attenuation_length[1,3]=  0.1783196     #Attenuation length NiCrAl 20.4meV

Attenuation_length[2,0]= 896.0            #Yield strength TAV6, MPa
Attenuation_length[2,1]=  1240.0           #Yield strength CuBe, MPa
Attenuation_length[2,2]=  585.0            #Yield strength Al, MPa
Attenuation_length[2,3]=  1530.0           #Yield strength NiCrAl, MPa


df2 = pd.DataFrame(
  data=Attenuation_length,
  columns=('TAV6','CuBe','Al', 'NiCrAl'),
  index = ('Attenuation length 5.1 meV','Attenuation length 20 meV','Yield strength MPa'  ))
st.table(df2)


Alfa=np.random.randn(3)
Alfa[0]=Attenuation_length[2,1]/Attenuation_length[2,0]
Alfa[1]=Attenuation_length[2,1]/Attenuation_length[2,2]
Alfa[2]=Attenuation_length[2,3]/Attenuation_length[2,2]
#Alfa[3]=1
#st.write('Alfa', Alfa)



c=np.random.rand(3)
c=np.sqrt(np.sqrt(Alfa))*np.sqrt(In*OD)


Sigma=np.random.randn(3)
Sigma[0]=Attenuation_length[2,0] #Yield Strenght TAV6
Sigma[1]=Attenuation_length[2,2] #Yield Strenght Al
Sigma[2]=Attenuation_length[2,2] #Yield Strenght Al
#st.write('Sigma', Sigma)

P_max=np.random.randn(3)
#P_max=(S_Al/2)*(Alfa[i]*(1 - (a[k]/c[k,i])^2) + 1 - (c[k,i]/(K[k,i,j]*a[k]))^2)
P_max=(Sigma/2)*(Alfa*(1-(In/c)**2) + 1 - (c/OD)**2) 

Transmission_5= np.random.randn(3)
Transmission_5[0]=(np.exp(-Attenuation_length[0,1]*(c[0]-In)))*(np.exp(-Attenuation_length[0,0]*(OD-c[0])))
Transmission_5[1]=(np.exp(-Attenuation_length[0,1]*(c[1]-In)))*(np.exp(-Attenuation_length[0,2]*(OD-c[1])))
Transmission_5[2]=(np.exp(-Attenuation_length[0,3]*(c[2]-In)))*(np.exp(-Attenuation_length[0,2]*(OD-c[2])))
#st.write('Transmission', Transmission_5)

#*(exp(-Attenuation_length[0,0]))
#<-(exp(-A_CuBe_5*(c[k,i]-a[k])))*(exp(-A_TAV6_5*((K[k,i,j]*a[k])-c[k,i]))


Total = np.random.randn(8, 3)
Total[0,]=In
Total[1,]=c
Total[2,]=OD
Total[3,]=K
Total[4,]=P_max
Total[5,]=Transmission_5
Total[6,0]= Attenuation_length[0,1]
Total[7,]= Alfa





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
           index=('Inner diameter "a",mm', 'First material diameter "c",mm', 'Outer diameter "b",mm', 'K=a/b', 'Maximal pressure', 'Transmisson at 5 meV', 'Transmission at 20 meV', 'Alfa'))

st.table(df2)    
  


#arr = np.random.normal(1, 1, size=100)
#fig4 = plt.figure()
#plt.hist(arr, bins=20)
   # #st.plotly_chart(fig4)

#st.pyplot(fig4, clear_figure=True)

a=np.array([4,5,6,7,8,9,10])
#b=(c[0]**2)*np.sqrt((Sigma[0])/(Alfa[0]*(c[0]**2)*Sigma[0]+(c[0]**2)*Sigma[0]-(a**2)*Alfa[0]*Sigma[0]-2*Pressure_max*100*(c[0]**2)))


b=(2*a*Sigma[0]*(np.sqrt(Alfa[0])))/(Sigma[0]*(1+Alfa[0])-2*Pressure_max*100)
C=(np.sqrt(np.sqrt(Alfa[0])))*np.sqrt(a*b)
y=(a**2)*(np.exp(-Attenuation_length[0,1]*(C-a)))*(np.exp(-Attenuation_length[0,0]*(b-C)))

#y=(a**2)*(np.exp(-Attenuation_length[0,1]*(c[0]-a)))*(np.exp(-Attenuation_length[0,0]*(b-c[0])))

st.markdown('CuBe/TAV6 with analytical parameters')
#st.write('Inner diameter a=, mm',a)
st.write('Maximal pressure, kbar', Pressure_max)
st.write('Outer diameter b=(2*a*Sigma[0]*(np.sqrt(Alfa[0])))/(Sigma[0]*(1+Alfa[0])-2*Pressure_max*100)')
st.write('c=(np.sqrt(np.sqrt(Alfa[0])))*np.sqrt(a*b)')
st.write('Signal=a^2*(np.exp(-A1*(c-a)))*(np.exp(-A2*(b-c)))')

fig5 = plt.figure()
plt.plot(a,y)

st.pyplot(fig5, clear_figure=True)
st.write('Outer diameter b=, mm',b)
st.write('Ultimate P=, kbar',Pressure_max*1.3)
st.markdown("""
 * CuBe/TAV6 Gaetan Ansys calculation
 * P = 10kbar, a=6 mm, b=20 mm, c=10.5 mm
""")


b=(2*a*Sigma[1]*(np.sqrt(Alfa[1])))/(Sigma[1]*(1+Alfa[1])-2*Pressure_max*100)
C=(np.sqrt(np.sqrt(Alfa[1])))*np.sqrt(a*b)
y=(a**2)*(np.exp(-Attenuation_length[0,1]*(C-a)))*(np.exp(-Attenuation_length[0,2]*(b-C)))

#y=(a**2)*(np.exp(-Attenuation_length[0,1]*(c[0]-a)))*(np.exp(-Attenuation_length[0,0]*(b-c[0])))

st.markdown('CuBe/Al with analytical parameters')

fig6 = plt.figure()
plt.plot(a,y)
st.pyplot(fig6, clear_figure=True)
#st.write('b',b)
#st.write('Analitical C',C) 
st.write('Outer diameter b=, mm',b,a)
st.write('Ultimate P=, kbar',Pressure_max*1.3)
st.markdown("""
 * CuBe/Al Ravil Sadikov cell
 * P = 10kbar, a=8 mm, b=46 mm, c=0 mm
""")


b=(2*a*Sigma[2]*(np.sqrt(Alfa[2])))/(Sigma[2]*(1+Alfa[2])-2*Pressure_max*100)
C=(np.sqrt(np.sqrt(Alfa[2])))*np.sqrt(a*b)
y=(a**2)*(np.exp(-Attenuation_length[0,3]*(C-a)))*(np.exp(-Attenuation_length[0,2]*(b-C)))

#y=(a**2)*(np.exp(-Attenuation_length[0,1]*(c[0]-a)))*(np.exp(-Attenuation_length[0,0]*(b-c[0])))

st.markdown('NiCrAl/Al with analytical parameters')

fig7 = plt.figure()
plt.plot(a,y)
st.pyplot(fig7, clear_figure=True)
#st.write('b',b)
#st.write('Analitical C',C) 
st.write('Outer diameter b=, mm',b)
st.write('Ultimate P=, kbar',Pressure_max*1.3)
st.markdown("""
 * NiCrAl/Al PC2 Ravil Sadikov cell
 * P = 10kbar, a=8 mm, b=46 mm, c=11.5 mm
""")
Alf=1
b=(2*a*Attenuation_length[2,2]*(np.sqrt(Alf)))/(Attenuation_length[2,2]*(1+Alf)-2*Pressure_max*100)
C=(np.sqrt(np.sqrt(Alf)))*np.sqrt(a*b)
y=(a**2)*(np.exp(-Attenuation_length[0,2]*(C-a)))*(np.exp(-Attenuation_length[0,2]*(b-C)))

#y=(a**2)*(np.exp(-Attenuation_length[0,1]*(c[0]-a)))*(np.exp(-Attenuation_length[0,0]*(b-c[0])))

st.markdown('Al/Al with analytical parameters')

fig8 = plt.figure()
plt.plot(a,y)
st.pyplot(fig8, clear_figure=True)
#st.write('b',b)
#st.write('Analitical C',C) 
st.write('Outer diameter b=, mm',b)
st.write('Ultimate P=, kbar',Pressure_max*1.3)
st.markdown("""
 * Al/Al PC1 Ravil Sadikov cell
 * P = 12kbar, a=8 mm, b=55 mm, c=0 mm
""")
