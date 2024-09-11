import csv
import streamlit as sl
with open("data.csv",'r')as f:
    x=csv.reader(f)
    data=list(x)
    l=[data[i][1] for i in range(1,len(data))]
sl.set_page_config(page_title='clinic',page_icon="icon.webp")
col1,col2=sl.columns(2)
col1.image("cliniclogo.jpg",width=250)
col2.title("Welcome to clinic")
col1,col2,col3=sl.columns(3)
name=col1.text_input("Enter your name")
phone=col2.text_input("Enter your phone number")
email=col3.text_input("Enter your email address")
a=list(sl.multiselect("Choose the tests from the below",options=l))
b =sl.button("Genrate bill")
c=0
c1=0
if b:
    sl.write(f"Genrated bill for {name}")
    col1,col2,col3=sl.columns(3)
    for i in a:
        for j in range(1,len(data)):
            if i==data[j][1]:
                c1+=1
                col2.write(data[j][1])
                col3.write(data[j][2])
                c+=int(data[j][2])
    for k in range(1,c1+1):
        col1.write(str(k))
    sl.markdown("---")
    col1,col2,col3=sl.columns(3)
    col2.write(f"your total bill amount is ")
    col3.write(str(c))
