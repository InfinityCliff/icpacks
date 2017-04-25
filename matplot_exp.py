from pylab import rcParams
import io
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


def create_graph_image(data, title='Title', x_name='X', y_name='Y', height=5, width=10, dpi=50):
    """return (ImageTk.PhotoImage) image of the graph

    Args:
        data : data to plot  
        title (Str) : Graph Title
        x_name (Str) : x axis name
        y_name (Str): y axis name
        height (int): height of graph
        width (int): width of graph
        dpi (int): dpi of graph
    """
    rcParams['figure.figsize'] = width, height

    plt.style.use('fivethirtyeight')
    plt.plot(data)  # TODO test that various types of data will plot correctly
    plt.title(title)
    # TODO add x and y axis names

    buf = io.BytesIO()  # open buffer
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')  # save figure image to buffer
    buf.seek(0)  # return buffer to start

    image_buff = Image.open(buf)  # save image from buffer
    image = image_buff.copy()  # make copy of image so image is not lost when buffer closes
    buf.close()  # close buffer
    plt.close()  # clear plt

    return ImageTk.PhotoImage(image)
