from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
# ¡IMPORTANTE! Necesitas una clave secreta para usar sesiones
app.secret_key = os.environ.get('SECRET_KEY', 'default_fallback_key_usar_solo_dev') 
CSV_FILE = 'respuestas.csv'

# Datos estáticos del formulario (Carreras, etc.)
CARRERAS = [
    "Ingeniería en Desarrollo y Gestión de Software", "Ingeniería en Mecatrónica", 
    "Ingeniería en Energías Renovables", "Licenciatura en Innovación de Negocios y Mercadotecnia",
    "Licenciatura en Desarrollo y Gestión Turística", "Licenciatura en Protección Civil y Emergencia"
]
# Simulamos los municipios de Jalisco
MUNICIPIOS = ['ACATIC', 'ACATLÁN DE JUÁREZ', 'AHUALULCO DE MERCADO', 'AMACUECA', 'AMATITÁN', 'AMECA', 'SAN JUANITO DE ESCOBEDO',
'ARANDAS', 'EL ATOYAC', 'AUTLÁN DE NAVARRO', 'AYOTLÁN', 'BOLAÑOS', 'CABO CORRIENTES', 'CASIMIRO CASTILLO', 'CIHUATLÁN', 'COCULA',
'COLOTLÁN', 'CONCEPCIÓN DE BUENOS AIRES', 'CUAUTITLÁN DE GARCÍA BARRAGÁN', 'CUAUTLA', 'CUIJINGO', 'DEGOLLADO', 'EJUTLA', 'EL GRULLO',
'EL LIMÓN', 'EL SALTO', 'ENCARNACIÓN DE DÍAZ', 'ETZATLÁN', 'GUACHINANGO', 'GUADALAJARA', 'HOSTOTIPAQUILLO', 'HUEJUQUILLA EL ALTO',
'HUILA', 'IXTLAHUACÁN DE LOS MEMBRILLOS', 'IXTLAHUACÁN DEL RÍO', 'JALOSTOTITLÁN', 'JAMAY', 'JOCOTEPEC', 'JUANACATLÁN', 'JUCHITLÁN',
'LA BARCA', 'LA HUERTA', 'LA MANZANILLA DE LA PAZ', 'LAGOS DE MORENO', 'LEÓN', 'LIMÓN DE LOS RAMÍREZ', 'MAGDALENA', 'MAZAMITLA',
'MEZQUITIC', 'MEXTICACÁN', 'MIGUEL HIDALGO', 'MIXTLÁN', 'OCOTLÁN', 'OJUELOS DE JALISCO', 'PONCITLÁN', 'PUERTO VALLARTA',
'QUITUPÁN', 'SAN CRISTÓBAL DE LA BARRANCA', 'SAN DIEGO DE ALEJANDRÍA', 'SAN JUAN DE LOS LAGOS', 'SAN MARTÍN DE BOLAÑOS',
'SAN MARTÍN HIDALGO', 'SAN MIGUEL EL ALTO', 'SAN SEBASTIÁN DEL OESTE', 'SANTA MARÍA DE LOS ÁNGELES', 'SAYULA', 'TALA', 'TALPA DE ALLENDE',
'TAMAZULA DE GORDIANO', 'TAPALPA', 'TEOCALTICHE', 'TEOCUITATLÁN DE CORONA', 'TEPATITLÁN DE MORELOS', 'TEQUILA', 'TLAJOMULCO DE ZÚÑIGA',  
'TLAQUEPAQUE', 'TONALÁ', 'TONAYA', 'TONILA', 'TOTATICHE', 'TOTOTLÁN', 'TUXCACUESCO', 'TUXCUECA', 'TUXPAN', 'UNIÓN DE SAN ANTONIO', 'UNIÓN DE TULA', 
'VALLE DE GUADALUPE', 'VALLE DE JUÁREZ', 'VILLA CORONA', 'VILLA GUERRERO', 'VILLA HIDALGO', 'YAHUALICA DE GONZÁLEZ GALLO', 'ZACOALCO DE TORRES', 'ZAPOPAN', 
'ZAPOTILTIC', 'ZAPOTLÁN DEL REY', 'ZAPOTLÁN EL GRANDE',] 

# Definición de todas las columnas posibles para el CSV
FIELDNAMES = [
    # Sección I
    'genero', 'edad', 'municipio', 'carrera',
    # Sección II
    'ha_leido_12m',
    # Sección III y IV (Habitos y Preferencias)
    'libros_leidos_12m', 'formato_fisico', 'formato_ebook', 'formato_audiolibro',
    'tiempo_lectura_semanal', 'tipos_libros_principal', 'generos_literarios', # Nota: generos_literarios será un string unido
    # Sección V
    'razon_no_lectura',
    # Sección VI y VII
    'quiere_resultados', 'comentario_adicional', 'email_resultados'
]

