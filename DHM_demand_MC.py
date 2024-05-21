# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 15:32:53 2023

@author: Student
"""
import pandas as pd
import random
import math
import numpy as np

X=6 #n of days for bridging
Y=26 #babies born below a cut-off GA weeks
Z=32 

A=0   #%of no-supply
B=0  #%of mothers with shartfall
C=0   #%of shartfall of  B affected babies

MCS_iterations=10000

Tiny_baby_weight_cutoff=1000
Tiny_baby_GA_cutoff=28
Intermed_GA_cutoff=32

Intermed_GA_cutoff=Intermed_GA_cutoff-1

Tiny_baby_initial=20
Tiny_baby_step=20
Small_baby_initial=26
Small_baby_step=30
Intermed_baby_initial=45
Intermed_baby_step=30
Target_max=180

df = pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx")
df_Norris_boys = pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx", sheet_name="Norris_boys")
df_Norris_girls = pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx", sheet_name="Norris_girls")
df_Twin_boys= pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx", sheet_name="Twin_boys")
df_Twin_girls=pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx", sheet_name="Twin_girls")
df_test= pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx", sheet_name="test")

# to set the birth week as an index and override the original df
df.set_index("Unnamed: 0", inplace=True)
df = df.rename(columns={"Unnamed: 2": 'Sing_n_births', 'Unnamed: 6': 'Mult_n_births'})
df_births= df[["Sing_n_births", 'Mult_n_births']]

#for LMS equation
from scipy.stats import norm

prob_x1_array=[0]*6
prob_x2_array=[0]*6
prob_x3_array=[0]*6
prob_y1_array=[0]*6
prob_y2_array=[0]*6
prob_y3_array=[0]*6

for block in range(1, 7):
    #print(block)
    GA_first= 20 + 3*block
    #print(GA_first)
    GA_second= 21 + 3*block
    GA_third= 22 + 3*block
    x1= df_births.at[GA_first, "Sing_n_births"]
    x2= df_births.at[GA_second, "Sing_n_births"]
    x3= df_births.at[GA_third, "Sing_n_births"]
    y1= df_births.at[GA_first, "Mult_n_births"]/2
    y2= df_births.at[GA_second, "Mult_n_births"]/2
    y3= df_births.at[GA_third, "Mult_n_births"]/2
    #print(y3)
    denominator=x1+x2+x3+y1+y2+y3
    #print(denominator)
    prob_x1=x1/denominator
    prob_x2=x2/denominator
    prob_x3=x3/denominator
    prob_y1=y1/denominator 
    prob_y2=y2/denominator 
    prob_y3=y3/denominator 
    #print(prob_x1)
    prob_x1_array[block-1]=prob_x1
    prob_x2_array[block-1]=prob_x2
    prob_x3_array[block-1]=prob_x3
    prob_y1_array[block-1]=prob_y1
    prob_y2_array[block-1]=prob_y2
    prob_y3_array[block-1]=prob_y3

df_NHS = pd.read_excel("C:\\Users\\Student\\Desktop\\Trial.xlsx", sheet_name="dataSet")
#remove first row
df_NHS=df_NHS.tail(-1)
df_NHS= df_NHS.rename(columns={
    "Mothers" : "Cluster_0",
    "Unnamed: 4": "Cluster_1",
    "Unnamed: 5": "Cluster_2",
    "Unnamed: 6": "Cluster_3",
    "Unnamed: 7": "Cluster_4",
    "Unnamed: 8": "Cluster_5",
    "Unnamed: 9": "Cluster_6",
    "Unnamed: 10": "Cluster_7"
})



#####################################################################################

A=A/100
B=B/100
C=C/100


results = [[0 for i in range(MCS_iterations)] for j in range(len(df_NHS))]

for MCS in range (1, MCS_iterations+1):
    print(MCS)
    for row_number in range (0,2): #(0, len(df_NHS)-1):
        #print(f"ROW NUMBER {row_number}")
        #print(df_NHS.iloc[row_number,1])
        total_per_Trust=0
        max_cluster = math.floor((Y-20)/3)
        for cluster in range(1,max_cluster+1):
            #print(f"Cluster_{cluster}")
            GA_low= 20+3*cluster
            GA_medium= 21+3*cluster
            GA_high=22+3*cluster
            n_of_deliveries= df_NHS.iloc[row_number,cluster+3] 
            #print(n_of_deliveries)

            for delivery in range(1,n_of_deliveries+1):
                #print(f"This is delivery number {delivery}")
                rand_num=random.uniform(0, 1)
                #print(rand_num)
                if rand_num< prob_x1_array[cluster-1]:
                    GA=GA_low
                    n_of_babies=1
                    GA_day=random.randint(0,6)
                    #print(f"{GA}+{GA_day}_GA")
                elif rand_num< prob_x1_array[cluster-1]+prob_x2_array[cluster-1]:
                    GA=GA_medium
                    n_of_babies=1
                    GA_day=random.randint(0,6)
                   # print(f"{GA}+{GA_day}_GA")
                elif rand_num< prob_x1_array[cluster-1]+prob_x2_array[cluster-1]+prob_x3_array[cluster-1]:
                    GA=GA_high
                    n_of_babies=1
                    GA_day=random.randint(0,6)
                    #print(f"{GA}+{GA_day}_GA")
                elif rand_num< prob_x1_array[cluster-1]+prob_x2_array[cluster-1]+prob_x3_array[cluster-1]+prob_y1_array[cluster-1]:
                    GA=GA_low
                    n_of_babies=2
                    GA_day=random.randint(0,6)
                    #print(f"{GA}+{GA_day}_GAtwins")
                elif rand_num< prob_x1_array[cluster-1]+prob_x2_array[cluster-1]+prob_x3_array[cluster-1]+prob_y1_array[cluster-1]+prob_y2_array[cluster-1]:
                    GA=GA_medium
                    n_of_babies=2
                    GA_day=random.randint(0,6)
                    #print(f"{GA}+{GA_day}_GAtwins")
                elif rand_num< prob_x1_array[cluster-1]+prob_x2_array[cluster-1]+prob_x3_array[cluster-1]+prob_y1_array[cluster-1]+prob_y2_array[cluster-1]+prob_y3_array[cluster-1]:
                    GA=GA_high
                    n_of_babies=2
                    GA_day=random.randint(0,6)
                   #print(f"{GA}+{GA_day}_GAtwins")
                GA_day=0 #!!!!!!

                supply_rand_num=random.uniform(0, 1)
                if supply_rand_num<A:
                    mother_status="no_supply"
                   # print("NO-SUPPLY")
                elif supply_rand_num<A+B:
                    mother_status="under_supply"
                   # print("UNDER-SUPPLY")
                else:
                    mother_status="supply"
                    #print("SUPPLY")

                for baby_born in range(1, n_of_babies+1):
                    k= random.randint(0, 1)
                    if k==0:
                        girl=True
                        #print("It is a girl")
                    else:
                        girl=False
                        #print("It is a boy")
                    r_number=random.uniform(0, 100)
                    r_number=round(r_number,1)
                    #print(f"Genrated number is {r_number}")
                    if r_number<=0.4:
                        centile=0.4
                       # print(f"Centile is {centile}")
                    elif r_number>=99.6:
                        centile=99.6
                       # print(f"Centile is {centile}")
                    else:
                        centile=r_number
                        #print(f"Centile is {centile}")
                    weight_array=[0]*(38-GA+1) 
                    granular_array=[0]*((38-GA+1)*7-6)

                    for avarage_feeding in range (GA, 38+1):
                        the_weight=df_test.iloc[avarage_feeding-11,2]
                        #print(the_weight)
                        weight_array[avarage_feeding-GA]=the_weight
                        granular_array[(avarage_feeding-GA)*7]=the_weight 
                        

                  #  for week_for_feeding in range(GA, 38+1):
                   #     if girl==True and n_of_babies==1:
                   #         L= df_Norris_girls.iloc[week_for_feeding-23, 2]
                    #        M= df_Norris_girls.iloc[week_for_feeding-23, 3]
                     #       S= df_Norris_girls.iloc[week_for_feeding-23, 4]
                      #  elif girl==False and n_of_babies==1:
                       #     L= df_Norris_boys.iloc[week_for_feeding-23, 2]
                        #    M= df_Norris_boys.iloc[week_for_feeding-23, 3]
                         #   S= df_Norris_boys.iloc[week_for_feeding-23, 4]
                       # elif girl==True and n_of_babies==2:
                        #    L= df_Twin_girls.iloc[week_for_feeding-23, 2]
                         #   M= df_Twin_girls.iloc[week_for_feeding-23, 3]
                          #  S= df_Twin_girls.iloc[week_for_feeding-23, 4]
                      #  elif girl==False and n_of_babies==2:
                          #  L= df_Twin_boys.iloc[week_for_feeding-23, 2]
                       #     M= df_Twin_boys.iloc[week_for_feeding-23, 3]
                        #    S= df_Twin_boys.iloc[week_for_feeding-23, 4]
                         #   #print(f"weigtht is {round(weight_equ,2)} g" )
                     #   weight_equ=M*pow(1+L*S*norm.ppf(centile/100),1/L)                 
                      #  weight_array[week_for_feeding-GA]=weight_equ
                       # granular_array[(week_for_feeding-GA)*7]=weight_equ                
                    #print(f"hello{weight_array}")        

                    for i in range(1, 38-GA+1):
                        day_step=0 #!!!!!!!
                        #(weight_array[i]-weight_array[i-1])/7
                        granular_array[(i-1)*7+1]=weight_array[i-1]+day_step
                        granular_array[(i-1)*7+2]=weight_array[i-1]+day_step*2
                        granular_array[(i-1)*7+3]=weight_array[i-1]+day_step*3
                        granular_array[(i-1)*7+4]=weight_array[i-1]+day_step*4
                        granular_array[(i-1)*7+5]=weight_array[i-1]+day_step*5
                        granular_array[(i-1)*7+6]=weight_array[i-1]+day_step*6
                    #print("gran ar is", granular_array)

                    bridging_array=[0]*X
                    bridging_total_per_baby=0
                    total_per_baby=0

                    if GA>23 and GA<=Y: #!!!!!
                        for bridging_day in range (1, X+1):
                             #   if (GA_day+bridging_day-1)<((Z-GA+1)*7-6):
                            weight=granular_array[GA_day+bridging_day-1]
                            #print(weight)
                            bridging_array[bridging_day-1]=weight
                        #print(bridging_array)


                        if bridging_array[0]<Tiny_baby_weight_cutoff or GA<Tiny_baby_GA_cutoff:
                            volume_per_kg=Tiny_baby_initial
                            step=Tiny_baby_step
                           # print('\033[93m'+ f"Tiny baby {volume_per_kg}")

                        elif GA>=Intermed_GA_cutoff:
                            volume_per_kg=Intermed_baby_initial
                            step=Intermed_baby_step
                            #print('\033[93m'+ f"Intermed baby {volume_per_kg}")

                        else:
                            volume_per_kg=1 #Small_baby_initial
                            step=Small_baby_step            
                           # print('\033[93m'+ f"Small baby {volume_per_kg}")

                        for ii in range (1, X+1):
                            feed_volume=bridging_array[ii-1]/1000*volume_per_kg
                            bridging_total_per_baby=bridging_total_per_baby+feed_volume
                            #print('\033[94m'+ f"{feed_volume}")
                            volume_per_kg=volume_per_kg+step
                            if volume_per_kg>=180:
                                volume_per_kg=180
                            #print('\033[91m'+ f"{volume_per_kg}")
                        #print(round(bridging_total_per_baby,0))

                        total_per_baby=bridging_total_per_baby
                        provision=0
                        #mothers with no-supply and undersupply will be continuing after bridging
                        if mother_status=="no_supply" or mother_status=="under_supply":
                            if mother_status=="no_supply":
                                provision=1
                            if mother_status=="under_supply":
                                provision=C                    
                            for iii in range(X+1, Z*7-(GA*7+GA_day)+1):
                                feed_volume=granular_array[iii+GA_day-1]/1000*volume_per_kg*provision
                                total_per_baby=total_per_baby+feed_volume
                                volume_per_kg=volume_per_kg+step
                                #print('\033[94m'+ f"{feed_volume}")
                                if volume_per_kg>=180:
                                    volume_per_kg=180
                                #print('\033[91m'+ f"{volume_per_kg}")
                        #print(round(total_per_baby,0)) 
                        total_per_Trust=total_per_Trust+total_per_baby
        #print(f"Hello {total_per_Trust}")
        results[row_number][MCS-1]=total_per_Trust
#print(results)

#set element results[118][1]=87
# print second column results[:][1]
        
np.savetxt('results.txt',results)
means = np.mean(results, axis=1)
#means = np.transpose(means)
print(means)

percentiles = np.percentile(results, [5,10,50,90,95], axis =1)
percentiles = np.transpose(percentiles)
print(percentiles)

