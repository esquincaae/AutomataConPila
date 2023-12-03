import tkinter as tk
from tkinter import messagebox

class Automata:
    def __init__(self):
        self.transitions = {
    # Transiciones para variables
    ('SV1', 'VR'): ('SV2', 'A'),
    ('SV2', 'T'): ('SV3', 'A'),
    ('SV3', 'L'): ('SV4', 'A'),
    ('SV4', 'I'): ('SV5', 'A'),
    ('SV5', 'N'): ('SV6', 'A'),
    ('SV5', 'VB'): ('SV6', 'A'),
    ('SV5', 'L'): ('SV6', 'A'),
    ('SV6', 'P'): ('SV7', 'A'),
    ('SV7', 'N'): ('SV8', 'A'),
    ('SV6', 'PC'): ('SVF', 'A'),
    ('SV8', 'PC'): ('SVF', 'A'),  # cierre
    ('SV8', 'PC'): ('SV1', 'A'),  # agregar otra variable
    ('SV8', 'PC'): ('SF1', 'B'),  # agregar funcion
    ('SV8', 'PC'): ('SC1', 'A'),  # agregar condicional
    ('SV8', 'PC'): ('SCI1', 'A'),  # agregar ciclo
    # Transiciones para funciones
    ('SF1', 'FN'): ('SF2', 'A'),
    ('SF2', 'L'): ('SF3', 'A'),
    ('SF3', 'X1'): ('SF4', 'A'),
    ('SF4', 'X2'): ('SF5', 'A'),
    ('SF5', 'X3'): ('SF6', 'A'),
    ('SF6', 'X5'): ('SF7', 'A'),
    ('SF7', 'X4'): ('SFF', 'A'),  # cierre
    ('SF7', 'X4'): ('SF1', 'A'),  # agregar otra funcion
    ('SF7', 'X4'): ('SV1', 'A'),  # agregar variable
    ('SF7', 'X4'): ('SC1', 'A'),  # agregar condicional
    ('SF7', 'X4'): ('SCI1', 'A'),  # agregar ciclo
    # Transiciones para condicional
    ('SC1', 'IF'): ('SC2', 'A'),
    ('SC2', 'X1'): ('SC3', 'A'),
    ('SC3', 'N'): ('SC4', 'A'),
    ('SC4', 'CN'): ('SC5', 'A'),
    ('SC5', 'N'): ('SC6', 'A'),
    ('SC6', 'X2'): ('SC7', 'A'),
    ('SC7', 'X3'): ('SF6', 'A'),  # camino para cerrar el si
    ('SC7', 'X3'): ('SC8', 'A'),  # camino para cerrar el si y abrir el sino
    ('SC8', 'X5'): ('SC9', 'A'),
    ('SC9', 'X4'): ('SC10', 'A'),
    ('SC10', 'EL'): ('SC11', 'A'),
    ('SC11', 'X3'): ('SF6', 'A'),  # continua en SF6
    # Transiciones para ciclo
    ('SCI1', 'CY'): ('SCI2', 'A'),
    ('SCI2', 'X1'): ('SCI3', 'A'),
    ('SCI3', 'VR'): ('SCI4', 'A'),
    ('SCI4', 'T'): ('SCI5', 'A'),
    ('SCI4', 'L'): ('SCI6', 'A'),
    ('SCI6', 'I'): ('SCI7', 'A'),
    ('SCI7', 'N'): ('SCI8', 'A'),
    ('SCI8', 'PC'): ('SCI9', 'A'),
    ('SCI9', 'L'): ('SCI10', 'A'),
    ('SCI10', 'CN'): ('SCI11', 'A'),
    ('SCI11', 'N'): ('SCI12', 'A'),
    ('SCI12', 'PC'): ('SCI13', 'A'),
    ('SCI13', 'L'): ('SCI14', 'A'),
    ('SCI14', 'AD'): ('SCI15', 'A'),
    ('SCI15', 'X2'): ('SCI16', 'A'),
    ('SCI16', 'X3'): ('SF6', 'A'),  # continua en SF6
}

        self.stack = []
        self.stack_symbol = 'A'
        self.current_state = 'SV1'

    def next_state(self):
        # Verifica si hay elementos en la pila
        sym = self.stack_symbol
        if not self.stack:
            raise ValueError("La pila está vacía")
        else:
            dato = self.stack[-1]
            if dato == 'VR':
                self.current_state = 'SV1'
            else:
                raise ValueError("Cima de la pila invalida")
        # Obtiene el input_type de la cima de la pila
        while self.stack:
            print(f'Lyra: {self.stack}')
            input_type = self.stack.pop()
            # Clave de transición usando el estado actual y el input_type de la pila
            transition_key = (self.current_state, input_type, sym)
            transition = self.transitions.get(transition_key)
            if transition is None:
                raise ValueError(f"Transición no encontrada para: {transition_key}")
            next_state, action = transition
            self.current_state = next_state
            if 
        print(f'Lyra: {self.stack}')
        return next_state, action

    def procesar_entrada(self, entrada):
        # Definir los tipos de tokens
        tokens = {
            'VR': ["var"],
            'T': ["ent", "flot", "booleano", "cadena"],
            'IF': ["si"],
            'EL': ["sino"],
            'CY': ["para"],
            'FN': ["funcion"],
            'X5': ["contenido"],
            'VB': ["false", "true"],
            'L': list("abcdefghijklmnñopqrstuvwxyz"),
            'N': list("0123456789"),
            'I': ["="],
            'PC': [";"],
            'P': ["."],
            'CN': ["<", ">", "<=", ">=", "==", "!="],
            'AD': ["++", "--"],
            'X1': ["("],
            'X2': [")"],
            'X3': ["{"],
            'X4': ["}"],
        }

        palabras = entrada.split()
        palabras.reverse()  # Invierte el orden de las palabras

        for palabra in palabras:
            simbolo_encontrado = False
            for tipo, valores in tokens.items():
                if palabra in valores or (tipo == 'L' and palabra.isalpha()) or (tipo == 'N' and palabra.isdigit()):
                    self.stack.append(tipo)  # Guarda el tipo en la pila
                    simbolo_encontrado = True
                    break
            if not simbolo_encontrado:
                self.stack.append('DESCONOCIDO')

        if 'DESCONOCIDO' in self.stack:
            raise ValueError(f"Símbolo desconocido en la entrada: {entrada}")

        return ' '.join(self.stack)

# Funciones para la interfaz gráfica
def procesar():
    entrada = text_area.get("1.0", tk.END).strip()
    try:
        simbolos_procesados = automata.procesar_entrada(entrada)
        resultado.set(f"Símbolos procesados: {simbolos_procesados}")
    except ValueError as e:
        messagebox.showerror("Error", e)
    automata.next_state()    

# Configuración de la ventana Tkinter
ventana = tk.Tk()
ventana.title("Autómata de Pila")

# Crea y configura widgets
text_area = tk.Text(ventana, height=10, width=50)
text_area.pack()

boton_procesar = tk.Button(ventana, text="Procesar", command=procesar)
boton_procesar.pack()

resultado = tk.StringVar()
etiqueta_resultado = tk.Label(ventana, textvariable=resultado)
etiqueta_resultado.pack()

# Crea una instancia del autómata
automata = Automata()

# Ejecuta el bucle principal de la GUI
ventana.mainloop()