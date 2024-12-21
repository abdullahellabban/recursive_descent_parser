import tkinter as tk
from tkinter import scrolledtext


class RecursiveDescentParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recursive Descent Parser")
        self.root.geometry("700x550")
        self.root.configure(bg='#f2f2f2')

        self.grammar = {}
        self.start_symbol = None
        self.input_string = ""
        self.index = 0

        title_label = tk.Label(root, text="Recursive Descent Parser", font=("Arial", 16), bg='#4CAF50', fg='white')
        title_label.pack(pady=10, fill=tk.X)

        grammar_label = tk.Label(root, text="Enter Grammar Rules:", font=("Arial", 12), bg='#f2f2f2')
        grammar_label.pack(pady=5)
        self.grammar_input = scrolledtext.ScrolledText(root, width=80, height=10, font=("Courier", 10))
        self.grammar_input.pack(pady=10)

        string_label = tk.Label(root, text="Enter String to Parse:", font=("Arial", 12), bg='#f2f2f2')
        string_label.pack(pady=5)
        self.string_input = tk.Entry(root, width=80, font=("Courier", 10))
        self.string_input.pack(pady=5)

        self.parse_button = tk.Button(root, text="Parse String", font=("Arial", 12), bg='#4CAF50', fg='white', command=self.parse_string)
        self.parse_button.pack(pady=5)

        self.check_button = tk.Button(root, text="Check Grammar Simplicity", font=("Arial", 12), bg='#4CAF50', fg='white', command=self.check_simplicity)
        self.check_button.pack(pady=5)

        output_label = tk.Label(root, text="Output:", font=("Arial", 12), bg='#f2f2f2')
        output_label.pack(pady=5)
        self.output = scrolledtext.ScrolledText(root, width=80, height=15, font=("Courier", 10), state='disabled')
        self.output.pack(pady=10)

    def log(self, message):
        self.output.configure(state='normal')
        self.output.insert(tk.END, f"{message}\n")
        self.output.see(tk.END)
        self.output.configure(state='disabled')

    def input_grammar(self):
        self.grammar.clear()
        grammar_text = self.grammar_input.get("1.0", tk.END).strip()

        for line in grammar_text.split("\n"):
            if "->" not in line:
                continue

            lhs, rhs = map(str.strip, line.split("->"))
            rhs = [r.strip() for r in rhs.split('|')]
            if lhs in self.grammar:
                self.grammar[lhs].extend(rhs)
            else:
                self.grammar[lhs] = rhs

        if self.grammar:
            self.start_symbol = list(self.grammar.keys())[0]
        else:
            self.log("No valid grammar rules found.")

    def check_simplicity(self):
        self.input_grammar()
        if not self.grammar:
            return

        for non_terminal, rules in self.grammar.items():
            for rule in rules:
                if rule.startswith(non_terminal):
                    self.log(f"Grammar isn't simple: Left recursion in '{non_terminal} -> {rule}'.")
                    return

        self.log("The grammar is simple!")

    def parse(self, input_string):
        self.input_string = input_string
        self.index = 0

        def parse_non_terminal(non_terminal):
            initial_index = self.index
            for rule in self.grammar[non_terminal]:
                self.index = initial_index
                if parse_rule(rule):
                    return True
            return False

        def parse_rule(rule):
            for symbol in rule:
                if symbol.isupper():
                    if not parse_non_terminal(symbol):
                        return False
                else:
                    if self.index < len(self.input_string) and self.input_string[self.index] == symbol:
                        self.index += 1
                    else:
                        return False
            return True

        return parse_non_terminal(self.start_symbol) and self.index == len(self.input_string)

    def parse_string(self):
        self.input_grammar()
        if not self.grammar:
            return

        input_string = self.string_input.get().strip()
        if not input_string:
            self.log("No input string to parse.")
            return

        if self.parse(input_string):
            self.log("The input string is Accepted!")
        else:
            self.log("The input string is Rejected!")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecursiveDescentParserGUI(root)
    root.mainloop()
