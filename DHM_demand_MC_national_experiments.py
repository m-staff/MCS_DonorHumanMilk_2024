# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 15:32:53 2023

@author: Student
"""
import pandas as pd
import random
import math
import numpy as np


Distribution_source="Norris"  #in not NHS means Norris

X=5 #n of days for bridging
Y=32 #babies born below a cut-off GA weeks for bridging
Z=34 #upper bound beyond bridging, max 37

A=1   #%of no-supply
B=20  #%of mothers with shartfall
C=50  #%of shartfall of B affected babies

MCS_iterations=10

Tiny_baby_weight_cutoff=1000
Tiny_baby_GA_cutoff=28
Intermed_GA_cutoff=32

Tiny_baby_initial=20
Tiny_baby_step=20
Small_baby_initial=26
Small_baby_step=30
Intermed_baby_initial=45
Intermed_baby_step=30
Target_max=180

df = pd.read_excel("Trial.xlsx")
df_Norris_boys = pd.read_excel("Trial.xlsx", sheet_name="Norris_boys")
df_Norris_girls = pd.read_excel("Trial.xlsx", sheet_name="Norris_girls")
df_Twin_boys= pd.read_excel("Trial.xlsx", sheet_name="Twin_boys")
df_Twin_girls=pd.read_excel("Trial.xlsx", sheet_name="Twin_girls")

# to set the birth week as an index and override the original df
df.set_index("Unnamed: 0", inplace=True)
df = df.rename(columns={"Unnamed: 2": 'Sing_n_births', 'Unnamed: 6': 'Mult_n_births'})
df_births= df[["Sing_n_births", 'Mult_n_births']]

#for LMS equation
from scipy.stats import norm

prob_x1_array=[0]*20

for block in range(1, 20+1):

    GA_first= 22 + block
    x1= df_births.at[GA_first, "Sing_n_births"]
    y1= df_births.at[GA_first, "Mult_n_births"]/2
    denominator=x1+y1
    prob_x1=x1/denominator
    prob_x1_array[block-1]=prob_x1


df_NHS = pd.read_excel("Trial.xlsx", sheet_name="dataSet")
#remove first row
df_NHS=df_NHS.tail(-1)

#####################################################################################

A=A/100
B=B/100
C=C/100


results = [[0 for i in range(MCS_iterations)] for j in range(len(df_NHS))]

from datetime import datetime
start_time=datetime.now().strftime("%Y-%m-%d %H:%M")

for MCS in range (1, MCS_iterations+1):
    
    if MCS%1 == 0:
        print(MCS)
    thelist=[134]
    for tt in range(len(thelist)):
        row_number=thelist[tt]
        total_per_Trust=0
        max_cluster = math.floor((max(Y,Z)-22))
        for cluster in range(1,max_cluster+1):
            GA=cluster+22
            n_of_infants= df_NHS.iloc[row_number,cluster+3] 
            total_babies=0
            while total_babies<n_of_infants:
                rand_num=random.uniform(0, 1)
                if rand_num< prob_x1_array[cluster-1]:
                    n_of_babies=1
                    GA_day=random.randint(0,6)
                else:
                    n_of_babies=2
                    GA_day=random.randint(0,6)
                if total_babies==n_of_infants-1:#so there is only one more required to be generated
                    n_of_babies=1
                total_babies=total_babies+n_of_babies

                supply_rand_num=random.uniform(0, 1)
                if supply_rand_num<A:           #maternal supply population
                    mother_status="no_supply"
                elif supply_rand_num<A+B:
                    mother_status="under_supply"
                else:
                    mother_status="supply"

                for baby_born in range(1, n_of_babies+1):
                    k= random.randint(0, 1)
                    if k==0:
                        girl=True
                    else:
                        girl=False
                    r_number=random.uniform(0, 100)
                    r_number=round(r_number,1)
                    if r_number<=0.4:
                        centile=0.4
                    elif r_number>=99.6:
                        centile=99.6
                    else:
                        centile=r_number
                    weight_array=[0]*(38-GA+1) 
                    granular_array=[0]*((38-GA+1)*7-6)

                    for week_for_feeding in range(GA, 38+1):
                        if girl==True and n_of_babies==1:
                            L= df_Norris_girls.iloc[week_for_feeding-23, 2]
                            M= df_Norris_girls.iloc[week_for_feeding-23, 3]
                            S= df_Norris_girls.iloc[week_for_feeding-23, 4]
                        elif girl==False and n_of_babies==1:
                            L= df_Norris_boys.iloc[week_for_feeding-23, 2]
                            M= df_Norris_boys.iloc[week_for_feeding-23, 3]
                            S= df_Norris_boys.iloc[week_for_feeding-23, 4]
                        elif girl==True and n_of_babies==2:
                            L= df_Twin_girls.iloc[week_for_feeding-23, 2]
                            M= df_Twin_girls.iloc[week_for_feeding-23, 3]
                            S= df_Twin_girls.iloc[week_for_feeding-23, 4]
                        elif girl==False and n_of_babies==2:
                            L= df_Twin_boys.iloc[week_for_feeding-23, 2]
                            M= df_Twin_boys.iloc[week_for_feeding-23, 3]
                            S= df_Twin_boys.iloc[week_for_feeding-23, 4]
                            #print(f"weigtht is {round(weight_equ,2)} g" )
                        weight_equ=M*pow(1+L*S*norm.ppf(centile/100),1/L)                 
                        weight_array[week_for_feeding-GA]=weight_equ
                        granular_array[(week_for_feeding-GA)*7]=weight_equ    #baby's daily calculated weight as it follows the centile growth curve                    

                    for i in range(1, 38-GA+1):
                        day_step=(weight_array[i]-weight_array[i-1])/7 #day_step=0 !!!!!
                        granular_array[(i-1)*7+1]=weight_array[i-1]+day_step
                        granular_array[(i-1)*7+2]=weight_array[i-1]+day_step*2
                        granular_array[(i-1)*7+3]=weight_array[i-1]+day_step*3
                        granular_array[(i-1)*7+4]=weight_array[i-1]+day_step*4
                        granular_array[(i-1)*7+5]=weight_array[i-1]+day_step*5
                        granular_array[(i-1)*7+6]=weight_array[i-1]+day_step*6

                    bridging_array=[0]*X
                    bridging_total_per_baby=0
                    total_per_baby=0

                    if GA>23 and GA<=Y: #start at GA=24 becuase Norris doesn't go lower
                        for bridging_day in range (1, X+1):
                            weight=granular_array[GA_day+bridging_day-1]
                            bridging_array[bridging_day-1]=weight

                        if bridging_array[0]<Tiny_baby_weight_cutoff or GA<Tiny_baby_GA_cutoff:
                            volume_per_kg=Tiny_baby_initial
                            step=Tiny_baby_step

                        elif GA>=Intermed_GA_cutoff:
                            volume_per_kg=Intermed_baby_initial
                            step=Intermed_baby_step                            

                        else:
                            volume_per_kg=Small_baby_initial #Small_baby_initial
                            step=Small_baby_step            

                        for ii in range (1, X+1):#ii refers to days after birth for bridging preriod
                            feed_volume=bridging_array[ii-1]/1000*volume_per_kg
                            bridging_total_per_baby=bridging_total_per_baby+feed_volume
                            volume_per_kg=volume_per_kg+step
                            if volume_per_kg>=180:
                                volume_per_kg=180

                        total_per_baby=bridging_total_per_baby
                                                
                        provision=0
                        #mothers with no-supply and undersupply will be continuing after bridging
                        if mother_status=="no_supply" or mother_status=="under_supply":
                            if mother_status=="no_supply":
                                provision=1
                            if mother_status=="under_supply":
                                provision=C      
                            number_days_beyond_bridging=(Z+1)*7-GA*7-GA_day-X
                            for iii in range(X+1, X+number_days_beyond_bridging+1): #!!!! #iii refers to day number of beyond_bridging e.g. if bridging was for 5 days, from day 6 till day (calculated)
                                feed_volume=granular_array[iii+GA_day-1]/1000*volume_per_kg*provision
                                total_per_baby=total_per_baby+feed_volume
                                volume_per_kg=volume_per_kg+step
                                if volume_per_kg>=180:
                                    volume_per_kg=180 #target feeding volume, so it does not go beyong 180ml/kg of baby                                    
                                    
                    elif GA>23 and GA<=Z:
                        
                        if granular_array[GA_day]<Tiny_baby_weight_cutoff or GA<Tiny_baby_GA_cutoff:
                            volume_per_kg=Tiny_baby_initial
                            step=Tiny_baby_step

                        elif GA>=Intermed_GA_cutoff:
                            volume_per_kg=Intermed_baby_initial
                            step=Intermed_baby_step                         

                        else:
                            volume_per_kg=Small_baby_initial #Small_baby_initial
                            step=Small_baby_step            

                        provision=0
                        #mothers with no-supply and undersupply will be continuing after bridging
                        if mother_status=="no_supply" or mother_status=="under_supply":
                            if mother_status=="no_supply":
                                provision=1
                            if mother_status=="under_supply":
                                provision=C      
                            number_days_beyond_bridging=(Z+1)*7-GA*7-GA_day
                            for iii in range(1, number_days_beyond_bridging+1): #!!!! #iii refers to day number of beyond_bridging e.g. if bridging was for 5 days, from day 6 till day (calculated)
                                feed_volume=granular_array[iii+GA_day-1]/1000*volume_per_kg*provision
                                total_per_baby=total_per_baby+feed_volume
                                volume_per_kg=volume_per_kg+step
                                if volume_per_kg>=180:
                                    volume_per_kg=180 #target feeding volume, so it does not go beyong 180ml/kg of baby
                                    
                    total_per_Trust=total_per_Trust+total_per_baby

        results[row_number][MCS-1]=total_per_Trust #2D array
        
means = np.mean(results, axis=1)

percentiles = np.percentile(results, [5,10,50,90,95], axis =1)
percentiles = np.transpose(percentiles)

from datetime import datetime
finish_time=datetime.now().strftime("%Y-%m-%d %H:%M")

#convert arrays to dfs
data_parametrs = {
    'Parameters': ['n_of_runs', 'X_n_days_bridging', 'Y_bridging_cutoff', 'Z_beyond_bridging_cutoff','A_mothers_no_supply','B_mothers_shartfall','C_shartfall_babies', 'start', 'end'],
    'Value': [MCS_iterations, X, Y, Z, A, B, C,start_time, finish_time],
 }

df_table_parameters = pd.DataFrame(data_parametrs)
df_means=pd.DataFrame(means, columns=["Means"])
df_percentiles=pd.DataFrame(percentiles, columns=["5","10", "50", "90", "95"])

#to merge 2 dfs
df_final_results=pd.concat([df_means, df_percentiles], axis=1)

#code to append to existing Excel file: if it does not exist, please create it
with pd.ExcelWriter('National_Experiments.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
   df_table_parameters.to_excel(writer, sheet_name="parameters")
   df_final_results.to_excel(writer, sheet_name="results")
    
    
    
    
    
    
    
    
    
    