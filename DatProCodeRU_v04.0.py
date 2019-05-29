# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:07:40 2019

@author: Anu Nair (nyke.anu@gmail.com)


"""

# Load the required packages
import pandas as pd

import matplotlib.pyplot as plt
#from scipy.signal import argrelextrema
from scipy.signal import find_peaks

#import numpy as np
#import time 
import winsound
#import pyttsx3

#
def DataSort(filename,flty,c_name):
      #Getting data from the file and extracing a particular data from it
      print("Opening file ",filename)
      print('Calculating ',c_name)

      if flty=='Qx' :
            data=[]
            reader = pd.read_csv(filename,skiprows =[i for i in range(37)],dtype=object,delimiter="\t")
            reader.columns=['ST_2.4kHz', 'ST_50Hz', 'PT_K1', 'PT_K3','RUN-UP_8','RUN-UP_9','IWP','LC_1','LC_2','ST_2.4KHz','PT_SW1','PT_SW2','PT_SW3','PT_SW4','PT_K2','PT_K4','PT_K5','PT_K6','19']

            data=pd.to_numeric(reader[c_name], errors='coerce').fillna(0, downcast='infer')

            #ti=[i/2400 for i in data.index]
            print("----------------------------Complete file preview--------------------------")
            print(reader.head())
            print("-----------------------------Current data preview-------------------------- ")
            print(data.head())
            print("____________________________Done reading data______________________________")

            return(data)

def PeakFinder(dat,tr_hd,tr_dis):
      print('threshold (y)= ',tr_hd,'[mm]')
      print('threshold (y)= ',scaleUp_std(tr_hd,3),'[bar]')
      print('threshold (x)= ',tr_dis,'samples')
#      scale_fac=9.81*1025/1000/1000/100
#      tr_hd=tr_hd/scale_fac


      #find out peak and mean values frm the file

      df = pd.DataFrame(dat.values, columns=['data'])
#      fig = plt.figure(1)
#      plt.plot(df.index, df['data'])
      df['time']=[i/2400 for i in dat.index]

      #print(df)
      #n=8000 # number of points to be checked before and after 
      # Find local peaks
      #df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
      #df['max'] = df.iloc[argrelextrema(df.data.values, np.greater_equal, order=n)[0]]['data']
      df['max'] = df.iloc[find_peaks(df.data.values, height=tr_hd,distance=tr_dis)[0]]['data']
      
      df=df.dropna()  # drop nan from the dataframe
      print("--------------------------------Peaks preview----------------------------- ")
      print(df.head())
      print("number of peaks = ",df.shape[0])
      print("-------------------------------------------------------------------------- ")


      return(df)
      
def scaleUp_std(df,ttype):
      scale_fac=90
      if ttype==1:
            #for pressure transducers 
            
            data=df['data']*scale_fac/1000  #in bar
            print ('Scale factor = ',scale_fac)

            print("------------------------sacled data preview------------------------------- ")
            print(data.head(10))
            return(data)

      if ttype==3:
            #scale up of single data 

              #in bar
            return((df/1000)*scale_fac)

def MeanNPeak(df,datum) :
      dat=scaleUp_std(df,1)

      #find the mean and peak of the given data series 
      import statistics as stat
      sort_dat=dat.sort_values(ascending=False) 

      SignOfPeaks='NA'#stat.mean(sort_dat[0:round(sort_dat.size/3)]) - scaleUp_std(datum,3) # mean of the data 
      #LNoOfOcc=stat.mode(dat)# value that occuring maximum time
      MaxVal=max(dat)-scaleUp_std(datum,3) # highest peak value among the peaks 
      meanOf='NA'#(stat.mean(dat)-scaleUp_std(datum,3))
      #display results 
      print("------------------scaled data preview(from intit)------------------------- ")
      print("--------------------function MeanNpeak results---------------------------- ")
      print('maximum of peak              :',MaxVal,'m')
      print('avarage of the peaks         :',meanOf,'m')
      print('significant of peaks         :',SignOfPeaks,'m')
      #print('value occuring most          : ',LNoOfOcc)

      print("---------------------------------END-------------------------------------- ")
      print("-------------------------------------------------------------------------- ")
      #plt.figure(2)
      #plt.plot(dat)
      #plt.show()
      
      return([SignOfPeaks,meanOf,MaxVal])


if __name__== "__main__":

      import sys
      from pandas import ExcelWriter
#      

      ###################################################################################
      
#      fl_name=["Results/Ballast/B_360/S7.ASC"]
#      fl_out='Results/Ballast/B_360/PressureTransducers/S7.out'
      
#      fl_name=["FullLoad/FL_180/S2.asc"]

      fl_out='XSP8'


#      sys.stdout = open(fl_out,'wt')
#      pt_name=['PT_K4']
      f = open('FileName.dat')
#      line = f.readline()
      outD=[['file','sensor','datum','cutoffht','Cutoffbar','cutoffq','Significant','Avarage','Mmax']]
      for line in f:
            line = line.strip('\n')
            fl_name=line


      
            ###################################################################################
#            if input('Password: ')!='*****':
#      
#                  winsound.Beep(440,2000)
#                  sys.exit()
                  
            print("###########################################################################")
            print("##                             FPSO ANALYSIS                            ###")
            print("##         ANU NAIR(Guide: PROF.VAS)   IIT MADRAS, INDIA                ###")
            print("###########################################################################")
      
            print ("\n") 
            import datetime
            now = datetime.datetime.now()
            print ("Current date and time : ")
            print (now.strftime("%Y-%m-%d %H:%M:%S"))
            
            print ("___________________________________________________________________________") 
      
            print ("___________________________________________________________________________")  
            
           
            pt_name=['RUN-UP_8' ,'RUN-UP_9']
      
      #      fl_name=['QX/S1.txt','QX/S2.txt','QX/S3.txt','QX/S4.txt','QX/S5.txt','QX/S6.txt','QX/S7.txt','QX/S8.txt'] 
      
            qtxt1='check in file ' + fl_name
            qtxt2='check out file ' + fl_out
            
      
#            if input(qtxt1)=='****':exit()
#       
#            if input(qtxt2)=='****':exit()
            j=fl_name
            for i in pt_name:
                  datum= 0
                  cutoffht=0
                  cutoffq=25

                  data=DataSort(fl_name,"Qx",i)
                  
                  
#                  plt.plot(data)
                  

                  df=PeakFinder(data,cutoffht,cutoffq)

                  while df.shape[0]==0:
                        fig = plt.figure(num=None, figsize=(20, 8), dpi=80, facecolor='w', edgecolor='k')

                        plt.plot(data)
                        plt.pause (20)
                        datum=float(input("Datum = "))

                        cutoffht=float(input("thd-Y = "))

                        df=PeakFinder(data,cutoffht,cutoffq)
                        plt.close()
#                  plt.scatter(df.index, df['max'], c='g')
#                  plt.xlabel('index')
#                  plt.ylabel('Pressure[mm]')
#                  plt.title('Pressure record time series')
#                  plt.grid(True)
#
#                  plt.show()
#                  plt.draw()
#
#
#
#                  plt.pause(10)
#                  winsound.Beep(440,300)
#
#
#
#                  while input("need more time? [enter] ")=='':
#
#                        plt.pause(10)
#                        winsound.Beep(440,300)     
#                        
#
#
#
#
#                  plt.close()
#
#                  
#
#
#                  chk=input("change controls? [enter] ")
#                  
#                  while chk=='':
#                        datum=float(input("Datum = "))
#
#                        cutoffht=float(input("thd-Y = "))
##                        cutoffq=float(input("thd-x = "))
#                        print ("initial value  " ,datum) 
#                        df=PeakFinder(data,cutoffht,cutoffq)
#                        fig = plt.figure(num=None, figsize=(20, 8), dpi=80, facecolor='w', edgecolor='k')
#                        plt.plot(data)
#
#                        plt.scatter(df.index, df['max'], c='g')
#                        plt.xlabel('index')
#                        plt.ylabel('Pressure[mm]')
#                        plt.title('Pressure record time series')
#                        plt.grid(True)
#
#                        plt.show()
#                        plt.draw()
#
#
#                        plt.pause(10)
#                        winsound.Beep(440,300)
#
#
#                        while input("need more time? [enter] ")=='':
#
#                              plt.pause(10)
#                              winsound.Beep(440,300)
#                        plt.close()
#
#
#                        chk=input("change controls? [enter] ")




                  [S,A,M]=MeanNPeak(df,datum)
                  print('datum','cutoffht','Cutoffbar','cutoffq','Significant','Avarage','Mmax')
                  print(datum,cutoffht,scaleUp_std(cutoffht,3),cutoffq,S,A,M)



                  outD.append([j,i,datum,cutoffht,scaleUp_std(cutoffht,3),cutoffq,S,A,M])
#                  Endtxt=i+' is done !!. Any notes? '
#
#                  print('Note: ',input(Endtxt))
                  winsound.Beep(240,400)
#                  flag=input("***********NEXT SENSOR? [enter to continue/**** to break]")
#                  if flag =='****': 
#                        winsound.Beep(440,2000)
#                        break    

                  
                  

                  print ("-----------------------------End of the probe r----------------------------")
                  print ("___________________________________________________________________________")
                  writer = ExcelWriter(fl_out + i + '.xlsx')
                  df.value['max'].to_excel(writer,'Sheet1')
                  writer.save()

      f.close()
      
      if (input('Save? ') == ''):
            Daat=pd.DataFrame(outD)

            writer = ExcelWriter(fl_out + '.xlsx')
            Daat.to_excel(writer,'Sheet1')
            writer.save()
      print ("-----------------------------End of the program----------------------------")
      print ("___________________________________________________________________________")




