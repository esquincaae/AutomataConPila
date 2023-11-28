import tkinter as tk

class PDA:
    def __init__(self):
        self.stack = []
        self.current_index = 0
        self.transitions = {
            ("q0", "var", "Z"): ("q1", "Z"),
            ("q1", "ent", "Z"): ("q2", "T"),
            ("q1", "flot", "Z"): ("q2", "T"),
            ("q1", "booleano", "Z"): ("q2", "T"),
            ("q1", "cadena", "Z"): ("q2", "T"),
            ("q2", "a", "T"): ("q3", "T"),
            ("q2", "b", "T"): ("q3", "T"),
            ("q2", "c", "T"): ("q3", "T"),
            ("q2", "d", "T"): ("q3", "T"),
            ("q2", "e", "T"): ("q3", "T"),
            ("q2", "f", "T"): ("q3", "T"),
            ("q2", "g", "T"): ("q3", "T"),
            ("q2", "h", "T"): ("q3", "T"),
            ("q2", "i", "T"): ("q3", "T"),
            ("q2", "j", "T"): ("q3", "T"),
            ("q2", "k", "T"): ("q3", "T"),
            ("q2", "l", "T"): ("q3", "T"),
            ("q2", "m", "T"): ("q3", "T"),
            ("q2", "n", "T"): ("q3", "T"),
            ("q2", "ñ", "T"): ("q3", "T"),
            ("q2", "o", "T"): ("q3", "T"),
            ("q2", "p", "T"): ("q3", "T"),
            ("q2", "q", "T"): ("q3", "T"),
            ("q2", "r", "T"): ("q3", "T"),
            ("q2", "s", "T"): ("q3", "T"),
            ("q2", "t", "T"): ("q3", "T"),
            ("q2", "u", "T"): ("q3", "T"),
            ("q2", "v", "T"): ("q3", "T"),
            ("q2", "x", "T"): ("q3", "T"),
            ("q2", "y", "T"): ("q3", "T"),
            ("q2", "z", "T"): ("q3", "T"),
            ("q3", "=", "T"): ("q4", "I"),
            ("q4", "0", "I"): ("q5", "I"),
            ("q4", "1", "I"): ("q5", "I"),
            ("q4", "2", "I"): ("q5", "I"),
            ("q4", "3", "I"): ("q5", "I"),
            ("q4", "4", "I"): ("q5", "I"),
            ("q4", "5", "I"): ("q5", "I"),
            ("q4", "6", "I"): ("q5", "I"),
            ("q4", "7", "I"): ("q5", "I"),
            ("q4", "8", "I"): ("q5", "I"),
            ("q4", "9", "I"): ("q5", "I"),
            ("q5", ";", "I"): ("q6", "PC"),
            ("q6", "var", "PC"): ("q1", "Z"),
            ("q5", ".", "I"): ("q6", "PC"),
        }
        self.start_state = "q0"
        self.current_state = self.start_state

    # Modificación en el método process_input

    def process_input(self, input_string):
        self.current_state = self.start_state
        stack_index = 0
        self.current_index = 0  # Reinicia current_index al inicio de la cadena

        # Eliminar espacios en blanco de la cadena de entrada
        input_string = input_string.replace(" ", "")

        for symbol in input_string:
            if stack_index < len(self.stack):
                current_symbol = self.stack[stack_index]
            else:
                current_symbol = "Z"  # Si la pila está vacía, asumimos un símbolo Z

            if (self.current_state, symbol, current_symbol) in self.transitions:
                new_state, new_stack_symbol = self.transitions[(self.current_state, symbol, current_symbol)]

                if current_symbol != "Z":
                    self.stack[stack_index] = new_stack_symbol
                elif new_stack_symbol != "Z":
                    self.stack.insert(stack_index, new_stack_symbol)

                self.current_state = new_state

                if symbol == " ":
                    stack_index -= 1
                else:
                    stack_index += 1
                self.current_index += 1  # Incrementa current_index después de procesar cada símbolo
            else:
                error_message = f"Error en la posición {self.current_index}: No se pudo encontrar una transición válida."
                print(error_message)  # Muestra el mensaje de error en la consola
                return False

        if self.current_state == "q6" or not self.stack:
            return True
        else:
            error_message = f"Error en la posición {self.current_index}: No se completó el procesamiento del autómata."
            print(error_message)  # Muestra el mensaje de error en la consola
            return False


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyra: Automata con pila")
        self.root.geometry("500x300")  # Tamaño de la ventana (ancho x alto)

        self.label = tk.Label(root, text="Ingrese un fragmento de código del lenguaje Lyra:")
        self.label.pack()

        self.text_area = tk.Text(root, wrap=tk.WORD, height=10)  # Altura del TextArea reducida
        self.text_area.pack(fill=tk.BOTH, expand=True)  # Relleno en ambas direcciones

        self.validate_button = tk.Button(root, text="Validar Código", command=self.validate_code)
        self.validate_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def validate_code(self):
        input_string = self.text_area.get("1.0", tk.END)  # Obtén todo el contenido del cuadro de texto
        pda = PDA()
        result = pda.process_input(input_string)
        
        if result:
            self.result_label.config(text="El fragmento de código es válido.")
        else:
            # Obtener el último símbolo procesado para mostrar en el mensaje de error
            last_symbol = input_string[pda.current_index - 1]
            error_message = f"Error en el símbolo: '{last_symbol}'"

            self.result_label.config(text=error_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()