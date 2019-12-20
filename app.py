# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter.filedialog import askopenfile as aof
from sympy import symbols, Symbol

from dnf import Dnf


class App(tk.Tk):
    _x, _y = 0, 0
    _matrix = []
    done = False

    def __init__(self):
        super().__init__()

        # Configuration parameters
        self.title("DNF - created by PB")
        self.minsize(700, 600)
        self.geometry("700x600")

        # Templates style
        style = ttk.Style()
        style.configure("TLabel", font=('Helvetica', 15, 'bold'), anchor="center")
        style.configure("B.TButton", font=('Helvetica', 15), anchor="center")

        # Elements style
        self.main_frame = tk.Frame(self, width=500, height=100)
        self.title_label = ttk.Label(self.main_frame, text="DNF")
        self.file_button = ttk.Button(self.main_frame, text="Choose File", command=lambda: self.load_file(),
                                      style="B.TButton")
        self.start_button = ttk.Button(self.main_frame, text="Start", command=lambda: self.start(),
                                       style="B.TButton")
        self.matrix_frame = tk.Frame(self, width=100, height=100)
        self.answer_frame = tk.Label(self, width=100, height=2)

        # Elements position
        self.main_frame.pack(fill=tk.BOTH)
        self.matrix_frame.pack()
        self.title_label.grid(row=0, column=0, sticky="NSEW")
        self.file_button.grid(row=1, column=0, sticky="NSEW", padx=150)
        self.start_button.grid(row=2, column=0, sticky="NSEW", padx=150)
        self.main_frame.grid_rowconfigure(0, weight=10)
        self.main_frame.grid_columnconfigure(0, weight=10)
        self.answer_frame.pack()

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

    def load_file(self):
        file = aof(mode='r', filetypes=[('Text files', '*.txt')])
        if file is not None:
            f_line = file.readline().split(' ')
            x = int(f_line[0])
            self._x = x
            self._y = int(f_line[1])
            table, j = [], 0
            lines = file.readlines()
            file.close()
            for line in lines:
                tmp, value = [], line.split(' ')
                if j == 0:
                    f = symbols("f1:" + str(self._x))
                    tmp.extend(f[x] for x in range(len(f)))
                    tmp.append('y')
                    tmp.append('-/-')
                    table.append(tmp)
                    tmp, j = [], 1
                tmp.extend(int(value[i]) for i in range(x))
                tmp.append(Symbol("x" + str(j)))
                j += 1
                table.append(tmp)
            self._matrix = table
            if self.matrix_frame.grid_slaves():
                self.clear()
            self.draw_matrix()
            self.done = False

    def start(self):
        if not self._matrix or self._x == 0 or self._y == 0:
            msg.showwarning("Warning",
                            "Please choose Text file! \nExample file content:\n4 3\n1 2 3 4\n5 6 7 8\n7 6 5 4")
            return
        else:
            if not self.done:
                dnf = Dnf(self._matrix, self._x, self._y)
                self.draw_matrix(dnf.get_result())
                self.done = True
                del dnf
                return
            else:
                msg.showinfo("Info", "Please choose new Text file!")
                return

    def clear(self):
        label_list = self.matrix_frame.grid_slaves()
        self.answer_frame.configure(text='')
        for label in label_list:
            label.destroy()

    def draw_matrix(self, test=''):
        strip = [i for i in range((self._x + 1) * (self._y + 1))]
        tmp = 0
        for i in range(self._y + 1):
            for j in range(self._x + 1):
                if i == 0 or j == self._x:
                    strip[tmp] = tk.Label(self.matrix_frame, text=self._matrix[i][j], width=4, height=2,
                                          relief='raised',
                                          background='red').grid(row=i, column=j)
                else:
                    strip[tmp] = tk.Label(self.matrix_frame, text=self._matrix[i][j], width=4, height=2,
                                          relief='raised',
                                          background='blue').grid(row=i, column=j)

                tmp += 1
        if test == '':
            pass
        else:
            h = test[0]
            val_to_draw = test[1]
            for val in val_to_draw:
                i = int(val[0])
                j = int(val[1])
                strip[i * j] = tk.Label(self.matrix_frame, text=self._matrix[i][j], width=4, height=2,
                                        relief='raised',
                                        background='white').grid(row=i, column=j)
            print(h)
            self.answer_frame.configure(text="Answer -->  " + str(h))

    def safe_destroy(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
