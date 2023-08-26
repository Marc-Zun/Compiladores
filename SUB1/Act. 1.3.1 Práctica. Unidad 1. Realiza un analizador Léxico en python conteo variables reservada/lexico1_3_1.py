#Librerias
import tkinter as tk
import re
from tkinter import ttk

#Define una clase Lexer para el análisis léxico
class Lexer:
    def __init__(self):
        #Lista de palabras reservadas, operadoes y delimitadores
        self.RESERVADA = ['for', 'do', 'while', 'if', 'else', 'public', 'static', 'void', 'int','main']
        self.OPERADOR = ['=', '+', '-', '*', '/']
        self.DELIMITADOR = ['(', ')', '{', '}', ';']

        #Expresiones regulares para patrones de tokens
        self.tokens_regex = {
            'RESERVADA': '|'.join(r'\b' + re.escape(keyword) + r'\b' for keyword in self.RESERVADA),
            'OPERADOR': '|'.join(map(re.escape, self.OPERADOR)),
            'DELIMITADOR': '|'.join(map(re.escape, self.DELIMITADOR)),
            'NÚMERO': r'\d+(\.\d+)?',   #Patrón para números enteros y decimales
            'IDENTIFICADOR': r'[A-Za-z_]+'  #Patrón para identificadores
        }
        #Compila las expresiones regulares en un patrón combinado
        self.token_patterns = re.compile('|'.join(f'(?P<{t}>{self.tokens_regex[t]})' for t in self.tokens_regex))
    
    #Tokeniza el texto de entrada
    def tokenize(self, text):
        tokens = []     #Lista para almacenar los tokens
        lines = text.split('\n') #Divide el texto de entrada en líneas
        NumeroLinea = 1  #Inicializa el número de línea
        #Itera a través de cada línea del texto
        for line in lines:
            line_has_tokens = False  #Bandera para verificar si la línea tiene tokens
            #Busca los patrons de tokens en la línea actual 
            for match in self.token_patterns.finditer(line):
                line_has_tokens = True
                #Itera a través de los grupos coincidentes de la expresión regular
                for token_type, token_value in match.groupdict().items():
                    #Verifica el tipo de token y su longitud
                    if token_type == 'IDENTIFICADOR' and token_value and len(token_value) > 1:
                        tokens.append((NumeroLinea, 'ERROR LÉXICO', token_value))    #Agrega un token de error léxico
                    elif token_type == 'IDENTIFICADOR' and token_value and len(token_value) == 1:
                        tokens.append((NumeroLinea, 'IDENTIFICADOR', token_value))  #Agrega un token identificador
                    elif token_value:
                        tokens.append((NumeroLinea, token_type, token_value))  #Agrega un token con su tipo y valor
            #Si la linea tiene tokens, incrementa el número de línea
            if line_has_tokens:
                NumeroLinea += 1
        return tokens  #Devuelve la lista de tokens resultante

    #Realiza el análisis de los tokens y genera una cadena de resultados 
    def analyze(self, text):
        tokens = self.tokenize(text) #Tokeniza el texto de entrada
        result = "Token\t\tLexema\t\tLinea\n"  #Crea una cadena para almacenar los resultados formateados
        for line_number, token_type, token_value in tokens:  #Itera a través de la lista de tokens generados
            result += f"{token_type}\t\t{token_value}\t\t{line_number}\n"   #Agrega una línea formateada al resultado 
        return result  #Devuelve la cadena de resultados

