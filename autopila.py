import tkinter as tk

class AutomataDePila:
    def __init__(self):
        self.current_state = 'q0'
        self.stack = ['Z']  # Pila con símbolo inicial Z
        self.transitions = {
            # Transiciones y operaciones de pila
            ('q0', 'VR', 'Z'): ('q1', 'Z'),
            ('q1', 'T', 'Z'): ('q2', 'Z'),
            ('q2', 'L', 'Z'): ('q3', 'Z'),
            ('q3', 'I', 'Z'): ('q4', 'Z'),
            ('q4', 'N', 'Z'): ('q5', 'Z'), ('q4', 'VB', 'Z'): ('q5', 'Z'), ('q4', 'L', 'Z'): ('q5', 'Z'),
            ('q5', 'PC', 'Z'): ('qf', 'Z'), ('q5', 'N', 'Z'): ('q6', 'Z'),
            ('q6', 'P', 'Z'): ('q7', 'Z'),
            ('q7', 'N', 'Z'): ('q5', 'Z')
        }

    def transition(self, symbol):
    # Ajustar el símbolo para que coincida con la gramática
        top_stack = self.stack[-1]
        if symbol == 'var':
            symbol = 'VR'
        elif symbol in ['ent', 'flot', 'booleano', 'cadena']:
            symbol = 'T'
        elif symbol.isalpha() and self.current_state in ['q2', 'q4', 'q5', 'q6', 'q7']:
            symbol = 'L'
        elif symbol.isdigit() and self.current_state in ['q4', 'q5', 'q7']:
            symbol = 'N'
        elif symbol == '=':
            symbol = 'I'
        elif symbol == ';':
            symbol = 'PC'
        elif symbol == '.' and self.current_state == 'q6':
            symbol = 'P'

    # Actualizar el estado actual y manejar la pila
        if (self.current_state, symbol, top_stack) in self.transitions:
            self.current_state, new_stack_symbol = self.transitions[(self.current_state, symbol, top_stack)]
            if new_stack_symbol != top_stack:
                self.stack.pop()
                if new_stack_symbol != '':
                    self.stack.append(new_stack_symbol)

    def reset(self):
        self.current_state = 'q0'
        self.stack = ['Z']  # Restablecer la pila al estado inicial


    def process(self, tokens):
        self.reset()  # Restablecer el autómata antes de procesar una nueva cadena
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
