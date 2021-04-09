#!/usr/bin/env python
# coding: utf-8

# In[27]:


import csv
path_to_csv='C:/Users/Master/Documents/first_list.csv'

def csv_to_list(path_to_csv):
    a=[]
    with open(path_to_csv, newline='') as f:
        for x in csv.reader(f):
            a.append(x[0])
    return a


# In[28]:


def change_to_url(l):
    l1=[]
    for x in l:
        l1.append('https://person-stream.clearbit.com/v2/combined/find?email='+x)
    return l1  


# In[29]:


def run_url(l1):
    l2=[]
    for x in l1:
        payload={}
        headers = {'Authorization': 'Bearer sk_f2cb4451a6b62a6e379151f29fb3be9a'}
        response = requests.request("GET", x, headers=headers, data=payload)
        l2.append(response.json())
        
    return l2
    


# In[30]:


import requests
import json
email_list=csv_to_list(path_to_csv)
email_list2=change_to_url(email_list)
email_list3=run_url(email_list2)


# The purpose of the next step is to replace NoneType values with '-' in the nested JSON. This is because, it makes it iterable

# In[31]:


def clean(d):
    if type(d) == list:
        return [clean(e) for e in d]
    elif type(d) == dict:
        for k, v in list(d.items()):
            if v is None:
                d[k]='-'
            else:
                d[k] = clean(v)
    return d


# In[32]:


email_list4= clean(email_list3)
email_dict1= dict(zip(email_list, email_list4))
email_dict2 = {key:val for key, val in email_dict1.items() if val !={'error': {'type': 'unknown_record', 'message': 'Unknown person.'}} }


# In[33]:


email_dict3={}
for x in email_dict2:
    email_dict3[x]=email_dict2[x]['company']['metrics']['employees']
 


# In[34]:


email_dict4={}
for x in email_dict2:
    if email_dict2[x]['person']!='-':
        email_dict4[x]=email_dict2[x]['person']


# In[12]:


email_dict5={}
for x in email_dict4:
    email_dict5[x]=[email_dict4[x]['employment']['title'],email_dict4[x]['employment']['role'],email_dict4[x]['employment']['subRole'],email_dict4[x]['employment']['seniority']]
email_dict5


# In[14]:


import pandas as pd
from pandas import DataFrame


# In[16]:


df_p= pd.DataFrame([{'email_id':email_id,'title':title,'role':role,'subRole':subRole,'seniority':seniority} for email_id,[title,role,subRole,seniority] in email_dict5.items() ])


# In[18]:


df_c= pd.DataFrame([{'email_id':email_id, 'emp_size':emp_size} for email_id,emp_size in email_dict3.items()])


# In[20]:


df_comb=pd.merge(df_p, df_c, how="outer", on=["email_id"])


# In[21]:


#df_comb


# In[22]:


df_comb.to_csv(r'C:/Users/Master/Desktop/clearbit/the_first.csv')


# In[35]:


email_dict2


# In[ ]:




