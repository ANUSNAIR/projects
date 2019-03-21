# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:07:40 2019

@author: Anu Nair (nyke.anu@gmail.com)


"""

# Load the required packages
import pandas as pd

#import matplotlib.pyplot as plt
#from scipy.signal import argrelextrema
from scipy.signal import find_peaks

#import numpy as np
#import time 




#
def DataSort(filename,flty,c_name):
      #Getting data from the file and extracing a particular data from it
      print("Opening file ",filename)



      if flty=='Qx' :
            data=[]
            reader = pd.read_csv(filename,skiprows =[i for i in range(37)],dtype=object,delimiter="\t")
            reader.columns=['ST_2.4kHz', 'ST_50Hz', 'PT_K1', 'PT_K3','RP_8','RP_9','IWP','LC_1','LC_2','ST_2.4KHz','PT_SW1','PT_SW2','PT_SW3','PT_SW4','PT_K2','PT_K4','PT_K5','PT_K6','19']



            data=pd.to_numeric(reader[c_name], errors='coerce').fillna(0, downcast='infer')



            #ti=[i/2400 for i in data.index]
            print("----------------------------Complete file preview--------------------------")
            print(reader.head())
            print("-----------------------------Current data preview-------------------------- ")
            print(data.head())
            print("____________________________Done reading data______________________________")
            




            return(data)
            









def PeakFinder(dat,tr_hd):
      print('thrushhold= ',tr_hd,'[mm]')
      print('thrushhold= ',scaleUp_std(tr_hd,3),'[bar]')
#      scale_fac=9.81*1025/1000/1000/100
#      tr_hd=tr_hd/scale_fac


      #find out peak and mean values frm the file

      df = pd.DataFrame(dat.values, columns=['data'])
      df['time']=[i/2400 for i in dat.index]







      #print(df)
      #n=8000 # number of points to be checked before and after 
      # Find local peaks
      #df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
      #df['max'] = df.iloc[argrelextrema(df.data.values, np.greater_equal, order=n)[0]]['data']
      df['max'] = df.iloc[find_peaks(df.data.values, height=tr_hd)[0]]['data']
      
      
      df=df.dropna()  # drop nan from the dataframe
      print("-----------------------------Peaks preview-------------------------- ")
      print(df.head())
      # Plot results
      #fig = plt.figure(1)
      #plt.scatter(df.index, df['min'], c='r')
      #plt.scatter(df.index, df['max'], c='g')
      #plt.plot(df.index, df['data'])

      #plt.xlabel('index')
      #plt.ylabel('Pressure[kPa]')
      #plt.title('Pressure record time series')
      #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
      #plt.axis([0, 144000, 0, 1000])
      #plt.grid(True)
      #plt.show()
      #fig.savefig('test.pdf')

      return(df)
      
def scaleUp_std(df,ttype):
      
      if ttype==1:
            #for pressure transducers 
            scale_fac=90
            data=df['data']*9.81*1025/1000*scale_fac/1000/100   #in bar
            print("------------------------sacled data preview------------------------------- ")
            print(data.head(10))
            return(data)
      if ttype==2:
            #for loadcells      

            data=df['data']*9.81*1025/1000*scale_fac/1000   #in KPa
            print("------------------------sacled data preview------------------------------- ")
            print(data.head())
            return(data)
      if ttype==3:
            #for scale up the time
            scale_fac=90
              #in bar
            return(df*9.81*1025/1000*scale_fac/1000/100)
            


def MeanNPeak(df) :
      dat=scaleUp_std(df,1)

      #find the mean and peak of the given data series 
      import statistics as stat
      sort_dat=dat.sort_values(ascending=False) 

      SignOfPeaks=stat.mean(sort_dat[0:round(sort_dat.size/3)]) # mean of the data 
      #LNoOfOcc=stat.mode(dat)# value that occuring maximum time
      MaxVal=max(dat) # highest peak value among the peaks 
      #display results 
      print("------------------------sacled data preview------------------------------- ")
      print("--------------------function MeanNpeak results---------------------------- ")
      print('maximum of peak              :',MaxVal,'bar')
      print('avarage of the peaks         :',stat.mean(dat),'bar')
      print('significant of peaks         :',SignOfPeaks,'bar')
      #print('value occuring most          : ',LNoOfOcc)

      print("---------------------------------END-------------------------------------- ")
      print("-------------------------------------------------------------------------- ")
      #plt.figure(2)
      #plt.plot(dat)
      #plt.show()




      



if __name__== "__main__":
      import sys
      sys.stdout = open('270.out','wt')
      
      print("###########################################################################")
      print("##                             FPSO ANALYSIS                            ###")
      # print("##         ANU NAIR(Guide: PROF.VAS)   IIT MADRAS, INDIA                ###")
      print("###########################################################################")

      print ("\n") 
      import datetime
      now = datetime.datetime.now()
      print ("Current date and time : ")
      print (now.strftime("%Y-%m-%d %H:%M:%S"))


      print ("___________________________________________________________________________")   
      pt_name=['PT_K1','PT_K3','PT_SW1','PT_SW2','PT_SW3','PT_SW4','PT_K2','PT_K4','PT_K5']
      fl_name=['QX/S1.txt','QX/S2.txt','QX/S3.txt','QX/S4.txt','QX/S5.txt','QX/S6.txt','QX/S7.txt','QX/S8.txt']      
      for j in fl_name:      
            for i in pt_name:
                  print('Calculating ',i)
                  data=DataSort(j,"Qx",i)
                  #scaleUp_std()
                  #plt.plot(data.index,data)
                  df=PeakFinder(data,0)
                  MeanNPeak(df)

            
      print ("-----------------------------End of the program----------------------------")
      print ("___________________________________________________________________________")

      #%logstart -o


