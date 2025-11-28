from flask import Flask, render_template, request

app = Flask(__name__)

# =================
# LÓGICA MATEMÁTICA 
# =================

def modelo_gauss_jordan(p, f, e):

    # Coeficientes
    coef_p = -0.025      # Precipitación (Estabilizador)
    coef_f = 0.0923      # Fugas (Factor Principal)
    coef_e = 0.0000137   # Extracción (Factor Acumulativo)
    
    prediccion = (p * coef_p) + (f * coef_f) + (e * coef_e)
    
    return max(0, prediccion)

def calcular_derivada(actual, anterior):

    return actual - anterior

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    
    # Valores iniciales 
    inputs = {
        'p': 764.0, 
        'f': 247.0, 
        'f_ant': 200.0, 
        'e': 618986.0
    }

    if request.method == 'POST':
        try:
            # Obtener datos del formulario HTML
            inputs['p'] = float(request.form['precipitacion'])
            inputs['f'] = float(request.form['fugas'])
            inputs['f_ant'] = float(request.form['fugas_anterior'])
            inputs['e'] = float(request.form['extraccion'])
            
            # Modelo Algebraico
            valor_exacto = modelo_gauss_jordan(inputs['p'], inputs['f'], inputs['e'])
            socavones_estimados = round(valor_exacto)
            
            
            derivada = calcular_derivada(inputs['f'], inputs['f_ant'])
            
            #Nivel de Riesgo (Semáforo)
            if socavones_estimados < 1:
                riesgo_texto = "Bajo"
            elif socavones_estimados < 5:
                riesgo_texto = "Moderado"
            else:
                riesgo_texto = "Crítico"

            # resultados para enviarlos al HTML
            resultado = {
                'estimados': int(socavones_estimados),
                'exacto': f"{valor_exacto:.4f}",
                'riesgo': riesgo_texto,
                'derivada': f"{derivada} rep/año",
                'derivada_valor': derivada, 
                # Desglose
                'aporte_p': f"{inputs['p'] * -0.025:.2f}",
                'aporte_f': f"{inputs['f'] * 0.0923:.2f}",
                'aporte_e': f"{inputs['e'] * 0.0000137:.2f}"
            }
            
        except ValueError:
            pass # Si el usuario mete texto en vez de números, recargamos sin error

    return render_template('index.html', res=resultado, inp=inputs)

if __name__ == '__main__':
    app.run(debug=True)