from flask import Flask, render_template
from flask import request
from proy import * 
from elemental2 import *
from basu import *
from flask import jsonify
import json
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
    amplitudreal = request.form.get('amplitudreal')

    amplitud = float(amplitud) * float(amplitudreal)

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
    inicio = request.form.get('inicio')
    fin = request.form.get('fin')

    print(id)
    #time.sleep(10)
    generar_grafica(id, str(tipo), float(amplitud),float(periodo),int(muestration),-1*float(desplazamiento),float(inicio), float(fin), (float(sigma)),(float(omega)),float(frec_ang),float(angulo_fase),str(par),int(continuidad))
        
    return "no"

@app.route('/urias', methods=['POST'])
def urias(): 
    global v
    json_data = request.get_json()

    datosA = json_data['datosA']
    datosB = json_data['datosB']
    operacion = json_data['tipo']
    puerko = json_data['idresultante']
    #print(f"{datosA}, {type(datosA)}")
    """PaqueteA = json.loads(datosA)
    PaqueteB = json.loads(datosB)"""
    PaqueteA = datosA
    PaqueteB = datosB

    id_A = PaqueteA["id"]
    tipo_A = PaqueteA["tipo"]
    amplitud_A = PaqueteA["amplitud"]
    periodo_A = PaqueteA["periodo"]
    muestration_A = PaqueteA["muestration"]
    desplazamiento_A = PaqueteA["desplazamiento"]
    inicio_A = PaqueteA["inicio"]
    fin_A = PaqueteA["fin"]
    sigma_A = PaqueteA["sigma"]
    omega_A = PaqueteA["omega"]
    frec_angular_A = PaqueteA["frecuencia_angular"]
    angulo_fase_A = PaqueteA["angulo_fase"]
    par_A = PaqueteA["par"]
    continuidad_A = PaqueteA["continuidad"]

    id_B = PaqueteB["id"]
    tipo_B = PaqueteB["tipo"]
    amplitud_B = PaqueteB["amplitud"]
    periodo_B = PaqueteB["periodo"]
    muestration_B = PaqueteB["muestration"]
    desplazamiento_B = PaqueteB["desplazamiento"]
    inicio_B = PaqueteB["inicio"]
    fin_B = PaqueteB["fin"]
    sigma_B = PaqueteB["sigma"]
    omega_B = PaqueteB["omega"]
    frec_angular_B = PaqueteB["frecuencia_angular"]
    angulo_fase_B = PaqueteB["angulo_fase"]
    par_B = PaqueteB["par"]
    continuidad_B = PaqueteB["continuidad"]
    tupla_A = id_A, str(tipo_A), float(amplitud_A),float(periodo_A),int(muestration_A),float(desplazamiento_A),float(inicio_A), float(fin_A), (float(sigma_A)),(float(omega_A)),float(frec_angular_A),float(angulo_fase_A),str(par_A),int(continuidad_A)
    tupla_B = id_B, str(tipo_B), float(amplitud_B),float(periodo_B),int(muestration_B),float(desplazamiento_B),float(inicio_B), float(fin_B), (float(sigma_B)),(float(omega_B)),float(frec_angular_B),float(angulo_fase_B),str(par_B),int(continuidad_B)
    operar_senales(tupla_A, tupla_B, operacion, puerko)
    #datosA = request.form.get('datosA')
    #datosB = request.form.get('datosB')
    #operacion = request.form.get('tipo')
    #data1_dict = json.loads(datosA)
    #print(data1_dict)

    # Obtener el valor de 'a'
    # a_value = data1_dict.get('a')
    
    #operar_senales(datosA, datosB, operacion)
    return v

@app.route('/filtrodel1', methods=['POST'])
def filtrodel1():
    global v
    poder = request.form.get('poder')
    id_señal = request.form.get('id')
    id_filtro1 = request.form.get('idintegral')
    x,y = leer_csv(f"static/data/{id_señal}.csv", "x", "y")
    x,y = filtro_del_1(x, y, float(poder))
    escrbir_csv(f"{id_filtro1}.csv", "x", "y", x, y)
    
    return v

@app.route('/integrar', methods=['POST'])
def integrar():
    id_señal = request.form.get('id')
    id_integral = request.form.get('idintegral')
    x,y = leer_csv(f"static/data/{id_señal}.csv", "x", "y")
    x,y = integrar_fx(x, y)
    escrbir_csv(f"{id_integral}.csv", "x", "y", x, y)

 
    
    return v

@app.route('/reflexion', methods=['POST'])
def reflexion():
    id_señal = request.form.get('id')
    x,y = leer_csv(f"static/data/{id_señal}.csv", "x", "y")
    x,y = reflejar(x, y)
    escrbir_csv(f"{id_señal}.csv", "x", "y", x, y)

 
    
    return v

@app.route('/diferenciar', methods=['POST'])
def diferenciar():
    id_señal = request.form.get('id')
    id_integral = request.form.get('idintegral')
    filtro = request.form.get('filtro')
    x,y = leer_csv(f"static/data/{id_señal}.csv", "x", "y")
    x,y = derivar_fx(x, y)
    escrbir_csv(f"{id_integral}.csv", "x", "y", x, y)
    
    return v



@app.route('/practica5', methods=['POST'])
def practica5():
    tipo = request.form.get('tipo')
    id = request.form.get('id')
    mue_mz = request.form.get('mue_mz')
    og_mz = request.form.get('og_mz')
    segundos = request.form.get('segundos')
    if tipo == '14':
        paso1(float(segundos),float(mue_mz),id)
    else:
        paso2(float(segundos),float(og_mz),float(mue_mz),id)
    

    return v

@app.route('/practica7', methods=['POST'])
def practica7():
    tipo = request.form.get('tipo')
    id = request.form.get('id')
    bits = request.form.get('bits')
    tipotipo = request.form.get('tipotipo')
    josue = request.form.get('josue')
    p33(int(josue),int(tipotipo),int(bits),id)
    

    return v

@app.route('/cortito', methods=['POST'])
def cortito():
    tipo = request.form.get('tipo')
    id = request.form.get('id')
    esc_tiempo = request.form.get('esc_tiempo')
    corrimiento = request.form.get('corrimiento')
    print(esc_tiempo)
    print(corrimiento)
    x,y = leer_csv(f"static/data/{id}.csv", "x", "y")
    x,y = desplazamiento(x, y, float(corrimiento))
    x, y = escalamiento_tiempo(x, y, float(esc_tiempo), False)
    escrbir_csv(f"{id}.csv", "x", "y", x, y)

    

    return v



@app.route('/audio', methods=['POST'])
def audio():
    # Ensure there's a file named 'audio' in the request
    #if 'audio' not in request.files:
    #    return jsonify({'error': 'No audio file found'}), 400

#    audio_file = request.files['audio']
 #   id_value = request.form.get('id')  # Get other data, like the 'id'

    # Now you can save or process the audio_file as you see fit
    # Example: Save the file locally
  #  file_path = f"uploads/{id_value}.wav"  # Assuming it's a .wav file
   # audio_file.save(file_path)

    return jsonify({'success': True, 'message': 'File uploaded successfully!'}), 200


    


if __name__ == '__main__':
    app.run()
