# 8 x 19
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from PIL import ImageDraw



# Open image file
image = Image.open('v4_Medium_full.png')

draw = ImageDraw.Draw(image, "RGBA")
draw.rectangle(((0, 00), (int(image.size[0]/8), int(image.size[1]/19))), fill=(0,0,0,127))


# 8 x 19
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from PIL import ImageDraw 


# Open image file


for x in range(8, 9):
    for y in range(15):
            
        image = Image.open('v4_Medium_full.png')
        draw = ImageDraw.Draw(image, "RGBA")
        x_new = x*image.size[0]/9
        y_new = y*image.size[1]/15
        coordinate = ((x_new, y_new), (int(x_new + image.size[0]/9), int(y_new + image.size[1]/15)))
        print(coordinate)
        draw.rectangle(coordinate, fill=(100,10,10, 150))




        # Set up figure
        fig=plt.figure(figsize=(float(image.size[0]/10),float(image.size[1]/10)))
        ax=fig.add_subplot(111)

        # Remove whitespace from around the image
        fig.subplots_adjust(left=0,right=1,bottom=0,top=1)


        # Add the image
        ax.imshow(image)
        # Add some labels to the gridsquares




        # Save the figure
        fig.savefig('testing' + str(x) + str(y) + '.png', dpi = 5)

        
    

