from flask import Flask, render_template, request
from ply import lex
import re

app = Flask(__name__)


def procesarCadena(entrada):
    # Implementa la lógica para procesar la cadena de entrada
    # Por propósitos de demostración, asumamos que simplemente convertimos a mayúsculas
    cadenaProcesada = entrada.upper()
    return cadenaProcesada


def checkSintaxisCorrect(entrada):
    if entrada != "":
        return True
    return "Error de sintaxis"


tokens = ("NUMERO", "SUMA", "RESTA", "MULTITPLICACION", "DIVISION")

t_SUMA = r"\+"
t_RESTA = r"\-"
t_MULTITPLICACION = r"\*"
t_DIVISION = r"\/"


def t_NUMERO(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_ignore = " \t\n"

incorrect_tokens = []


def t_error(t):
    print(f"Caracter erroneo: {t.value}")
    incorrect_tokens.append(t.value)
    t.lexer.skip(1)


def t_string(t):
    r"[A-Za-z=]"
    print(f"Illegal number: {t.value}")
    incorrect_tokens.append(t.value)
    t.lexer.skip(1)


# Función para manejar operadores consecutivos repetidos
def t_consecutive_repeated_operators(t):
    r"[+\-*/]{2,}"

    print(f"Illegal consecutive repeated operators: {t.value}")
    incorrect_tokens.append(t.value)
    t.lexer.skip(1)


def analizar_Lexico(codigo_fuente):
    analizador_lexico.input(codigo_fuente)

    for token in analizador_lexico:
        print(token)


analizador_lexico = lex.lex()


@app.route("/sintactico", methods=["POST"])
def sintactic_page():
    global incorrect_tokens
    incorrect_tokens = []
    cadena_sintactica = request.get_data(as_text=True)
    analizar_Lexico(cadena_sintactica)

    # Crear una expresión regular para buscar todos los tokens incorrectos
    patron = "|".join(re.escape(token) for token in incorrect_tokens)

    # Reemplazar todas las ocurrencias de incorrect_tokens con la variable reemplazo
    def reemplazo(match):
        token = match.group()
        return (
            f'<mark style="padding:0">{token}</mark>'
            if token in incorrect_tokens
            else token
        )

    cadena_sintactica = re.sub(patron, reemplazo, cadena_sintactica)

    return str(cadena_sintactica)


@app.route("/", methods=["GET", "POST"])
def homepage():
    cadenaProcesada = None
    if request.method == "POST":
        entrada = request.form.get("entrada")
        cadenaProcesada = procesarCadena(entrada)

    return render_template(
        "index.html", title="Analizador Semántico", cadenaProcesada=cadenaProcesada
    )


if __name__ == "__main__":
    app.run(debug=True)
