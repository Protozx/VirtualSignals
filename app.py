from flask import Flask, render_template
from flask import request
from proy import * 
from elemental2 import *
from flask import jsonify
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
    print((int(amplitud),int(frecuencia),int(muestration),int(desplazamiento),int(periodo),(float(sigma)/100),(float(omega)/100),float(frec_ang),float(angulo_fase),par,continuidad,tipo,id))    
    return "no"

@app.route('/urias', methods=['POST'])
def urias():
    global v
    
    return v

@app.route('/filtrodel1', methods=['POST'])
def filtrodel1():
    global v
    
    return v

@app.route('/integrar', methods=['POST'])
def integrar():
    global v
    
    return v

@app.route('/diferenciar', methods=['POST'])
def diferenciar():
    global v
    
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
