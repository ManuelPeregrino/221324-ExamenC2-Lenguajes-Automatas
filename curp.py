import tkinter as tk
from tkinter import ttk
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class AutomatonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Manuel Peregrino Examen Corte 2')
        self.geometry('1440x900')
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20)
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=20)
        input_entry.pack(side=tk.LEFT, padx=(0, 10))
        submit_button = ttk.Button(input_frame, text='Generar Automata', command=self.generate_automaton)
        submit_button.pack(side=tk.LEFT)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def generate_automaton(self):
        user_input = self.input_var.get()
        if not user_input:
            return
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_xlim(-1, len(user_input) + 1)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        path, transitions = self.simulate_regex(user_input)
        is_valid = path[-1] == 'q4'
        states = ['q' + str(i) for i in range(len(transitions) + 1)]
        positions = {state: (i, 0) for i, state in enumerate(states)}
        self.draw_states(ax, states, positions, 'q4', path, transitions)
        result_text = "Valida" if is_valid else "Invalida"
        result_color = "green" if is_valid else "red"
        ax.text(len(user_input) / 2, -1.5, f"La cadena es {result_text}", fontsize=16, color=result_color, ha='center')
        self.canvas.draw()

    def simulate_regex(self, input_str):
        path = ['q0']
        transitions = []
        for i, char in enumerate(input_str):
            if char.isalpha() and i < 4:
                path.append(f'q{i+1}')
                transitions.append(char)
            else:
                break
        return path, transitions

    def draw_states(self, ax, states, positions, accept_state, path, transitions):
        for i, state in enumerate(states):
            pos = positions[state]
            if state in path:
                circle = patches.Circle(pos, 0.5, fill=True, color='yellow', linewidth=2, zorder=2)
                ax.add_patch(circle)
                if state == accept_state:
                    inner_circle = patches.Circle(pos, 0.3, fill=True, color='white', linewidth=2, zorder=3)
                    ax.add_patch(inner_circle)
            else:
                circle = patches.Circle(pos, 0.5, fill=False, color='black', linewidth=2, zorder=1)
                ax.add_patch(circle)
            ax.text(pos[0], pos[1], state, horizontalalignment='center', verticalalignment='center', fontsize=15, zorder=4)
            if i < len(states) - 1:
                next_state = states[i + 1]
                next_pos = positions[next_state]
                if next_state in path:
                    ax.annotate('', xy=next_pos, xytext=pos, arrowprops=dict(arrowstyle="->", color='red', lw=2), va='center', zorder=2)
                    if i < len(transitions):
                        label_pos = ((pos[0] + next_pos[0]) / 2, (pos[1] + next_pos[1]) / 2 + 0.1)
                        ax.text(*label_pos, transitions[i], horizontalalignment='center', verticalalignment='center', fontsize=12, color='red', zorder=3)
                else:
                    ax.annotate('', xy=next_pos, xytext=pos, arrowprops=dict(arrowstyle="->", color='black', lw=1), va='center', zorder=1)

if __name__ == '__main__':
    app = AutomatonApp()
    app.mainloop()
