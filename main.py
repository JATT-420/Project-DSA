import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def manacher(s):
    T = '#'.join('^{}$'.format(s))
    n = len(T)
    P = [0] * n
    C = R = 0
    for i in range(1, n - 1):
        P[i] = (R > i) and min(R - i, P[2 * C - i])
        while T[i + P[i] + 1] == T[i - P[i] - 1]:
            P[i] += 1
        if i + P[i] > R:
            C, R = i, i + P[i]
    max_len, center_index = max((n, i) for i, n in enumerate(P))
    start = (center_index - max_len) // 2
    return s[start:start + max_len], P


class ManacherVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manacher's Algorithm Visualizer")
        self.geometry("1200x800")

        self.input_label = tk.Label(self, text="Enter a string:")
        self.input_label.pack(pady=10)

        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.pack(pady=10)

        self.start_button = ttk.Button(self, text="Start Visualization", command=self.start_visualization)
        self.start_button.pack(pady=10)

        self.quit_button = ttk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.BOTTOM, pady=10)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def start_visualization(self):
        s = self.input_entry.get()
        if not s:
            self.result_label.config(text="Please enter a valid string.")
            return

        longest_palindrome, P = manacher(s)
        self.result_label.config(text=f"Longest Palindrome: {longest_palindrome}")

        T = '#'.join('^{}$'.format(s))
        n = len(T)

        self.ax.clear()
        self.bars = self.ax.bar(range(n), [0] * n, color='b', alpha=0.6)
        self.center_line = self.ax.axvline(x=0, color='r', lw=2, label='Center')
        self.right_line = self.ax.axvline(x=0, color='g', lw=2, label='Right Boundary')
        self.text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, fontsize=12,
                                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
        self.step_text = self.ax.text(0.02, 0.85, '', transform=self.ax.transAxes, fontsize=12,
                                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
        self.fig.legend(loc='upper right')

        self.P = P
        self.T = T
        self.n = n
        self.C = self.R = 0

        self.ani = animation.FuncAnimation(self.fig, self.update, frames=range(1, self.n - 1), init_func=self.init,
                                           repeat=False)
        self.canvas.draw()

    def init(self):
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, max(len(self.input_entry.get()) // 2, 10))
        self.ax.set_xticks(range(self.n))
        self.ax.set_xticklabels(self.T, fontsize=10)
        for bar in self.bars:
            bar.set_height(0)
        self.center_line.set_xdata(0)
        self.right_line.set_xdata(0)
        self.text.set_text('')
        self.step_text.set_text('')
        return self.bars, self.center_line, self.right_line, self.text, self.step_text

    def update(self, i):
        if self.R > i:
            self.P[i] = min(self.R - i, self.P[2 * self.C - i])
        while self.T[i + self.P[i] + 1] == self.T[i - self.P[i] - 1]:
            self.P[i] += 1
        if i + self.P[i] > self.R:
            self.C, self.R = i, i + self.P[i]
        for j, bar in enumerate(self.bars):
            bar.set_height(self.P[j])
        self.center_line.set_xdata(self.C)
        self.right_line.set_xdata(self.R)
        self.text.set_text(f'i: {i}, C: {self.C}, R: {self.R}')
        self.step_text.set_text(f'P: {self.P}')
        return self.bars, self.center_line, self.right_line, self.text, self.step_text

if __name__ == "__main__":
    app = ManacherVisualizer()
    app.mainloop()










    use_this ="babbabbabc"