#Define una clase LexerApp para la interfaz gráfica de usurio
class LexerApp: 
    def __init__(self):  #Define una clase llamda LexerApp para la interfaz grafica de usuario
        self.windows = tk.Tk() #Crea una ventana de la clase
        self.windows.title("Analizador léxico") #Establece el titulo de la ventana

        #Crea una etiqueta para el titulo de la aplicacion
        self.text_label = tk.Label(text="----- ANALIZADOR LÉXICO -----", height=2, width=45, font=("Arial", 15, 'bold'), fg="#FFF3DA", bg="#141E46")
        self.text_label.pack(pady=5)

        #Crea un cuadro de texto para la entrada de texto
        self.text_input = tk.Text(self.windows, height=8, width=55, font=("Arial", 12))
        self.text_input.pack(pady=5)

        #Crea un marco para los botones
        self.button_frame = tk.Frame(self.windows)
        self.button_frame.pack()

        #crea un boton para realizar el analisis lexico del texto de entrada
        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_text, bg="#A8DF8E", font=("Arial", 14, 'bold'))
        self.analyze_button.grid(row=0, column=0, padx=30, pady=10)

        #crea un boton para limpiar el cuadro de texto
        self.clean_button = tk.Button(self.button_frame, text="Limpiar", command=self.clean_text, bg="#FFC436", font=("Arial", 14, 'bold'))
        self.clean_button.grid(row=0, column=1, padx=30, pady=10)

        #Crea un boton para salir del programa
        self.exit_button = tk.Button(self.button_frame, text="Salir", command=self.exit_app, bg="#FF6969", font=("Arial", 14, 'bold'))
        self.exit_button.grid(row=0, column=2, padx=30, pady=10)

        #Crea un widget TreeView para mostrar los resultados de análisis
        self.treeview = ttk.Treeview(self.windows, columns=("Token", "Lexema", "Línea"), show="headings")
        self.treeview.heading("Token", text="Token")
        self.treeview.heading("Lexema", text="Lexema")
        self.treeview.heading("Línea", text="Línea")
        self.treeview.pack()

        # Configura la alineación de las columnas para centrar el contenido
        self.treeview.column("Token", anchor="center")
        self.treeview.column("Lexema", anchor="center")
        self.treeview.column("Línea", anchor="center")

        self.count_tree = ttk.Treeview(self.windows, columns=("Elemento", "Cantidad"), show="headings")
        self.count_tree.heading("Elemento", text="Elemento")
        self.count_tree.heading("Cantidad", text="Cantidad")
        self.count_tree.pack(pady=10)

        self.count_tree.column("Elemento", anchor="center")
        self.count_tree.column("Cantidad", anchor="center")

    #Define un metodo para realizar el analisis lexico del texto de entrada y mostrar los resultados
    def analyze_text(self):  
        lexer = Lexer()  #Crea una instancia de la clase Lexer 
        text = self.text_input.get("1.0", "end").strip() # Obtiene el texto ingresado y elimina espacios en blanco
        if not text:  # Verifica si el texto está vacío
            return  # Si el texto está vacío, no realiza el análisis ni muestra los resultados
        
        result = lexer.tokenize(text)
        
        # Limpia las entradas existentes en el Treeview
        self.treeview.delete(*self.treeview.get_children())
        
        num_reserved_words = 0
        num_operators = 0
        num_delimiters = 0
        num_numbers = 0
        num_identifiers = 0
        num_lexical_errors = 0
        num_open_parentheses = 0
        num_close_parentheses = 0
        num_open_braces = 0
        num_close_braces = 0
        num_semicolons = 0
    
        for line_number, token_type, token_value in result:
            self.treeview.insert("", "end", values=(token_type, token_value, line_number))

            if token_type == 'RESERVADA':
                num_reserved_words += 1
            elif token_type == 'OPERADOR':
                num_operators += 1
            elif token_type == 'DELIMITADOR':
                num_delimiters += 1
                if token_value == '(':
                    num_open_parentheses += 1
                elif token_value == ')':
                    num_close_parentheses += 1
                elif token_value == '{':
                    num_open_braces += 1
                elif token_value == '}':
                    num_close_braces += 1
                elif token_value == ';':
                    num_semicolons += 1
            elif token_type == 'NÚMERO':
                num_numbers += 1
            elif token_type == 'IDENTIFICADOR':
                num_identifiers += 1
            elif token_type == 'ERROR LÉXICO':
                num_lexical_errors += 1

        # Inserta las cuantificaciones en el Treeview de conteo
        self.count_tree.delete(*self.count_tree.get_children())  # Limpia el contenido existente

        # Inserta las cuantificaciones en la tabla
        quantities = [
            ("Palabras Reservadas", num_reserved_words),
            ("Operadores", num_operators),
            ("Delimitadores", num_delimiters),
            ("Números", num_numbers),
            ("Errores Léxicos", num_lexical_errors),
            ("Identificadores", num_identifiers),
            ("Paréntesis de Apertura", num_open_parentheses),
            ("Paréntesis de Cierre", num_close_parentheses),
            ("Llaves de Apertura", num_open_braces),
            ("Llaves de Cierre", num_close_braces),
            ("Punto y Coma", num_semicolons)
        ]

        for element, quantity in quantities:
             self.count_tree.insert("", "end", values=(element, quantity))

    #Define un metodo para limpiar el cuadro de texto y la etiqueta de resultados
    def clean_text(self):
        self.text_input.delete("1.0", "end") #Borra el contenido del cuadro del texto
        self.treeview.delete(*self.treeview.get_children()) #Limpia el contenido del ttk
        self.count_tree.delete(*self.count_tree.get_children())  # Limpia el contenido del Treeview de conteo

    def exit_app(self): #Define un metodo para salir del programa
        self.windows.destroy()

    def run(self): #Define un metodo para ejecutar la aplicacion de la interfaz grafica
        self.windows.mainloop() #inicia el bucle de la interfaz grafica

app = LexerApp() #Crea una instancia de la clase Lexer app
app.run()   #Ejecuta la aplicacion de la interfaz grafica llamando al metodo "Run"