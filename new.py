# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, flash, g, jsonify
from flask_googlemaps import GoogleMaps
from grove_rgb_lcd import *
from grovepi import *
import mysql.connector
import json
import hashlib
import RPi.GPIO  as GPIO
import time

sensor = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(18, GPIO.OUT)  
setRGB(0,128,64)
dbConnection = mysql.connector.connect(host='ip', password="", user='', database='')

while True:
       
      # setText("detecting..........")
       i=GPIO.input(7)
       if i==0:                 #When output from motion sensor is LOW
             print "DETECTED"
             GPIO.output(18, 1)  #Turn OFF LED
             
             
             sds = dbConnection.cursor()
             sds.execute('select id from `order` where post_id = %s',[id])
             re = sds.fetchall()
             for r in re:
                 sd = dbConnection.cursor()
                 sd.execute('select id,incode,aucode,polestate from `order` where id = %s',[r[0]])
                 print r[0]
                 s = r[0]
                 result=sd.fetchall()
                 for row in result:
                    if row[1]==row[2]:
                        setText("park successfully")
                        sdt = dbConnection.cursor()
                        sdt.execute('UPDATE `order` SET incode=%s,polestate=%s,orderstate=%s WHERE id = %s', ["","down","overdue",s])
                        c = dbConnection.cursor()
                        c.execute('UPDATE post SET polestate=%s WHERE id = %s', ["down",id])
                      
                    elif row[3]=="up" :
                        setText(".....")
                 
                        
             dbConnection.commit()
             c.close()
             time.sleep(2)
         
       elif i==1:               #When output from motion sensor is HIGH
             print "NOTHING"
             GPIO.output(18, 0)  #Turn ON LED
             time.sleep(2)
             c = dbConnection.cursor()
             c.execute('UPDATE post SET polestate=%s WHERE id = %s', ["up",id])
             dbConnection.commit()
           
             sds = dbConnection.cursor()
             sds.execute('select id,orderstate from `order` where post_id = %s',[id])
             re = sds.fetchall()
             print re
             if re==[]:
                 setText("This pole is free")

             elif re!=[] :
                 for r in re:
                     s = r[0]
                     print r[0]
                     sdt = dbConnection.cursor()
                     sdt.execute('UPDATE `order` SET polestate=%s WHERE id = %s', ["up",s])
            
                     sd = dbConnection.cursor()
                     sd.execute('select id,incode,aucode,orderstate,polestate from `order` where id = %s',[r[0]])
                     
                
                     result=sd.fetchall()
                     for row in result:
                         if row[3]=="overdue":
                             setText("This order is overdue")
                             
                         elif row[1]==row[2]:
                        
                             setText("You can park now")
                             c.execute('UPDATE post SET polestate=%s WHERE id = %s', ["down",id])
                             sdt = dbConnection.cursor()
                             sdt.execute('UPDATE `order` SET orderstate=%s WHERE id = %s', ["start",s])
                         elif row[1]!=row[2]:
                             setText("wait fot connection")
                             print row[3]
                             c = dbConnection.cursor()
                             c.execute('UPDATE post SET polestate=%s WHERE id = %s', ["up",id])
                         elif row[3]=="delete":
                             d = dbConnection.cursor()
                             d.execute('DELETE from `order` where id = %s', [s])
                         elif row[4]=="reserved":
                             setText("reserved")
                             c = dbConnection.cursor()
                             c.execute('UPDATE post SET polestate=%s WHERE id = %s', ["reserved",id])
                         
                           
             dbConnection.commit()
             c.close()
