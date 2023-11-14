import tkinter as tk
from subprocess import call
import pyperclip  # Necesitas instalarlo con pip install pyperclip

codigo = '''
    int contador = 1;
    while (contador <= 5) {
        System.out.println(contador);
        contador++;
    }
'''

class MenuPrincipalApp:
    def __init__(self, root):
        # Configuración del frame principal
        self.root = root
        root.title("Analizador Léxico y Sintáctico - while de Java")
        root.geometry("410x350")
        root.configure(bg="#F5E8C7")

        # Label "Analizador lexico y sintactico"
        label_Titulo = tk.Label(root, text="ANALIZADOR LÉXICO Y SINTÁCTICO", height=2, width=300, bg="#363062", font=("Arial", 14, 'bold'), fg="#FFF3DA")
        label_Titulo.pack()

        # Label "compiladores"
        label_Compiladores = tk.Label(root, text="Compiladores", bg="#F5E8C7", font=("Arial", 12, 'bold'))
        label_Compiladores.pack(pady=5)

        # Cuadro de texto
        self.texto = tk.Text(root, height=5, width=40, bg="white", font=("Arial", 12))
        self.texto.insert("1.0", "int contador = 1; \nwhile (contador <= 5) {\n  System.out.println(contador);\n  contador++;\n}")
        self.texto.pack(pady=5)

        boton_copiar = tk.Button(root, text="Copiar Texto", command=self.copiar_al_portapapeles, font=("Arial", 16, 'bold'), bg="#61A3BA")
        boton_copiar.pack(pady=10)
        
        # Botones
        frame_botones = tk.Frame(root, bg="#F5E8C7")
        frame_botones.pack()

        boton_lexico = tk.Button(frame_botones, text="Léxico", command=self.lexico, font=("Arial", 16, 'bold'), bg="#818FB4")
        boton_lexico.grid(row=0, column=0, padx=10)

        boton_sintactico = tk.Button(frame_botones, text="Sintáctico", command=self.sintactico, font=("Arial", 16, 'bold'), bg="#818FB4")
        boton_sintactico.grid(row=0, column=1, padx=10)

        boton_salir = tk.Button(frame_botones, text="Salir", command=root.destroy, font=("Arial", 16, 'bold'), bg="#FA7070")
        boton_salir.grid(row=0, column=2, padx=10)

        # Label de datos
        label3 = tk.Label(root, text="Código realizado por Marco Zúniga 6M - LIDTS", bg="#F5E8C7", font=("Arial", 10, 'bold'))
        label3.pack(pady=10)

    def copiar_al_portapapeles(self):
        contenido = self.texto.get("1.0", "end-1c")  # Obtener el contenido del cuadro de texto
        pyperclip.copy(contenido)  # Copiar al portapapeles

    def lexico(self):
        root.destroy()
        call(["python", "lexico.py"])

    def sintactico(self):
        root.destroy()
        call(["python", "sintactico.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipalApp(root)
    root.mainloop()
