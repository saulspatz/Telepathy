import tkinter as tk
from tkinter import font
from board import tiles

SIZE = 40  # side of tile in pixels
colors = ('Blue', 'Pink','Green','Brown', 'Silver','Purple', 'Red', 'Orange', 'Yellow')
shapes = ('Bolt','Die', 'Gem', 'Hand', 'Moon', 'Eye', 'Star', 'Heart', 'Sun' )

class Telepathy(tk.Tk):
    def __init__(self, master=None):
        super().__init__()
        self.title('Telepathy')
        self.tileFont = font.Font(family ='Helvetica', size=11, weight = 'normal')
        self.indexFont = font.Font(family ='Helvetica', size=14, weight = 'normal')
        self.panelFont = font.Font(family ='Helvetica', size=12, weight = 'normal')
        self.excludeTileFont = font.Font(family ='Helvetica', size=12, weight = 'normal', overstrike=1)
        self.exludeIndexFont = font.Font(family ='Helvetica', size=14, weight = 'normal', overstrike=1)
        self.excludePanelFont = font.Font(family ='Helvetica', size=12, weight = 'normal', overstrike=1)
        self.grid()
        self.makeWidgets()
        self.resizable(False, False)
    
    def makeWidgets(self):
        self.makeTiles()
        self.makePanel()
        self.makeRecord()
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)

    def makeTiles(self):
        canvas= tk.Canvas(self, height = 20*SIZE, width=20*SIZE)
        alphabet = 'ABCDEFGHIJKLMNOPQR'
        for row in range(18):
            canvas.create_rectangle((0, (row+1)*SIZE),(SIZE, (row+2)*SIZE), fill = 'bisque')
            canvas.create_rectangle((19*SIZE, (row+1)*SIZE),(20*SIZE, (row+2)*SIZE), fill='bisque')
            canvas.create_text((SIZE/2, (row+3/2)*SIZE), anchor = tk.CENTER, 
                text = alphabet[row], font = self.indexFont
            )
            canvas.create_text((39*SIZE/2, (row+3/2)*SIZE), anchor = tk.CENTER, 
                text = alphabet[row], font = self.indexFont
            )
        for column in range(18):
            canvas.create_rectangle(((column+1)*SIZE, 0),((column+2)*SIZE, SIZE), fill = 'bisque')
            canvas.create_rectangle(((column+1)*SIZE,0), ((column+2)*SIZE, 20*SIZE), fill='bisque')
            canvas.create_text(((column+3/2)*SIZE, (SIZE/2)), anchor = tk.CENTER, 
                text = f'{column+1}', font = self.indexFont
            )
            canvas.create_text(((column+3/2)*SIZE,(39*SIZE/2)), anchor = tk.CENTER, 
                text = f'{column+1}', font = self.indexFont
            )

        for tile in tiles:
            row, column, color, shape, colorName = tile
            c =canvas.create_rectangle(
                ((column+1)*SIZE, (row+1)*SIZE),
                ((column+2)*SIZE, ((row+2)*SIZE)),
                fill = color,
                tags = ('tile', color, shape, f'row{row}', f'column{column}')
            )
            def callback(event, color=color, shape=shape, row=row, column=column):
                return self.onClickTile(event, color, shape, row, column, colorName)
            
            t = canvas.create_text((column+3/2)*SIZE, (row+3/2)*SIZE, anchor=tk.CENTER,
                    tags = ('tile', color, shape, f'row{row}', f'column{column}'),
                    text = shape,
                    font = self.tileFont
            )

            canvas.tag_bind(c, '<ButtonRelease-1>', callback)
            canvas.tag_bind(t, '<ButtonRelease-1>', callback)
        canvas.grid(row=1, column = 0, sticky = tk.N+tk.E+tk.W+tk.S)

    def makePanel(self):
        self.panel = tk.Frame(self, bg = 'bisque')
        panel = self.panel
        for idx, color in enumerate(colors):
            label = tk.Label(panel,bg ='bisque', fg = 'black', text = color, font = self.panelFont)
            label.grid(column = idx, row = 0)
        for idx, shape in enumerate(shapes):
             label = tk.Label(panel,bg ='bisque', fg = 'black', text = shape, font = self.panelFont)
             label.grid(column = idx, row = 1)
        for column in range(9):
            panel.columnconfigure(column, weight = 1)
        panel.grid(row=0, column = 0, sticky=tk.E+tk.W)

    def onClickTile(self,event, color, shape, row, column):
        return
    
    def makeRecord(self):
        self.record = tk.Text(self, bg = 'bisque')

root = Telepathy()


root.mainloop()


