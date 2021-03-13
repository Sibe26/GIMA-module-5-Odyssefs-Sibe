# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:32:32 2021

@author: Odisseas
"""
#Set os.chdir to local directory folder.
#Make sure to download the Clone_final.map & the Vleuten_costmap_final.map
#Store both the maps in the local directory folder
#Run the script & choose inputs
#Optional: set desired coordinates 

import pcraster
import os
os.chdir("G:\Module5\In-depth\dataset")
from pcraster import *
from pcraster.framework import *


pcraster.setclone("Clone_final.map")



pcraster.clone= pcraster.readmap("Clone_final.map")
x=pcraster.nominal(pcraster.xcoordinate(1))
pcraster.report(x,'x')
y=pcraster.nominal(pcraster.ycoordinate(1))
pcraster.report(y,'y')

# create point of departure
col1 =pcraster.pcreq(x,128814)
row1 =pcraster.pcreq(y,458569)
start_coord=pcraster.pcrand(col1,row1)
pcraster.report(start_coord,'start_coord')
    
# create point of arrival
col2 =pcraster.pcreq(x,130104)
row2 =pcraster.pcreq(y,458139)
end_coord=pcraster.pcrand(col2,row2)
pcraster.report(end_coord,'end_coord')

    
#create intermidiate point
col3 =pcraster.pcreq(x,128954)
row3 =pcraster.pcreq(y,457339)
int_coord=pcraster.pcrand(col3,row3)
pcraster.report(int_coord,'int_coord')   




#spread for start location
start_loc = pcraster.spread("start_coord",0,"Vleuten_costmap_final.map")
#spread for intermidiate location
intermidiate_loc = pcraster.spread("int_coord",0,"Vleuten_costmap_final.map")
#spread for end location 
end_loc = pcraster.spread("end_coord",0,"Vleuten_costmap_final.map")
#tripc- accumulated spread between start and intermidiate locations
trip1 = start_loc  + intermidiate_loc
#trip - accumulated spread between intermidiate and end locations
trip2 = intermidiate_loc + end_loc
#fastest time start to intermidiate location
time1 = (int(pcraster.cellvalue(pcraster.mapminimum(trip1+1),1)[0]))/60
#fastest time intermidiate location to end
time2 = (int(pcraster.cellvalue(pcraster.mapminimum(trip2+1),1)[0]))/60
#Asking for available time to go from start to intermidiate location
while True:
  try:
    trip1_time= int(input("Enter time for start to intermidiate location trip (in minutes):"))
    while int(trip1_time)<time1:
        trip1_time = int(input("Not sufficient time to complete the trip,please enter a time value more than" + " " + str(int(time1)) + " minutes:")) 
    break
  except ValueError:
      print("Please input integer only:")  
      continue
 
#Asking for available time to go from intermidiate location to the end
while True:
  try:
    trip2_time= int(input("Enter time for intermidiate location to end trip (in minutes):"))
    while int(trip2_time)<time2:
          trip2_time = int(input("Not sufficient time to complete the trip,please enter a time value more than" + " " + str(int(time2)) + " minutes:"))
    break
  except ValueError:
      print("Please input integer only:")  
      continue     

#possible delays/time window
while True:
    try:
        delay = int(input("Enter possible delay/time window (in minutes):"))
        break
    except ValueError:
        print ("Please input integer only:")
        continue

#Creating potential path area map, printing results
ppa = (trip1 < trip1_time*60 + delay*60/2)|((trip2 ) < trip2_time*60 + delay*60/2)
pcraster.report(ppa,'ppa')
pcraster.aguila('ppa')
print("Within a time frame of " + str(trip1_time + trip2_time + delay) + " minutes" + ", the potential path area between the three given locations is " + str(int(pcraster.cellvalue(pcraster.maptotal(pcraster.scalar(ppa)),1)[0])) + " square meters.")
