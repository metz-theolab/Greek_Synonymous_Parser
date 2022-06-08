import pandas as pd
import numpy as np
import requests
import time
import json
import re
from string import digits
from bs4 import BeautifulSoup
from numpy import loadtxt


#Config
word_list = []
word_list = loadtxt('en_words.txt', dtype='str')
occur_min = 2000
occur_max = 100000  




def import_perseus(en_lex):
    
    #1. Calcule le nombre de pages html
    url = "https://www.perseus.tufts.edu/hopper/definitionlookup?&q="+en_lex+"&sort=freq&target=greek"

    data = requests.get(url)
    if data is None:
        return
    soup = BeautifulSoup(data.text, 'lxml')                          #Extract in soup the html of the page
    try:
        pages = max(list(soup.find("div", {"class":"pager"}).text))      #Extract the number of result pages
    except:
        pages = 1
    #2. Récupère le DataFrame pour chaque page html

    df=[]
    for x in range(int(pages)):
        url = "https://www.perseus.tufts.edu/hopper/definitionlookup?type=exact&page="+str(x+1)+"&q="+en_lex+"&sort=freq&target=greek"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'lxml')                       #Extract in soup the html of the page
        table = soup.find("table", {"class":"data"})                  #Extract in table the html of the table "data"
        if table is None:
            return
        
        rows = []
        for child in table.children:
            row = []
            for td in child:
                try:
                    row.append(td.text.replace('\n', ''))
                    
                except:
                    continue
            if len(row) > 0:
                rows.append(row)
                
        df_part = pd.DataFrame(rows[1:], columns=rows[0])             #Create the Dataframe for each page
        df.append(df_part)                                            #Add the Dataframe into a list
   
    result=pd.concat(df, axis=0, ignore_index=True)                   #Concatenate the list into one Dataframe

    
    #3. Filtrage des données
    result['Max. Inst.'] = result['Max. Inst.'].str.replace(',','')   #Supprime les virgules dans la colonne Max. Inst.
    #result['Headword'] = re.sub(r'[0-9]+', '', result['Headword'].str)
    
    result = result.astype({'Max. Inst.':'int'})                      #Convertit les valeurs de la colonne Max. Inst. en integer
    
    result = result[(result['Short Definition'] == en_lex+",")
                    | (result['Short Definition'] == en_lex) 
                    | (result['Short Definition'] == ", "+en_lex) 
                    | ((result['Max. Inst.'] > occur_min) & (result['Max. Inst.'] < occur_max))]
    if result.empty:
        return
    
    result = result.sort_values(by = 'Max. Inst.', ascending = False) #Trie les valeurs par Max. Inst. décroissant

    #print(result.loc[:, ["Headword", "Max. Inst.", "Short Definition"]])
    
    
    
    #4. Dump les valeurs dans le dictionnaire
        
    result = result.rename(columns = {'Headword': en_lex})          #Renome la colonne des mots grec par sa clé en anglais

    #dict_syn[en_lex] = en_lex
    dict_syn = result.loc[:, [en_lex]].to_dict(orient='list')     #Dump la colonne des synonymes dans le dictionnaire
    
    dict_syn = {key: [re.sub('\d', '', ele) for ele in val]         #Nettoie le dictionnaire de toute valeur numérique
       for key, val in dict_syn.items()}
    
    dict_syn[dict_syn[en_lex][0]]=dict_syn[en_lex]
    del dict_syn[en_lex][0]
    del dict_syn[en_lex]
    
    return dict_syn



if __name__ == "__main__":

    dict_syns = {}
    i=0
    count=0
    for en_lex in word_list:

        if en_lex!="":
            dict_syn = import_perseus(en_lex)
        if dict_syn: dict_syns.update(dict_syn)
        
        #Créer un dump json tout les 10 mots
        if i==10:
            with open("synonyms.txt", "w", encoding='utf-8') as f:
                json.dump(dict_syns, f, ensure_ascii=False)
                print("dump", end=' ')
                
                
            i=0
        i+=1
        count+=1
        print(count, end=' ')

    #dump final    
    with open("synonyms.txt", "a+", encoding='utf-8') as f:
        json.dump(dict_syns, f, ensure_ascii=False)    