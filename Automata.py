import tkinter as tk

class PDA:
    def __init__(self):
        self.states = set(["q0", "q1", "q2", "q3", "q4", "q5", "q6"])
        self.input_alphabet = set(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "false", "true", "=", ";", ".", "var", "ent", "flot", "booleano", "cadena"])
        self.stack_alphabet = set(["Z", "T", "N", "L", "I", "PC", "VB", "VR"])
        self.transitions = {
            ("q0", "var", "Z"): ("q1", "Z"),
            ("q1", "ent", "Z"): ("q2", "T"),
            ("q1", "flot", "Z"): ("q2", "T"),
            ("q1", "booleano", "Z"): ("q2", "T"),
            ("q1", "cadena", "Z"): ("q2", "T"),
            ("q2", "a", "T"): ("q3", "T"),
            ("q2", "b", "T"): ("q3", "T"),
            # Más transiciones para cada letra del alfabeto y números
            ("q3", "=", "T"): ("q4", "I"),
            ("q4", "a", "I"): ("q5", "I"),
            # Más transiciones para asignar valores
            ("q5", ";", "I"): ("q6", "PC"),
            ("q6", "var", "PC"): ("q1", "Z"),
        }
        self.start_state = "q0"
        self.stack = ["Z"]
        self.accept_states = set(["q6"])

    def process_input(self, input_string):
        current_state = self.start_state
        input_string += " "
        stack_index = 0

        for symbol in input_string:
            current_symbol = self.stack[stack_index]

            if (current_state, symbol, current_symbol) in self.transitions:
                new_state, new_stack_symbol = self.transitions[(current_state, symbol, current_symbol)]

                if current_symbol != "Z":
                    self.stack[stack_index] = new_stack_symbol
                elif new_stack_symbol != "Z":
                    self.stack.insert(stack_index, new_stack_symbol)

                current_state = new_state

                if symbol == " ":
                    stack_index -= 1
                else:
                    stack_index += 1
            else:
                return False

        return current_state in self.accept_states

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Autómata con Pila")

        self.label = tk.Label(root, text="Ingrese una declaración de variable:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.check_button = tk.Button(root, text="Verificar", command=self.check_input)
        self.check_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def check_input(self):
        input_string = self.entry.get()
        pda = PDA()
        result = pda.process_input(input_string)
        if result:
            self.result_label.config(text="La declaración de variables es válida.")
        else:
            self.result_label.config(text="La declaración de variables no es válida.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()