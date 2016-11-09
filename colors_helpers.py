# Colors Helpers

# Change from RGB to BGR
def generateRGBToBGR(r,g,b):
	return (b,g,r)

# Colors
colors = {
	'red'	: generateRGBToBGR(255,0,0),
	'green'	: generateRGBToBGR(0,255,0),
	'blue'	: generateRGBToBGR(0,0,255)
}