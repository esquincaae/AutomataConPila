import tkinter as tk

class AutomataDePila:
    def __init__(self):
        self.current_state = 'q0'
        self.stack = ['Z']  # Pila con símbolo inicial Z
        self.transitions = {
            # Transiciones actualizadas con categorías
            ('q0', 'VR', 'Z'): ('q1', 'Z'),
            ('q1', 'T', 'Z'): ('q2', 'Z'),
            ('q2', 'LETTER', 'Z'): ('q3', 'Z'),
            ('q3', 'I', 'Z'): ('q4', 'Z'),
            ('q4', 'DIGIT', 'Z'): ('q5', 'Z'), 
            ('q4', 'FLOAT', 'Z'): ('q5', 'Z'),
            ('q4', 'VB', 'Z'): ('q5', 'Z'),
            ('q5', 'PC', 'Z'): ('qf', 'Z'),
            # Añadir más transiciones según sea necesario
        }

    def transition(self, symbol):
        top_stack = self.stack[-1]

        def process_symbol(sym):
            if (self.current_state, sym, top_stack) in self.transitions:
                self.current_state, new_stack_symbol = self.transitions[(self.current_state, sym, top_stack)]
                if new_stack_symbol != top_stack:
                    self.stack.pop()
                    if new_stack_symbol != '':
                        self.stack.append(new_stack_symbol)

        # Clasificación de símbolos
        if symbol == 'var':
            process_symbol('VR')
        elif symbol in ['ent', 'flot', 'booleano', 'cadena']:
            process_symbol('T')
        elif symbol.isalpha() and symbol not in ['false', 'true']:
            process_symbol('LETTER')
        elif symbol in ['false', 'true']:
            process_symbol('VB')
        elif symbol == '=':
            process_symbol('I')
        elif symbol.isdigit():
            process_symbol('DIGIT')
        elif self.is_float(symbol):
            process_symbol('FLOAT')
        elif symbol == ';':
            process_symbol('PC')
        # Añadir más lógica según sea necesario

    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def reset(self):
        self.current_state = 'q0'
        self.stack = ['Z']

    def process(self, tokens):
        self.reset()
        for token in tokens:
            if token.strip():  # Ignorar espacios en blanco
                self.transition(token.strip())
            if self.current_state == 'qf':
                return True
        return False

def submit():
    tokens = entry.get().split(" ")
    result = automata.process(tokens)
    result_label.config(text="Cadena aceptada" if result else "Cadena rechazada")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Autómata de Pila para Gramática de Declaración de Variables")

automata = AutomataDePila()

entry_label = tk.Label(root, text="Ingrese la declaración de variable:")
entry_label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

submit_button = tk.Button(root, text="Procesar", command=submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
