import tkinter as tk
from tkinter import messagebox

class Automata:
    def __init__(self):
        
        self.transitions = {
            # Transiciones para variables
            ('SV1', 'VR'): ('SV2', 'T'),
            ('SV2', 'T'): ('SV3', 'L'),
            ('SV3', 'L'): ('SV4', 'I'),
            ('SV4', 'I'): ('SV5', 'N'),
            ('SV4', 'I'): ('SV5','VB'),
            ('SV4', 'I'): ('SV5','L'),
            ('SV5', 'N'): ('SV6','P'),
            ('SV5', 'N'): ('SV6', 'PC'),
            ('SV5', 'VB'): ('SV6', 'PC'),
            ('SV5', 'L'): ('SV6', 'PC'),
            ('SV6', 'P'): ('SV7', 'N'),
            ('SV7', 'N'): ('SV8', 'PC'),
            ('SV6', 'PC'): ('SVF', 'O'), #cierre
            ('SV8', 'PC'): ('SVF', 'O'),  #cierre
            # Transiciones para funciones
            ('SF1', 'FN'): ('SF2', 'L'),
            ('SF2', 'L'): ('SF3', 'X1'),
            ('SF3', 'X1'): ('SF4', 'X2'),
            ('SF4', 'X2'): ('SF5', 'X3'),
            ('SF5', 'X3'): ('SF6', 'X5'),
            ('SF6', 'X5'): ('SF7', 'X4'),
            ('SF7', 'X4'): ('SFF', 'O'),  # cierre
            # Transiciones para condicional
            ('SC1', 'IF'): ('SC2', 'X1'), #1
            ('SC2', 'X1'): ('SC3', 'N'), #2
            ('SC3', 'N'): ('SC4', 'CN'), #3
            ('SC4', 'CN'): ('SC5', 'N'), #4
            ('SC5', 'N'): ('SC6', 'X2'), #5
            ('SC6', 'X2'): ('SC7', 'X3'), #6
            ('SC7', 'X3'): ('SC8', 'X5'), 

            ('SC8', 'X5'): ('SC9', 'X4'), 
            ('SC9', 'X4'): ('SC10', 'EL'), # Entrar en el bloque del 'sino'
            ('SC10', 'EL'): ('SC11', 'X3'),  
            ('SC11', 'X3'): ('SF6', 'O'),  # Cierre del bloque 'sino' 
            ('SC7', 'X4'): ('SF6', 'O'), #cierre del bloque 'si'
            # Transiciones para ciclo
            ('SCI1', 'CY'): ('SCI2', 'X1'),
            ('SCI2', 'X1'): ('SCI3', 'VR'),
            ('SCI3', 'VR'): ('SCI4', 'T'),
            ('SCI4', 'T'): ('SCI5', 'L'),
            ('SCI5', 'L'): ('SCI6', 'I'),
            ('SCI6', 'I'): ('SCI7', 'N'),
            ('SCI7', 'N'): ('SCI8', 'PC'),
            ('SCI8', 'PC'): ('SCI9', 'L'),
            ('SCI9', 'L'): ('SCI10', 'CN'),
            ('SCI10', 'CN'): ('SCI11', 'N'),
            ('SCI11', 'N'): ('SCI12', 'PC'),
            ('SCI12', 'PC'): ('SCI13', 'L'),
            ('SCI13', 'L'): ('SCI14', 'AD'),
            ('SCI14', 'AD'): ('SCI15', 'X2'),
            ('SCI15', 'X2'): ('SCI16', 'X3'),
            ('SCI16', 'X3'): ('SF6', 'X5'),  # continua en SF6
        }

        self.stack = []

    def next_state(self):
        text_area.delete('1.0', tk.END) 
        # Obtiene el input_type de la cima de la pila
        if not self.stack:
            raise ValueError("La pila está vacía")
        else:
            dato = self.stack[-1]
            if dato == 'VR':
                self.current_state = 'SV1'
            elif dato == 'FN':
                self.current_state = 'SF1'
            elif dato == 'IF':
                self.current_state = 'SC1'
            elif dato == 'CY':
                self.current_state = 'SCI1'
            else:
                raise ValueError("Cima de la pila invalida")
        while self.stack:
            print(f'estado actural: [{self.current_state}] Lyra: {self.stack}')
            text_area.insert(tk.END, f"Lyra: {self.stack}\n")
            input_type = self.stack.pop()
            bpop = self.current_state 
            transition_key = (self.current_state, input_type)
            transition = self.transitions.get(transition_key)
            if transition is None:
                messagebox.showerror("ERROR",f"Transición no encontrada para: {transition_key}")
            next_state, action = transition
            self.current_state = next_state
            bpop1 = self.current_state
        if bpop1 == 'SC10' or bpop1 == 'SFF' or bpop1 == 'SVF':
            print(f'estado actual: [{self.current_state}] Lyra: {self.stack}')
            text_area.insert(tk.END, f"Lyra: {self.stack}\n")
            messagebox.showinfo('Lyra', 'Cadena Valida')
        else:
            messagebox.showerror("ERROR",f"No se puede terminar en: {bpop}")

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
                messagebox.showerror("ERROR",f"Simbolo no encontrado para: {palabra}")
                exit(0)

        if 'DESCONOCIDO' in self.stack:
            messagebox.showerror("ERROR",f"Símbolo desconocido en la entrada: {entrada}")

        return ' '.join(self.stack)

# Funciones para la interfaz gráfica
def procesar():
      
    entrada = entry.get()
    try:
        automata.procesar_entrada(entrada)
        text_area.delete('1.0', tk.END) 
    except ValueError as e:
        messagebox.showerror("Error", e)
    automata.next_state()
    

# Crea y configura widgets
root = tk.Tk()
root.title("Lyra: Automata de pila")

# Crear un Entry
entry = tk.Entry(root, width=100)
entry.pack(padx=10, pady=10)

# Crear un botón que llame a la función 'procesar'
boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

# Crear un área de texto para la salida
text_area = tk.Text(root, height=15, width=150)
text_area.pack(padx=10, pady=10)

automata = Automata()

root.mainloop()