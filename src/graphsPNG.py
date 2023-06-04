import graphviz
import os
from PIL import Image
from io import BytesIO

def storeGraphsPNG(PAR_PATH, infoLst, programName, typeGraph):
    # store each Digraph in a png
    infoLstPath = []

    for info in infoLst:
        # Create a Graphviz object
        graph = graphviz.Source(info["graph"])

        # Render the graph to a file
        graph.format = 'png'

        savePlace = os.path.join(PAR_PATH, "output", programName,"images", programName + "_" + typeGraph + "_" + str(infoLst.index(info)))

        # Render the graph to a byte stream
        graph.format = 'png'
        image_bytes = graph.pipe(format='png')

        # Set the desired size for the square image
        max_size = 500

        # Open the image using BytesIO
        image_stream = BytesIO(image_bytes)

        # Use PIL to resize the image
        image = Image.open(image_stream)

        # Calculate the aspect ratio and resize the image
        width, height = image.size
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        image = image.resize((new_width, new_height))

        # Create a new blank square image
        square_image = Image.new("RGBA", (max_size, max_size), (255, 255, 255, 0))

        # Calculate the position to paste the resized image
        x_offset = (max_size - new_width) // 2
        y_offset = (max_size - new_height) // 2

        # Paste the resized image onto the square image
        square_image.paste(image, (x_offset, y_offset))

        # Save the resized square image to a file
        square_image.save(savePlace + ".png")

        infoPath = {
            "path": "images/" + programName + "_" + typeGraph + "_" + str(infoLst.index(info)) + ".png"
        }

        infoLstPath.append(infoPath)

    return infoLstPath
