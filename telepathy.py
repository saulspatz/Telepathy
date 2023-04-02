import tkinter as tk
from tkinter import font
from board import tiles

SIZE = 40  # side of tile in pixels
colors = ('Blue', 'Pink', 'Green', 'Brown', 'Silver',
          'Purple', 'Red', 'Orange', 'Yellow')
shapes = ('Bolt', 'Die', 'Gem', 'Hand', 'Moon', 'Eye', 'Star', 'Heart', 'Sun')


class Telepathy(tk.Tk):
    def __init__(self, master=None):
        super().__init__()
        self.title('Telepathy')
        self.tileFont = font.Font(family='Helvetica', size=11, weight='normal')
        self.indexFont = font.Font(
            family='Helvetica', size=14, weight='normal')
        self.panelFont = font.Font(
            family='Helvetica', size=12, weight='normal')
        self.recordFont = font.Font(
            family='Helvetica', size=14, weight='normal')
        self.excludeTileFont = font.Font(
            family='Helvetica', size=12, weight='normal', overstrike=1)
        self.excludeIndexFont = font.Font(
            family='Helvetica', size=14, weight='normal', overstrike=1)
        self.excludePanelFont = font.Font(
            family='Helvetica', size=12, weight='normal', overstrike=1)
        self.grid()
        self.makeWidgets()
        self.resizable(False, False)

    def makeWidgets(self):
        self.makeTiles()
        self.makePanel()
        self.makeRecord()

    def makeTiles(self):
        self.canvas = tk.Canvas(self, height=20*SIZE, width=20*SIZE)
        canvas = self.canvas
        alphabet = 'ABCDEFGHIJKLMNOPQR'
        for row in range(18):
            canvas.create_rectangle(
                (0, (row+1)*SIZE), (SIZE, (row+2)*SIZE), fill='bisque')
            canvas.create_rectangle(
                (19*SIZE, (row+1)*SIZE), (20*SIZE, (row+2)*SIZE), fill='bisque')
            canvas.create_text((SIZE/2, (row+3/2)*SIZE), anchor=tk.CENTER,
                               text=alphabet[row], font=self.indexFont,
                               tag = f'index{alphabet[row]}'
                               )
            canvas.create_text((39*SIZE/2, (row+3/2)*SIZE), anchor=tk.CENTER,
                               text=alphabet[row], font=self.indexFont,
                               tag = f'index{alphabet[row]}'
                               )
        for column in range(18):
            canvas.create_rectangle(
                ((column+1)*SIZE, 0), ((column+2)*SIZE, SIZE), fill='bisque')
            canvas.create_rectangle(
                ((column+1)*SIZE, 0), ((column+2)*SIZE, 20*SIZE), fill='bisque')
            canvas.create_text(((column+3/2)*SIZE, (SIZE/2)), anchor=tk.CENTER,
                               text=f'{column+1}', font=self.indexFont, tag=f'index{column}')
            canvas.create_text(((column+3/2)*SIZE, (39*SIZE/2)), anchor=tk.CENTER,
                               text=f'{column+1}', font=self.indexFont, tag=f'index{column}')

        for tile in tiles:
            row, column, color, shape, colorName = tile
            c = canvas.create_rectangle(
                ((column+1)*SIZE, (row+1)*SIZE),
                ((column+2)*SIZE, ((row+2)*SIZE)),
                fill=color,)

            def callback(event, color=color, shape=shape, row=row, column=column, colorName=colorName):
                return self.onClickTile(event, color, shape, row, column, colorName)

            t = canvas.create_text((column+3/2)*SIZE, (row+3/2)*SIZE, anchor=tk.CENTER,
                                   tags=('text', color, shape,
                                         f'row{row}', f'column{column}'),
                                   text=shape,
                                   font=self.tileFont)

            canvas.tag_bind(c, '<ButtonRelease-1>', callback)
            canvas.tag_bind(t, '<ButtonRelease-1>', callback)
        canvas.grid(row=1, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

    def makePanel(self):
        self.panel = tk.Frame(self, bg='bisque')
        panel = self.panel
        self.labels = labels = {}
        for idx, color in enumerate(colors):
            label = tk.Label(panel, bg='bisque', fg='black',
                             text=color, font=self.panelFont)
            labels[color.lower()] = label
            label.grid(column=idx, row=0)
        for idx, shape in enumerate(shapes):
            label = tk.Label(panel, bg='bisque', fg='black',
                             text=shape, font=self.panelFont)
            labels[shape.lower()] = label
            label.grid(column=idx, row=1)
        for column in range(9):
            panel.columnconfigure(column, weight=1)
        panel.grid(row=0, column=0, sticky=tk.E+tk.W)

    def makeRecord(self):
        self.record = tk.Text(
            self, bg='bisque', height=40, width=40, undo=True)
        self.record.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S)
        scrollY = tk.Scrollbar(self, orient=tk.VERTICAL,
                               command=self.record.yview)
        scrollY.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S)
        self.record['yscrollcommand'] = scrollY.set

    def onClickTile(self, event, color, shape, row, column, colorName):
        canvas = self.canvas

        for text in canvas.find_withtag('text'):
            tags = set(canvas.gettags(text))
            if {color, shape, f'row{row}', f'column{column}'} & tags:
                canvas.itemconfigure(text, font=self.excludeTileFont)

        for label in canvas.find_withtag(f'index{column}'):
            canvas.itemconfigure(label, font=self.excludeIndexFont)

        base = ord('A')
        for label in canvas.find_withtag(f'index{chr(base+row)}'):
            canvas.itemconfigure(label, font=self.excludeIndexFont)

        for idx in colorName.lower(), shape:
            self.labels[idx].configure(font=self.excludePanelFont)

root = Telepathy()


root.mainloop()
