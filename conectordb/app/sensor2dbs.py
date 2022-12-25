#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import json
import urllib3
import mysql.connector

db = mysql.connector.connect(host = "172.0.0.3", user = "root", passwd = "secret", db = "iroom")

type_sensor = ['temperature', 'humidity', 'light', 'sound', 'motion']
last_value = [0,0,0,0,0,0,0,0]

#PONER LA IP DE LA MÁQUINA VIRTUAL EN LA QUE ESTÉ CORRIENDO EL EMULADOR
server = 'http://172.0.0.6:8000/'
#server = 'http://10.0.21.132:8000/'
http = urllib3.PoolManager()
def updateSensor(code):
        value = 0
        try:
            for x in range(5):
                response = http.request('GET', server + type_sensor[x])
                data = json.loads(response.data)
                last_value[x] = data[type_sensor[x]]
                print(type_sensor[x],"---->", last_value[x])

        except ValueError:
                print ('Error al recibir datos')
        if value != last_value[code]:
                try:
                    for x in range(5):
                        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", (type_sensor[x], last_value[x]))
                    db.commit()
                except ValueError:
                        print ('Error al insertar en base de datos')

def controlLightColor():
        try:
                cursor.execute ("""SELECT valor FROM sensors WHERE nombre='red' order by time desc""")
                red = int(cursor.fetchone()[0])
                if (red != last_value[5]):
                        last_value[5] = red
                        print ("red:" + str(red))
                        response = http.request('PUT', server+'red/'+str(red))

                cursor.execute ("""SELECT valor FROM sensors WHERE nombre='green' order by time desc""")
                green = int(cursor.fetchone()[0])
                if (green != last_value[6]):
                        last_value[6] = red
                        print ("green:" + str(green))
                        response = http.request('PUT', server+'green/'+str(green))

                cursor.execute ("""SELECT valor FROM sensors WHERE nombre='red' order by time desc""")
                blue = int(cursor.fetchone()[0])
                if (blue != last_value[7]):
                        last_value[7] = red
                        print ("blue:" + str(blue))
                        response = http.request('PUT', server+'blue/'+str(blue))


        except ValueError:
                print ('Error al consultar de base de datos o conectar con iroom')

if __name__ == "__main__":
        time.sleep(15)
        cursor=db.cursor(buffered=True)
        cursor.execute ("""DROP table sensors""")
        cursor.execute ("""create table sensors( time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, nombre VARCHAR(15), valor INTEGER)""")
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('temperature', 20))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('humidity', 40))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('light', 30))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('sound', 10))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('motion', 0))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('red', 20))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('blue', 20))
        cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('green', 20))
        db.commit()
        print ('Base de datos creada, comienza la consulta de sensores')
        while True:
                for code in range(0, 5):
                        updateSensor(code)
                        time.sleep(1)
                controlLightColor()
