#!/usr/bin/python
# -*- coding: utf-8 -*- 

from flask import Flask, url_for, session, render_template, Response, request, flash, redirect, abort, jsonify
from flaskext.mysql import MySQL
import json
import time


mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('IROOM_SETTINGS', silent=True)
mysql.init_app(app)
last_value = [0,0,0,0,0]
type_sensor = ['temperature', 'humidity', 'light', 'sound', 'motion']
tipo_sensor =  ['temperatura', 'humedad', 'luz', 'sonido', 'movimiento']
def event_sensor():
        while True:		   
            conn = mysql.connect()
            cursor = conn.cursor()
            for x in range(5):
                cursor.execute ("""select valor from sensors where nombre=%s order by time desc""", type_sensor[x])
                valor = int(cursor.fetchone()[0])
                if valor != last_value[x]:
                        sensor = {"tipo":tipo_sensor[x], "valor":valor}
                        data_json = json.dumps(sensor)
                       #print (sensor)
                        yield 'data: %s\n\n' % str(data_json)
                        last_value[x] = valor
                        #flash('Actualizado sensor de temperatura')
@app.route('/post_acortador', methods=['GET','POST'])
def acortador():
    url = str(request.form.get("url"))
    codigo = str(request.form.get("codigo"))
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO acortador (codigo, url) VALUES (%s, %s)"
    cursor.execute (sql, (codigo, url))
    conn.commit()
    flash('Base de datos actualizada!')
    return redirect('/sensors', code=307)
@app.route('/URL/<codigo>')
def redireccionar(codigo):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute ("""select url from acortador where codigo=%s""", codigo)
    valor = (cursor.fetchone())
    if valor is not None:
        print(valor[0])
        return redirect(valor[0], code=307)
    else:
        return redirect('/', code=307)

@app.route('/update_sensor')
def sse_request():	  
        return Response(event_sensor(), mimetype='text/event-stream')
	  
@app.route('/', methods=['GET','POST'])
def main(): 
        return render_template('index.html')
		
@app.route('/sensors', methods=['GET','POST'])
def sensors():
        return render_template('sensors.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('Has entrado en la sesion')
			return redirect(url_for('sensors'))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Has salido de la sesion')
	return redirect(url_for('main'))


@app.route('/iluminacion')
def iluminacion():
	return render_template('iluminacion.html')
	

@app.route('/setcolor', methods=['GET'])
def setcolor():
    color = request.args.get('color')
    red = int('0x'+color[1:3],16)
    green = int('0x'+color[3:5],16)
    blue = int('0x'+color[5:7],16)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO sensors(nombre, valor)" "values(%s, %s)", ('red', red))
    cursor.execute ("INSERT INTO sensors(nombre, valor)" "values(%s, %s)", ('green', green))
    cursor.execute ("INSERT INTO sensors(nombre, valor)" "values(%s, %s)", ('blue', blue))
    conn.commit()
    print('El color rojo modificado tiene un valor de ' + str(red) + ', el color verde tiene un valor de ' + str(green) + ' y el azul tiene un valor de ' + str(blue))
    return 'Ok'	
 

if __name__=='__main__':
	with app.test_request_context():
		app.debug = True
		app.run(host ='0.0.0.0')
		
