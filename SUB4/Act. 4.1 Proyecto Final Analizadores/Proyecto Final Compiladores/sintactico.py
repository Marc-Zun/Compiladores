#Importando Librerias
import re
import tkinter as tk
from tkinter import messagebox
from ply import lex, yacc
from subprocess import call

#Definir los tokens
tokens = (

    'WHILE',
    'SYSTEM',
    'OUT',
    'INT',
    'ID',
    'NUM',
    'STRING',
    'PLUS',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'DOT',
    'EQUALS',
    'LEQ',
    "MAYOR",
    "MENOR",
    "COM",
    'PRINTLN',
     
)
t_PLUS = r'\+'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_DOT = r'\.'
t_EQUALS = r'='
t_LEQ = r'<=' 
t_MAYOR = r'>'
t_MENOR = r'<'
t_COM = r'"'


def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1] 
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value == 'while':
        t.type = 'WHILE'
    elif t.value == 'int':
        t.type = 'INT'
    elif t.value == 'println':
        t.type = 'PRINTLN'
    elif t.value == 'System':
        t.type = 'SYSTEM'
    elif t.value == 'out':
        t.type = 'OUT'
    return t
# Regla para identificar números
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

def t_error(t):
    error_message(f"Token desconocido '{t.value[0]}'", t.lineno)
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Variable global para verificar si la sintaxis es correcta
is_syntax_correct = True
error_info = None  # Almacena información sobre el error si hay alguno


# Definición de la gramática para el análisis sintáctico
def p_while_loop(p):
    '''while_loop : INT ID EQUALS NUM SEMICOLON WHILE LPAREN ID LEQ NUM RPAREN LBRACE SYSTEM DOT OUT DOT PRINTLN LPAREN ID RPAREN SEMICOLON ID PLUS PLUS SEMICOLON RBRACE'''
    pass

# Manejo de errores de sintaxis
def p_error(p):
    global is_syntax_correct, error_info
    is_syntax_correct = False
    if p:
        error_info = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}"
    else:
        error_info = "Error de sintaxis: final inesperado del código"

# Construcción del parser
parser = yacc.yacc()

# Función para el análisis léxico
def lex_analyzer(code):
    lexer.input(code)
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append((token.lineno, token.type, token.value))
    return tokens

# Función para el análisis sintáctico
def parse_code(code):
    parser.parse(code, lexer=lexer)

def error_message(message, line_number):
    messagebox.showerror("Error de sintaxis", f"{message}\n En la línea {line_number}")

# Función para procesar el código ingresado
def process_code():
    global is_syntax_correct, error_info
    code = code_text.get("1.0", "end-1c")
    tokens = lex_analyzer(code)
    result_text.delete("1.0", "end")
    is_syntax_correct = True
    error_info = None
    try:
        parser.parse(code, lexer=lexer)
    except Exception as e:
        is_syntax_correct = False
        error_info = f"Error durante el análisis sintáctico: {e}"

    for token in tokens:
        line_number, token_type, token_value = token
        result_text.insert("end", f"Línea ->: {token_type} -> {token_value}\n")

    if is_syntax_correct:
        messagebox.showinfo("Análisis Sintáctico", "Todo está correcto.")
    else:
        messagebox.showerror("Error de Sintaxis", error_info)
        
def regresar():
    window.destroy()
    call(["python", "main.py"])

# Creación de la ventana de la interfaz gráfica
window = tk.Tk()
window.title("Analizador Sintactico")
window.geometry("490x590")
window.configure(bg='#FFF2D8')

#Crea una etiqueta para el titulo de la aplicacion
text_label = tk.Label(window, text="----- ANALIZADOR SINTÁCTICO -----", height=1, width=50, font=("Arial", 20, 'bold'), fg="#FFF3DA", bg="#141E46")
text_label.pack()


# Etiqueta y campo de texto para ingresar el código
code_label = tk.Label(window, text="Ingrese el código:", font=("ARIAL", 14), bg='#FFF2D8')
code_label.pack(pady=10)

code_text = tk.Text(window, height=10, width=50)
code_text.pack()

# Botón para procesar el código
#process_button = tk.Button(window, text="Procesar", command=process_code, font=("ARIAL", 14),bg='#64CCC5')
#process_button.pack(pady=10)

# Crear un frame para los botones
button_frame = tk.Frame(window, bg='#FFF2D8')
button_frame.pack(pady=10)

# Botón para procesar el código
process_button = tk.Button(button_frame, text="Analizar", command=process_code, font=("ARIAL", 14), bg="#A8DF8E")
process_button.grid(row=0, column=0, padx=5)

# Botón para limpiar el código ingresado
clear_button = tk.Button(button_frame, text="Limpiar", command=lambda: (code_text.delete("1.0", "end-1c"), result_text.delete("1.0", "end")), font=("ARIAL", 14), bg="#FFC436")
clear_button.grid(row=0, column=1, padx=5)

# Botón para salir del programa
exit_button = tk.Button(button_frame, text="Salir", command=window.destroy, font=("ARIAL", 14), bg="#FF6969")
exit_button.grid(row=0, column=2, padx=5)

# Etiqueta y campo de texto para mostrar los tokens
result_label = tk.Label(window, text="Tokens:", font=("ARIAL", 14), bg='#FFF2D8')
result_label.pack(pady=5)

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

regresar_button = tk.Button(window, text="Regresar al menú", command=regresar, font=("Arial", 16, 'bold'), bg="#61A3BA")
regresar_button.pack(pady=20)

# Ejecución de la interfaz gráfica
window.mainloop()


    
