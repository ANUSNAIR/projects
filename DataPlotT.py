# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:05:53 2019

@author: Anu Nair (nyke.anu@gmail.com)


"""
import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
#from scipy.signal import argrelextrema
#from scipy.signal import find_peaks

#import numpy as np
#import time 
import math







#
def DataSort(filename,flty,c_name):
      #Getting data from the file and extracing a particular data from it



      if flty=='Qx' :
            data=[]

            reader = pd.read_csv(filename,skiprows =[i for i in range(37)],dtype=object,delimiter="\t")
            reader.columns=['ST_2.4kHz', 'ST_50Hz', 'PT_K1', 'PT_K3','RP_8','RP_9','IWP','LC_1','LC_2','ST_2.4KHz','PT_SW1','PT_SW2','PT_SW3','PT_SW4','PT_K2','PT_K4','PT_K5','PT_K6','19']



            data=pd.to_numeric(reader[c_name], errors='coerce').fillna(0, downcast='infer')
            df = pd.DataFrame(data.values, columns=['data'])




            df["time"]=[i/2400 for i in data.index]
            print("----------------------------Complete file preview--------------------------")
            print(reader.head())
            print("-----------------------------Current data preview-------------------------- ")
            print(data.head())
            print("____________________________Done reading data______________________________")





            return(df)
def DataPlotter_PT(df,fgn):
      

      



      #Function plot the file and save
      scale_fac=90*9.81*1025/1000/1000/100 #bar
      y=df['data']*scale_fac
      x=df['time']*math.sqrt(90)*1000
      xy = pd.DataFrame(x.values, columns=['x'])
      xy['y'] = pd.DataFrame(y.values, columns=['y'])

#      fig=plt.figure (fgn)


      plt.plot(x, y,linewidth=2,)#marker='^'

      plt.title('Time series plot',fontsize=28, verticalalignment='bottom')

      plt.ylabel('Pressure [bar]',fontsize=28)



      plt.xlabel('Time (ms)',fontsize=28)
      plt.tick_params(which='major', width=1.0)
      plt.tick_params(which='major', length=10)
      plt.tick_params(which='minor', width=1.0, labelsize=28)
      plt.tick_params(which='minor', length=5, labelsize=28, labelcolor='0.25')

      plt.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
#      plt.text(0.0, -0.4, "Made with http://matplotlib.org",
#        fontsize=10, ha="right", color='.5')



      plt.show()
#      fig.savefig('test1.pdf',dpi=600)
      return(xy)

      
if __name__== "__main__":
#      import sys
      plt.close()
      plt.close()
      fl_name="Results/Ballast/B_200/S6.txt"

      fl_out='Results/Ballast/B_200/PressureTransducers/Impact_S6.out'






#      sys.stdout = open(fl_out,'wt')
      df=DataSort(fl_name,"Qx",'PT_SW4')
      xy=DataPlotter_PT(df,1)
      



      
      loc=xy['y'].idxmax()
      Pmax=xy['y'][loc]
      TPmax=xy['x'][loc]
      xy1=xy[loc-15:loc+15]
      hPmax=Pmax/2



      
      

      ThPmax_Up=4863603.466718877


      ThPmax_Dn=4863609.698731208
      
      
      trise=2*(TPmax-ThPmax_Up)
      tdecay=2*(ThPmax_Dn-TPmax)
      TriCrvY=[0,Pmax,0]
      TriCrvX=[TPmax-trise,TPmax,TPmax+tdecay]
      fig = plt.figure(figsize=(16, 8))
      ax = fig.add_subplot(1, 1, 1,)# aspect=1)
      
      Tval=pd.DataFrame([Pmax,TPmax,ThPmax_Up,ThPmax_Dn,trise,tdecay],['Pmax= ','t_Pmax= ','ThPmax_Up= ','ThPmax_Dn=','Tr= ','Td= '])

      print(Tval)

      
#      ax.set_xlim(0, 4)
#      ax.set_ylim(0, 4)
      

      
      ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
      
      ax.plot(xy1['x'], xy1['y'], c=(0.25, 0.25, 1.00), lw=2, label="Pressure", zorder=10)
      

            

      ax.plot(xy1['x'], (xy1['y']*0+hPmax), c=(1.00, 0.25, 0.25), lw=1,linestyle="--")
      ax.plot(xy1['x'], (xy1['y']*0+Pmax), c=(1.00, 0.25, 0.25), lw=1,linestyle="--")
      ax.plot(xy1['x'], (xy1['y']*0), c=(1.00, 0.25, 0.25), lw=1,linestyle="--")
      ax.plot([TPmax,TPmax],[Pmax,0], lw=1,linestyle="--",c=(1.00, 0.25, 0.25))
      ax.set_title("Pressure Time series plot", fontsize=20, verticalalignment='bottom')
      ax.set_xlabel("Time (ms)")
      ax.set_ylabel("Pressure [bar]")
#      plt.pause(20)

      if input('Continue? ')=='y':
            ax.plot(TriCrvX,TriCrvY, lw=1,linestyle="--",c=(1.00, 0.25, 0.25))






            ax.annotate(r'$P_{max}$', xy=(TPmax,Pmax), xytext=(TPmax+10,Pmax+0.5),arrowprops=dict(arrowstyle="->"),fontsize=14, ha="left", color='blue')

            ax.annotate(r'$1/2P_{max_{up-crossing}}$', xy=((TPmax-trise/2),hPmax), xytext=((TPmax-trise)-20,hPmax +3),arrowprops=dict(arrowstyle="->"),fontsize=14, ha="left", color='blue')

            ax.annotate(r'$1/2P_{max_{up-crossing}}$', xy=((TPmax+tdecay/2),hPmax), xytext=((TPmax+tdecay)+20,hPmax +2),arrowprops=dict(arrowstyle="->"),fontsize=14, ha="right", color='blue')

            ax.annotate("", xy=(TPmax + tdecay,-0.2), xytext=(TPmax,-0.2),arrowprops=dict(arrowstyle="<->"),fontsize=14, ha="right", color='blue')
            ax.annotate("", xy=(TPmax - trise,-0.2), xytext=(TPmax,-0.2),arrowprops=dict(arrowstyle="<->"),fontsize=14, ha="right", color='blue')

            ax.text(TPmax - trise/2,-.8, "Tr", fontsize=12, ha="right", color='blue')
            ax.text(TPmax + tdecay/2,-.8, "Td", fontsize=12, ha="right", color='blue')
      



#      
      plt.show()
#      plt.pause(20)

      if input('Save? ')=='y':
            fig.savefig(fl_out +'.pdf',dpi=600)
            plt.close()
            from pandas import ExcelWriter

            writer = ExcelWriter(fl_out + '.xlsx')
            Tval.to_excel(writer,'Sheet1')
            writer.save()
      
