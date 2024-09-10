import csv
import streamlit as sl
with open("data.csv",'r')as f:
    x=csv.reader(f)
    data=list(x)
    l=[data[i][1] for i in range(1,len(data))]
sl.set_page_config(page_title='bhagavan clinic',page_icon="icon.webp")
sl.header("welcome to Bhagavan clinic")
col1,col2,col3=sl.columns(3)
name=col1.text_input("enter your name")
phone=col2.text_input("enter your phone number")
email=col3.text_input("enter your email address")
a=list(sl.multiselect("choose the tests from the below",options=l))
c=0
col1,col2,col3=sl.columns(3)
for i in a:
    for j in range(1,len(data)):
        if i==data[j][1]:
            col1.write(str(j))
            col2.write(data[j][1])
            col3.write(data[j][2])
            c+=int(data[j][2])
sl.markdown("---")
col1,col2,col3=sl.columns(3)
col2.write(f"your total bill amount is ")
col3.write(str(c))