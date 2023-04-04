import tkinter as tk
from tkinter import font
from tkinter import messagebox
from board import tiles

SIZE = 40  # side of tile in pixels
colors = ('Blue', 'Pink', 'Green', 'Brown', 'Silver',
          'Purple', 'Red', 'Orange', 'Yellow')
shapes = ('Bolt', 'Die', 'Gem', 'Hand', 'Moon', 'Eye', 'Star', 'Heart', 'Sun')
colorTags = {c.lower() for c in colors}
shapeTags = {s.lower() for s in shapes}

class Telepathy(tk.Tk):
    def __init__(self, master=None):
        super().__init__()
        self.title('Telepathy')
        '''
        If new fonts are needed add them to the END of the list
        Tk numbers the fonts in the order they are assigned, and we
        need to know the internal name in order to know which tiles have
        been excluded.
        '''
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
        alphabet = self.alphabet = 'ABCDEFGHIJKLMNOPQR'
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
                fill=color,
                tags=('tile', colorName, shape,
                      f'row{alphabet[row]}', f'column{column+1}'))

            def callback(event, shape=shape, row=row, column=column, colorName=colorName):
                return self.onClickTile(event, shape, row, column, colorName)

            t = canvas.create_text((column+3/2)*SIZE, (row+3/2)*SIZE, anchor=tk.CENTER,
                                   tags=('text', colorName, shape,
                                         f'row{alphabet[row]}', f'column{column+1}'),
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
        self.record = tk.Text(self, bg='bisque', height=40, width=40, 
                              undo=True, font = self.recordFont)
        self.record.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S)
        scrollY = tk.Scrollbar(self, orient=tk.VERTICAL,
                               command=self.record.yview)
        scrollY.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S)
        self.record['yscrollcommand'] = scrollY.set

    def onClickTile(self, event, shape, row, column, colorName):
        canvas = self.canvas
        base = ord('A')
        rowIndex = chr(base+row)
        name =colorName.lower()

        result = messagebox.askyesnocancel(message = f'{rowIndex}{column+1} {name} {shape}')
        if result == None:   # Cancel
            return
        if result == False:  # No
            for text in canvas.find_withtag('text'):
                tags = set(canvas.gettags(text))
                if intersect := {colorName, shape, f'row{rowIndex}', f'column{column+1}'} & tags:
                    canvas.itemconfigure(text, font=self.excludeTileFont)
                    for tag in intersect:
                        canvas.dtag(text, tag)
                    print(canvas.gettags(text))

            for label in canvas.find_withtag(f'index{column}'):
                canvas.itemconfigure(label, font=self.excludeIndexFont)

            for label in canvas.find_withtag(f'index{rowIndex}'):
                canvas.itemconfigure(label, font=self.excludeIndexFont)

            for idx in name, shape:
                self.labels[idx].configure(font=self.excludePanelFont)
        else:  #Yes
            currentTags = [tag for tag in canvas.find_withtag('current') 
                    if tag not in ('current', 'text', 'tile')]
            found = len(currentTags) == 1 
            if found:
                foundTag = currentTags[0]
                if foundTag.startswith('row'):
                    tagType = 'row'
                elif foundTag.startswith('column'):
                    tagType = 'column'
                elif foundTag in colorTags:
                    tagType = 'color'
                elif foundTag in shapeTags:
                    tagType = 'shape'
                else:
                    raise Exception(f'unkown tag type {foundTag}')
            for text in canvas.find_withtag('text'):
                tags = set(canvas.gettags(text))
                if {colorName, shape, f'row{rowIndex}', f'column{column+1}'} & tags == set():
                    canvas.itemconfigure(text, font=self.excludeTileFont)
                if found and foundTag not in tags:
                    canvas.itemconfigure(text, font=self.excludeTileFont)
        excluded = 0
        for text in canvas.find_withtag('text'):
            print(canvas.itemcget(text, 'font'))
            if canvas.itemcget(text, 'font') == 'font5':
                excluded += 1
        self.record.insert(tk.END, f"{rowIndex}{column+1} {name} {shape} {'Warm' if result else 'No'} {excluded}\n")
    
root = Telepathy()
root.mainloop()
