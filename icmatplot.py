from pylab import rcParams
import io
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


def create_graph_image(data, title='Title', x_name='X', y_name='Y', height=5, width=10, dpi=50):
    """return (ImageTk.PhotoImage) image of the graph

        :param data:: data to plot  
        :param title:str: Graph Title
        :param x_name:str : x axis name
        :param y_name:str: y axis name
        :param height:int: height of graph
        :param width:int: width of graph
        :param dpi:int: dpi of graph
    """
    rcParams['figure.figsize'] = width, height
    if (len(data)) > 0:
        plt.style.use('fivethirtyeight')
        plt.plot(data)  # TODO test that various types of data will plot correctly
        plt.title(title)
        # TODO add x and y axis names
    else:
        return None

    buf = io.BytesIO()  # open buffer
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')  # save figure image to buffer
    buf.seek(0)  # return buffer to start

    image_buff = Image.open(buf)  # save image from buffer
    image = image_buff.copy()  # make copy of image so image is not lost when buffer closes
    buf.close()  # close buffer
    plt.close()  # clear plt

    return ImageTk.PhotoImage(image)
