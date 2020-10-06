#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 09:19:21 2020

@author: edvardcarlsson
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size("small")



                   
def compare(kurs_input,stil_id,pw):
    antal = len(kurs_input)
    
    df = pd.DataFrame(columns=["Kurs","Antal Registrerade", "Antal godkända", 
                           "God undervisning", "Tydliga mål", "Förståelseinriktad examination", 
                           "Lämplig arbetsbelastning", "Kursen känns angelägen för min utbildning", 
                           "Överlag är jag nöjd med den här kursen"], index = range(antal))
   
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # samma kurskoder
    kurskoder = []
    for i in range(antal):
        driver.get("http://lubaspp.lu.se/lubas/pp/Educationplaning.seam?planOmgangId=50&actionMethod=home.xhtml%3AutbildningsNamnd.resetFields%28%29")
        sleep(1)
        driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/div/div[3]/div[4]/div/span[1]/input").clear()
        sleep(1)
        driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/div/div[3]/div[4]/div/span[1]/input").send_keys("{}".format(kurs_input[i]))
        sleep(1)
        driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/div/div[3]/div[6]/div/span[1]/table/tbody/tr[2]/td[4]/table/tbody/tr[1]/td/input").click()
        sleep(1)
        driver.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/div/div[3]/input").click()
        sleep(1)
        kurskoder.append(driver.find_element_by_id("f2:t1:0:C2").text)
    
    # logga in på LU
    driver.get("https://www.lu.se/user/login")
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/div/form/a").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[3]/form/div[1]/input").send_keys(stil_id)
    sleep(1)
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[3]/form/div[2]/input").send_keys(pw)
    sleep(1)
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[3]/form/div[3]/input").click()

                                             
    # hämta ceq-info                                         
    for i in range(antal):
        driver.get("http://www.ceq.lth.se/rapporter/?kurskod={}".format(kurskoder[i]))
        sleep(1)
        driver.find_element_by_partial_link_text("{}".format(kurs_input[i])).click()
    
        df.iloc[i,0] = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/b").text
        df.iloc[i,1] = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[1]/table/tbody/tr[7]/td[2]").text
        df.iloc[i,2] = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[1]/table/tbody/tr[8]/td[2]").text[:3]
        df.iloc[i,3] = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[2]/td[2]").text
        df.iloc[i,4] = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[3]/td[2]").text
        df.iloc[i,5] = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[4]/td[2]").text
        df.iloc[i,6] = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[5]/td[2]").text
        df.iloc[i,7] = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[7]/td[2]").text
        df.iloc[i,8] = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[8]/td[2]").text
   
    return df
             
                            

def autolabel(rects,ax):
    for rect in rects:
        height = rect.get_height()
        if height >= 0:
            ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0.5),  # 0.5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        else:
             ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, - 10),  # vertical offset - negative
                    textcoords="offset points",
                    ha='center', va='bottom')


def score(ceq):
    # convert to ints
    for i in range(len(ceq)):
        ceq.iloc[i,1] = int(ceq.iloc[i,1])
        ceq.iloc[i,2] = int(ceq.iloc[i,2])
        ceq.iloc[i,3] = int(ceq.iloc[i,3])
        ceq.iloc[i,4] = int(ceq.iloc[i,4])
        ceq.iloc[i,5] = int(ceq.iloc[i,5])
        ceq.iloc[i,6] = int(ceq.iloc[i,6])
        ceq.iloc[i,7] = int(ceq.iloc[i,7])
        ceq.iloc[i,8] = int(ceq.iloc[i,8])    


    # Number of registered/passed
    labels = ceq.columns[1:3]
    courses = ceq.iloc[:,0].tolist()
    lists = [[] for i in range(len(courses))]
    for i in range(len(courses)):
        lists[i] = ceq.iloc[i,1:3].tolist()
        
    # layout        
    x = np.arange(len(labels))  
    width = 0.1  


    fig1, ax1 = plt.subplots()
    
    rects = [[] for i in range(len(courses))]
    for i in range(len(courses)):
        rects[i] = ax1.bar(x + i*width, lists[i], width,label=courses[i])
    
    ax1.set_xticks(x+0.1)
    ax1.set_xticklabels(labels)
    ax1.set_ylabel("Antal")
    ax1.set_title("Registrerade & godkända")
    ax1.legend(handles=rects, title="Kurser", bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)

    
    for i in range(len(courses)):
        autolabel(rects[i],ax1)


    # scores
    labels = ceq.columns[3:9]
    courses = ceq.iloc[:,0].tolist()
    lists = [[] for i in range(len(courses))]
    for i in range(len(courses)):
        lists[i] = ceq.iloc[i,3:9].tolist()

    x = np.arange(len(labels)) 
    width = 0.2  
    
    rects = [[] for i in range(len(courses))]
    
    fig2, ax2 = plt.subplots()
    for i in range(len(courses)):
        rects[i] = ax2.bar(x + i*width, lists[i], width,label=courses[i])
        
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.set_ylabel("Medelpoäng")
    ax2.set_title("Jämförelse mellan kurser")
    plt.xticks(rotation=90)
    ax2.legend(handles=rects, title="Kurs", bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)

    for i in range(len(courses)):
        autolabel(rects[i],ax2)




                                        
                
kurs_input = ["Tillämpad mas", "Introduktion till art", "Affärsmarkna", "Tillämpad affä"]  
stil_id = "LU account"
pw = "LU password"        
   

ceq = compare(kurs_input,stil_id,pw)                                 

score(ceq)








 