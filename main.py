from flask import Flask, render_template, request
from ply import lex


# Flask instance
app = Flask(__name__)


def procesarCadena(entrada):
    if entrada is not None:
        # Implementa la lógica para procesar la cadena de entrada
        cadenaProcesada = entrada.upper()
        return cadenaProcesada
    else:
        return None
def checkSintaxisCorrect(entrada):
    if entrada != "":
        return True
    return "Error de sintaxis"

# Mis identificadores
tokens = (
        'NUMERO',
        'SUMA',
        'RESTA',
        'MULTIPLICACION'
    )

t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULTIPLICACION = r'\*'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'


def t_error(t):
    print(f'Caracter erroneo: {t.value[0]}')
    t.lexer.skip(1)


# Inicializar analizador lexico fuera de la función
analizadorLexico = lex.lex()

def analizarLexico(codigoFuente):
    if codigoFuente is not None:
        # Assuming `analizadorLexico` is some lexer object
        analizadorLexico.input(codigoFuente)

        # Initialize an empty array to store token types
        token_types = []

        for token in analizadorLexico:
            # Append the type of each token to the array
            token_types.append(token.type)

        # Return the array of token types
        return token_types
    else:
        return None

def analizarSintaxis(tokens):
    if tokens is not None:
        pila = []
        operadores = {'SUMA', 'RESTA', 'MULTIPLICACION'}

        for token in tokens:
            if token in operadores:
                # Verificar si hay operandos suficientes en la pila
                if len(pila) < 2:
                    print("Error de sintaxis: Falta operandos para el operador " + token)
                else:
                    # Realizar la operación y apilar el resultado
                    operand2 = pila.pop()
                    operand1 = pila.pop()
                    if token == 'SUMA':
                        resultado = operand1 + operand2
                        print(f"Operación SUMA: {operand1} + {operand2} = {resultado}")
                    elif token == 'RESTA':
                        resultado = operand1 - operand2
                        print(f"Operación RESTA: {operand1} - {operand2} = {resultado}")
                    elif token == 'MULTIPLICACION':
                        resultado = operand1 * operand2
                        print(f"Operación MULTIPLICACION: {operand1} * {operand2} = {resultado}")
                    pila.append(resultado)
            else:
                # Si no es un operador, asumimos que es un número y lo apilamos
                pila.append(token)

        # Al final, debe haber un solo resultado en la pila
        if len(pila) == 1:
            print(f"Resultado final: {pila[0]}")
            return pila[0]
        else:
            print("Error de sintaxis: Demasiados operandos")
    else:
        return []

@app.route("/", methods=["GET", "POST"])
def homepage():
    cadenaProcesada = None
    codigoAnalizado = None  # Nueva variable para almacenar el resultado del análisis léxico
    resultadoSintactico = None  # Nueva variable para almacenar el resultado del análisis sintáctico

    if request.method == "POST":
        entrada = request.form.get("entrada")
        codigoFuenteSintactico = request.form.get("codigoFuente")  # Nuevo campo en el formulario
        cadenaProcesada = procesarCadena(entrada)
        codigoAnalizado = analizarLexico(codigoFuenteSintactico)

        # Realizar análisis léxico
        tokens = analizarLexico(codigoFuenteSintactico)

        # Realizar análisis sintáctico
        resultadoSintactico = analizarSintaxis(tokens)

    return render_template("index3.html", title="Lenguajes y Automatas II", cadenaProcesada=cadenaProcesada, codigoAnalizado=codigoAnalizado, resultadoSintactico=resultadoSintactico)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)