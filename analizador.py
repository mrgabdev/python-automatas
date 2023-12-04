from flask import Flask, render_template, request
from transformers import pipeline
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición de tokens
tokens = (
    'NUMERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
)

# Expresiones regulares para los tokens
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Definición de la regla para el token NUMERO
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Variables para almacenar caracteres no reconocidos y mensajes de error de sintaxis
caracteres_no_reconocidos = []

# Variable para controlar si se debe imprimir el resultado
imprimir_resultado = True

# Manejo de errores
def t_error(t):
    global caracteres_no_reconocidos
    global imprimir_resultado
    caracteres_no_reconocidos.append(t.value[0])
    imprimir_resultado = False
    t.lexer.skip(1)


# Reglas de gramática y precedencia para el analizador sintáctico
def p_expresion(p):
    """
    expresion : expresion SUMA expresion
              | expresion RESTA expresion
              | expresion MULTIPLICACION expresion
              | expresion DIVISION expresion
              | PARENTESIS_IZQ expresion PARENTESIS_DER
              | NUMERO
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(' and p[3] == ')':
        p[0] = p[2]
    else:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            if p[3] != 0:
                p[0] = p[1] / p[3]
            else:
                print("División por cero")
                p[0] = None

# Regla de error para errores sintácticos
def p_error(p):
    global imprimir_resultado
    imprimir_resultado = False

# Construir el lexer
lexer = lex.lex()

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Analizando léxicamente la expresión que se ingrese
def evaluar_lexico(expresion):
    # Reiniciar la lista antes de cada análisis
    global caracteres_no_reconocidos
    caracteres_no_reconocidos = []

    # Ejecutar el lexer
    lexer.input(expresion)

    # Iterar sobre los tokens
    for token in lexer:
        pass  # No es necesario hacer nada aquí

    # Crear cadena de caracteres no reconocidos separados por coma
    caracteres_concatenados = ",".join(map(str, caracteres_no_reconocidos))

    return caracteres_concatenados

def analizador_sintactico(expresion):
    # Restablecer la variable de impresión del resultado
    global imprimir_resultado
    imprimir_resultado = True

    # Análisis de la expresión de entrada
    resultado = parser.parse(expresion, lexer=lexer)

    # Imprimir el resultado si se debe
    if imprimir_resultado:
        return resultado
    else:
        return "Error de sintaxis"

# Construir analizador semántico
def analizador_semantico(texto):
    sentiment_analyzer = pipeline('sentiment-analysis',
                                  model='nlptown/bert-base-multilingual-uncased-sentiment')
    resultado = sentiment_analyzer(texto)[0]
    sentimiento = resultado['label']
    print(f"Sentimiento: {sentimiento} ")
    return sentimiento


# Ruta principal del servidor flask
@app.route('/', methods=["GET", "POST"])
@app.route('/index.html', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # Cadena de entrada
        expresion = request.form['lexicalInput']
    else:
        expresion = ""

    caracteres_no_reconocidos = evaluar_lexico(expresion)

    # Retornar la cadena al renderizar la plantilla
    return render_template('index.html', caracteres_no_reconocidos=caracteres_no_reconocidos, expresion=expresion)


@app.route('/semantic.html', methods=["GET", "POST"])
def semantic():
    if request.method == 'POST':
        # Cadena de entrada
        expresion = request.form['semanticInput']

    else:
        expresion = ""

    sentimiento = analizador_semantico(expresion)
    return render_template('semantic.html', expresion = expresion, sentimiento = sentimiento)


@app.route('/syntax.html', methods=["GET", "POST"])
def syntax():
    # Inicialización de variables
    resultado = ""

    if request.method == 'POST':
        # Cadena de entrada
        expresion = request.form['syntaxInput']
        resultado = analizador_sintactico(expresion)
    else:
        expresion = ""

    # Retornar el resultado al renderizar la plantilla
    return render_template('syntax.html', resultado=resultado, expresion=expresion)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
