import tkinter as tk
from tkinter import messagebox

class AutomataDePila:
    def __init__(self, tipo_entrada):
        self.tipo_entrada = tipo_entrada if tipo_entrada else 'variable'
        self.current_state = 'SV1' if self.tipo_entrada == 'variable' else 'SF1' 
        self.stack = []
        self.transitions = {
            # Transiciones para variables
            ('SV1', 'VR', 'A'): ('SV2', 'B'),
            ('SV2', 'T', 'B'): ('SV3', 'C'),
            ('SV3', 'LETTER', 'C'): ('SV4', 'D'),
            ('SV4', 'I', 'D'): ('SV5', 'E'),
            ('SV5', 'DIGIT', 'E'): ('SV6', 'F'),
            ('SV6', 'PC', 'F'): ('SVF', 'G'),
            ('SV6', 'P', 'F '): ('SV7', 'H'),
            ('SV7', 'DIGIT', 'H'): ('SV8', 'I'),
            ('SV8', 'PC', 'I'): ('SVF', 'J'),
            # Transiciones para funciones
            ('SF1', 'FN', 'A1'):('SF2', 'B1'),
            ('SF2', 'LETTER', 'B1'):('SF3', 'C1'),
            ('SF3', 'X1', 'C1'):('SF4', 'D1'),
            ('SF4', 'X2', 'D1'):('SF5', 'E1'),
            ('SF5', 'X3', 'E1'):('SF6', 'F1'),
            ('SF6', 'X5', 'F1'):('SF7', 'G1'),
            ('SF7', 'X4', 'G1'):('SFF', 'H1'),
            # Transiciones para condicional
            ('SC1', 'IF', 'A2'):('SC2', 'B2'),
            ('SC2', 'X1', 'B2'):('SC3', 'C2'),
            ('SC3', 'DIGIT', 'C2'):('SC4', 'D2'),
            ('SC4', 'CN', 'D2'):('SC5', 'E2'),
            ('SC5', 'DIGIT', 'E2'):('SC6', 'F2'),
            ('SC6', 'X2', 'F2'):('SC7', 'G2'),
            ('SC7', 'X3', 'G2'):('SC8', 'H2') or ('SF6', 'I2'),
            ('SC8', 'X5', 'H2'):('SC9', 'I2'),
            ('SC9', 'X4', 'I2'):('SC10', 'J2'),
            ('SC10', 'EL', 'J2'):('SC11', 'K2'),
            ('SC11', 'X3', 'K2'):('SCF', 'L2'),
            #Transiciones para ciclo
            ('SCI1', 'CY', 'A3'): ('SCI2', 'B3'),
            ('SCI2', 'X1', 'B3'): ('SCI3', 'C3'),
            ('SCI3', 'VR', 'C3'): ('SCI4', 'D3'),
            ('SCI4', 'T', 'D3'): ('SCI5', 'E3'),
            ('SCI4', 'L', 'E3'): ('SCI6', 'F3'),
            ('SCI6', 'I', 'F3'): ('SCI7', 'G3'),
            ('SCI7', 'N', 'G3'): ('SCI8', 'H3'),
            ('SCI8', 'PC', 'H3'): ('SCI9', 'I3'),
            ('SCI9', 'L', 'I3'): ('SCI10', 'J3'),
            ('SCI10', 'CN', 'J3'): ('SCI11', 'K3'),
            ('SCI11', 'N', 'K3'): ('SCI12', 'L3'),
            ('SCI12', 'PC', 'L3'): ('SCI13', 'O3'),
            ('SCI13', 'L', 'O3'): ('SCI14', 'P3'),
            ('SCI14', 'AD', 'P3'): ('SCI15', 'Q3'),
            ('SCI15', 'X2', 'Q3'): ('SCI16', 'R3'),
            ('SCI16', 'X2', 'R3'): ('SCI17', 'S3'),
            ('SCI17', 'X3', 'S3'): ('SF6', 'O3')
        }

    def transition(self, symbol, stack_label):
        top_stack = self.stack[-1] if self.stack else None
        #print(f"Estado actual: {self.current_state}, Símbolo: {symbol}, Cima de la pila: {top_stack}")
        
        def process_symbol(sym):
            if (self.current_state, sym, top_stack) in self.transitions:
                self.current_state, new_stack_symbol = self.transitions[(self.current_state, sym, top_stack)]
                self.stack.pop()
                if new_stack_symbol != '':
                    self.stack.append(new_stack_symbol)
            stack_label.config(text="Pila: " + str(self.stack))
            #print(f"Nuevo estado: {self.current_state}, Lyra: {self.stack}")
        
        # Clasificación de símbolos
        if symbol == 'var':
            process_symbol('VR')
        elif symbol in ['ent', 'flot', 'booleano', 'cadena']:
            process_symbol('T')
        elif symbol.isalpha() and symbol not in ['false', 'true']:
            process_symbol('LETTER')
        elif symbol == '=':
            process_symbol('I')
        elif symbol.isdigit():
            process_symbol('DIGIT')
        elif symbol == ';':
            process_symbol('PC')
        elif symbol == '.':
            process_symbol('P')
        elif symbol == 'funcion':
            process_symbol('FN')
        elif symbol == '(':
            process_symbol('X1')
        elif symbol == ')':
            process_symbol('X2')
        elif symbol == '{':
            process_symbol('X3')
        elif symbol == 'contenido':
            process_symbol('X5')    
        elif symbol == '}':
            process_symbol('X4')
        elif symbol == 'si':
            process_symbol('IF')
        elif symbol == 'sino':
            process_symbol('EL')
        elif symbol == 'para':
            process_symbol('CY')
        elif symbol in ["<", ">", "<=", ">=", "==", "!="]:
            process_symbol('CN')
        elif symbol in ['++', '--']:
            process_symbol('AD')
        else:
            pass
        # Asegúrate de que la clasificación de símbolos esté completa

    #def is_float(self, string):
     #   try:
      #      float(string)
       #     return True
        #except ValueError:
         #   return False

    def process(self, stack_label):
        while self.stack:
            symbol = self.stack.pop()
            print(f"Lyra{self.stack}")  # Imprimir el estado actual de la pila
            self.transition(symbol, stack_label)
            if self.current_state in ['SVF', 'SFF', 'SCF']:
                return True
        return False

def submit():
    cadena = text_area.get("1.0", "end-1c")
    tokens = cadena.split(" ")
    automata.stack.extend(reversed(tokens))  # Agrega los tokens a la pila en orden inverso
    #print(f"Lyra{automata.stack}")

    result = automata.process(stack_label)
    result_label.config(text="Cadena aceptada" if result else "Cadena rechazada")
    stack_label.config(text="Pila final: " + str(automata.stack))

root = tk.Tk()
root.title("Lyra: Autómata de Pila")

automata = AutomataDePila(tipo_entrada='')

entry_label = tk.Label(root, text="Ingrese la cadena a validar:")
entry_label.pack()

text_area = tk.Text(root, height=30, width=90)
text_area.pack()

submit_button = tk.Button(root, text="Procesar", command=submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

stack_label = tk.Label(root, text="Pila: " + str(automata.stack))
stack_label.pack()

root.mainloop()