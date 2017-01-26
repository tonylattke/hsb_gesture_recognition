# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Colors Helpers

# Change from RGB to BGR
def generateRGBToBGR(r,g,b):
    return (b,g,r)

# Colors
colors = {
    'red'       : generateRGBToBGR(255,0,0),
    'green'     : generateRGBToBGR(0,255,0),
    'blue'      : generateRGBToBGR(0,0,255),
    'cyan'      : generateRGBToBGR(0,255,255),
    'magenta'   : generateRGBToBGR(255,0,255),
    'yellow'    : generateRGBToBGR(255,255,0),
    'black'     : generateRGBToBGR(0,0,0),
    'white'     : generateRGBToBGR(255,255,255)
}


# Color settings
colorSettings = {
    'finger'        : colors['cyan'],
    'fingerPoint'   : colors['red'],
    'defect'        : colors['blue'],
    'center'        : colors['magenta'],
    'handSurface'   : colors['green']
}
