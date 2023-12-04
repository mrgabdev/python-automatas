# Importación de los módulos necesarios de la biblioteca ply
import ply.lex as lex
import ply.yacc as yacc

# Lista de nombres de tokens
tokens = (
    'NUMERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'PARENIZQUIERDO',
    'PARENDERECHO',
)

# Reglas de expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_PARENIZQUIERDO = r'\('
t_PARENDERECHO = r'\)'

# Expresión regular para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios en blanco
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    global imprimir_resultado
    imprimir_resultado = False
    t.lexer.skip(1)
    print("Carácter inválido")
    return False

# Reglas de gramática y precedencia para el analizador sintáctico
def p_expresion(p):
    """
    expresion : expresion SUMA expresion
              | expresion RESTA expresion
              | expresion MULTIPLICACION expresion
              | expresion DIVISION expresion
              | PARENIZQUIERDO expresion PARENDERECHO
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
                imprimir_resultado = False
                print("División por cero")
                p[0] = None

# Regla de error para errores sintácticos
def p_error(p):
    global imprimir_resultado
    imprimir_resultado = False
    print("Error de sintaxis")
    return False

# Construcción del analizador léxico
lexer = lex.lex()

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Bucle principal para continuar o salir
while True:
    # Restablecer la variable de impresión del resultado
    imprimir_resultado = True

    # Entrada de la expresión desde el usuario
    expresion = input("Ingrese una expresión aritmética: ")

    # Análisis de la expresión de entrada
    resultado = parser.parse(expresion, lexer=lexer)

    # Imprimir el resultado si se debe
    if imprimir_resultado:
        print("Resultado:", resultado)

    # Preguntar al usuario si desea continuar
    continuar = input("¿Desea continuar? (s/n): ")
    if continuar.lower() != 's':
        break