# --- Rutas de la Aplicación ---

@app.route('/')
def inicio():
    session.clear() 
    return redirect(url_for('paso1_datos'))

# 1. Sección I: Datos Estadísticos
@app.route('/paso1', methods=['GET', 'POST'])
def paso1_datos():
    if request.method == 'POST':
        session['genero'] = request.form.get('genero')
        session['edad'] = request.form.get('edad')
        session['municipio'] = request.form.get('municipio')
        session['carrera'] = request.form.get('carrera')
        # Redirige a 'paso2_lectura'
        return redirect(url_for('paso2_lectura'))
    return render_template('paso1_datos.html', municipios=MUNICIPIOS, carreras=CARRERAS)

# 2. Sección II: Actividad de la Lectura (Define el flujo)
@app.route('/paso2', methods=['GET', 'POST'])
# NOTA: Cambiamos el nombre de la función a 'paso2_lectura' para que coincida con url_for del Paso 1
def paso2_lectura(): 
    if request.method == 'POST':
        ha_leido = request.form.get('ha_leido_12m')
        session['ha_leido_12m'] = ha_leido

        if ha_leido == 'Sí':
            return redirect(url_for('paso3_habitos'))
        else:
            return redirect(url_for('paso4_no_lectura'))
            
    # Asegúrate de que esta plantilla existe
    return render_template('paso2_lectura.html')
# 3. Sección III y IV: Hábitos y Preferencias (Solo si ha_leido == 'Sí')
# Nota: Implementaremos el bucle "while" de géneros literarios con JavaScript o simplemente guardando una lista multi-select. 
@app.route('/paso3', methods=['GET', 'POST'])
def paso3_habitos():
    if request.method == 'POST':
        # III. Hábitos
        session['libros_leidos_12m'] = request.form.get('libros_leidos')
        session['formato_fisico'] = request.form.get('fisico')
        session['formato_ebook'] = request.form.get('ebook')
        session['formato_audiolibro'] = request.form.get('audiolibro')
        session['tiempo_lectura_semanal'] = request.form.get('tiempo_semanal')
        
        # IV. Preferencias
        session['tipos_libros_principal'] = request.form.get('tipo_principal')
        
        # Manejo de la selección múltiple de géneros (simula el while)
        generos_seleccionados = request.form.getlist('generos_literarios')
        session['generos_literarios'] = " | ".join(generos_seleccionados) # Unimos para guardar en un campo CSV
        
        return redirect(url_for('paso5_comentarios')) # Salta directamente a la Sección VI    
    return render_template('paso3_habitos.html')


# 4. Sección V: Razón de No Lectura (Solo si ha_leido == 'No')
@app.route('/paso4', methods=['GET', 'POST'])
def paso4_no_lectura():
    if request.method == 'POST':
        session['razon_no_lectura'] = request.form.get('razon')
        # Llenamos campos vacíos para mantener la consistencia del CSV
        session['libros_leidos_12m'] = session['formato_fisico'] = session['formato_ebook'] = session['formato_audiolibro'] = None
        session['tiempo_lectura_semanal'] = session['tipos_libros_principal'] = session['generos_literarios'] = None
        
        return redirect(url_for('paso5_comentarios')) # Ir a la Sección VI
        
    return render_template('paso4_no_lectura.html')

# 5. Sección VI y VII: Comentarios y Email
@app.route('/paso5', methods=['GET', 'POST'])
def paso5_comentarios():
    if request.method == 'POST':
        quiere_resultados = request.form.get('quiere_resultados')
        session['quiere_resultados'] = quiere_resultados
        session['comentario_adicional'] = request.form.get('comentario_adicional')
        
        email = None
        if quiere_resultados == 'Sí, por favor':
            email = request.form.get('email_resultados')
            
        session['email_resultados'] = email
        
        # Finalizar y guardar los datos
        guardar_respuestas(session)
        
        return redirect(url_for('fin_encuesta'))
        
    # Lógica para mostrar/ocultar el campo de email con JavaScript
    return render_template('paso5_comentarios.html')


@app.route('/fin')
def fin_encuesta():
    session.clear()
    return render_template('fin_encuesta.html')


# Función de guardado centralizado
def guardar_respuestas(respuestas):
    """Escribe los datos de la sesión en el archivo CSV."""
    
    # Creamos un diccionario con todos los campos, usando None si no existen
    data_to_save = {key: respuestas.get(key) for key in FIELDNAMES}
    
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter=';') # Usamos ';' para evitar conflictos con comas en los comentarios
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(data_to_save)

if __name__ == '__main__':
    # Inicializa el CSV con encabezados si no existe
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter=';')
            writer.writeheader()
            
    app.run(debug=True)