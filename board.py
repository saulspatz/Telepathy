from collections import Counter, namedtuple

Picture = namedtuple('Picture', 'color shape'.split()) 
colorArray = [
'APGBYVROSGSBRVYOAP',
'PGSOBRAVYVRPYSAGBO',
'SYBRVPGAOYBVPAORGS',
'BOVPASYGRPGYVOSBRA',
'VRASGBOYPSYOARBVPG',
'GSYVOAPRBOVASGRPYB',
'RAPYSOVBGBORGPVASY',
'OVRGPYBSARAGBYPSOV',
'YBOARGSPVAPSOBGYVR',
'PGAVOBRYSBVRSOYAPG',
'SYGARVPOBAGSVPRYBO', 
'YBSPARGVORPGOAVSYB',
'BOYGPASRVPSYRGABOV',
'GSPRVOABYVAPBROGSY',
'VROYSGBPASBOPYGVRA',
'APROBYVSGORAYVBPGS',
'RAVBYSOGPYOVGBSRAP',
'OVBSGPYARGYBASPOVR'
]

shapeArray = [
'BDGPMESHCESDMCBGPH',
'PHEDBCMGSPHSGDEBCM',
'HESGDMPCBSBGPMDCHE',
'ESBCGPHMDGCPSEMHBD',
'SBDMCHEPGCMHBSPEDG',
'DGCHPSBEMBDCHPGMES',
'MPHBSGCDEMPEDBHSGC',
'CMPSEDGBHDGMEHCPSB',
'GCMEHBDSPHEBCGSDMP',
'MPCDBSGEHCPHDMGESB',
'PHMGDBCSEPESCHMBDG',
'DGBEHPSMCBGCEDSMPH',
'HEPCGDMBSDCMSGBPHE',
'BDSHPMECGMHEGPCSBD',
'ESHMCGPDBGMPBCDHES',
'SBEPMCHGDSDGHBECMP',
'CMGBSEDHPEBDPSHGCM',
'GCDSEHBPMHSBMEPDGC'
]

board = { }
for row in range(18):
    for column in range(18):
        board[row, column] = Picture(colorArray[row][column], shapeArray[row][column])

for array in (colorArray, shapeArray):
    for line in array:
        assert list(Counter(line).values()) == 9*[2]

for column in range(18):
    colColors = [board[row, column].color for row in range(18)]
    assert list(Counter(colColors).values()) == 9*[2]
    colShapes = [board[row, column].shape for row in range(18)]
    assert list(Counter(colColors).values()) == 9*[2]

assert list(Counter(board.values()).values()) == 81*[4]

for n in range(18):
    row = [board[n, column] for column in range(18)]
    assert len(set(row)) == 18
    col = [board[r, n] for r in range(18)]
    assert len(set(col)) == 18

Tile = namedtuple('Tile', 'row column color shape colorName'.split()) 
colors = {}
shapes = {}
names = {}

colors['A'] = 'LightBlue2'
colors['P'] = 'pink'
colors['G'] = 'lightgreen'
colors['B'] = 'brown3'
colors['Y'] = '#dd0'
colors['V'] = 'medium purple'
colors['R'] = 'red'
colors['O'] = 'orange'
colors['S'] = 'silver'

names['A'] = 'blue'
names['P'] = 'pink'
names['G'] = 'green'
names['B'] = 'brown'
names['Y'] = 'yellow'
names['V'] = 'purple'
names['R'] = 'red'
names['O'] = 'orange'
names['S'] = 'silver'

shapes['B'] = 'bolt'
shapes['H'] = 'heart'
shapes['E'] = 'eye'
shapes['S'] = 'star'
shapes['C'] = 'sun'
shapes['G'] = 'gem'
shapes['D'] = 'dice'
shapes['P'] = 'hand'
shapes['M'] = 'moon'

tiles = set()
for row in range(18):
    for column in range(18):
        color = colorArray[row][column]
        tiles.add(Tile(row, column, 
                       colors[color], 
                       shapes[shapeArray[row][column]], 
                       names[color]))
