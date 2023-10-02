from flask import Flask, render_template
from flask import request
from proy import * 
from elemental2 import *
#import time


app = Flask(__name__, static_folder='static')
v = ""

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/imagenes')
def imagenes():
    return render_template('imagenes.html')

@app.route('/esperanza')
def esperanza():
    return render_template('esperanza.html')


@app.route('/datos', methods=['POST'])
def datos():
    global v
    amplitud = request.form.get('amplitud')
    frecuencia = request.form.get('frecuencia')
    muestration = request.form.get('muestration')
    desplazamiento = request.form.get('desplazamiento')
    periodo = request.form.get('periodo')
    sigma = request.form.get('sigma')
    omega = request.form.get('omega')
    frec_ang = request.form.get('frecuencia_angular')
    angulo_fase = request.form.get('angulo_fase')
    par = request.form.get('par')
    continuidad = request.form.get('continuidad')
    tipo = request.form.get('tipo')
    id = request.form.get('id')
    #time.sleep(10)
    generar_grafica(int(amplitud),int(frecuencia),int(muestration),int(desplazamiento),int(periodo),(float(sigma)/100),(float(omega)/100),float(frec_ang),float(angulo_fase),par,continuidad,tipo,id)
    
    return "no"

@app.route('/fredy', methods=['POST'])
def fredy():
    global v
    
    return v

if __name__ == '__main__':
    app.run()
