import tkinter


def image_to_canvas(subframe, photo, row=0, column=0, padx=2, pady=1, sticky='nsew', x1=0, y1=0, anchor='nw'):
    """place graph image on canvas, and place canvas in subframe

    Args:
        subframe (tkinter.Frame): frame to contain canvas(s)
        photo (pyimage): graph image to add to canvas
        row (Int): grid row
        column (Int): grid column
        padx: x padding for widget
        pady (Int): y padding for widget
        sticky (Str): grid sticky
        x1 (Int): x coordinate
        y1 (Int): y coordinate
        anchor (Str): image anchor location
    """
    canvas = tkinter.Canvas(subframe)
    canvas.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
    canvas.create_image(x1, y1, image=photo, anchor=anchor)

    return photo


def create_menu(window, menu_def):
    """creates a mneu from the provided dict in the provided window
    
    Args:
        window (tkinter.Tk): frame to contain menu
        menu_def (tuple): menu structure definition    
    """
    def create_sub_menu(menu, submenu_def):
        sub_menu_ = tkinter.Menu()
        for sub_menu_name, sub_menu_command in submenu_def:
            sub_menu_.add_command(label=sub_menu_name, command=sub_menu_command)

        return sub_menu_

    top_menu = tkinter.Menu(window)

    for top_menu_name, sub_menu_tpl in menu_def:
        # sub_menu = tkinter.Menu()
        sub_menu = create_sub_menu(top_menu, sub_menu_tpl)
        # for sub_menu_name, sub_menu_command in sub_menu_tpl:
        #    sub_menu.add_command(label=sub_menu_name, command=sub_menu_command)
        top_menu.add_cascade(label=top_menu_name, menu=sub_menu)

    window.config(menu=top_menu)


def clear_subframe(frame, subframe):
    """clears and recreates subframe

    Args:
        frame (tkinter.Frame or LabelFrame): container for subframe
        subframe (tkinter.Frame or LabelFrame): containter for graphs
    """
    subframe.destroy()  # clear subframe
    subframe = tkinter.Frame(frame)
    subframe.grid(row=0, column=0, sticky='nsew')

    return subframe


def populate_list_box(listbox, data, select='keys'):
    """populates a list box in the GUI with the data provided.
    data can be of type 'dict or list'
    
    Args:
        listbox (Tkinter.Listbox): list box to add data to
        data (dict, list): data to add to list box
        select (Str): 'keys' add dict keys - Default, 
                      'values' add dict values
    """
    if type(data) is dict and select == 'keys':
        items = sorted(data.keys())
    elif type(data) is dict and select == 'values':
        items = sorted(data.values())
    else:
        items = data

    for item in items:
        listbox.insert(tkinter.END, item)


# TODO add format option for columns, maybe dict of {col name : string.format sequence}
def add_price_data(frame, subframe, data, col_order=None, col_titles=None, row=0, column=0, sub_sticky='nsew',
                   table_sticky='ew', headerfont=('arial', 10, 'bold'), tablefont=('arial', 10)):
    """takes data provided (DataFrame) and displays it in a table in a subframe
    Uses index as frist column
    
    Args:
        frame (tkinter.Frame or Labelframe): main frame
        subframe (tkinter.Frame) : subframe to be cleared
        col_order (list) : use to set order of columns or exclude columns from table, only provided will be
            returned.  
        col_titles (list) : Title for column to use in table
        row (int) : grid row
        column (int) : grid column
        sub_sticky (str) : grid sticky for subframe
        table_sticky (str) : grid sticky for table labels
        headerfont (tuple) : font for text in header
        tablefont (tuple) : font for text in table
        data (DataFrame): data to be displayed
    """
    # determine DataFrame column names
    if col_order is None:
        col_order = list(data)

    if col_titles is None:
        col_titles = col_order

    subframe.destroy()
    subframe = tkinter.Frame(frame)
    subframe.grid(row=row, column=column, columnspan=len(col_order), sticky=sub_sticky)

    row = 0
    column = 0
    for name in col_order:
        tkinter.Label(subframe, text=col_titles[column], font=headerfont)\
            .grid(row=row, column=column, sticky=table_sticky)  # add label
        if column == 0:
            col_data = data.index
        else:
            col_data = data[name]

        for data_row in col_data:
            row += 1
            tkinter.Label(subframe, text=data_row, font=tablefont)\
                .grid(row=row, column=column, sticky=table_sticky)  # add data
        row = 0
        column += 1

    return subframe


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    link: http://stackoverflow.com/questions/3221956/what-is-the-simplest-way-to-make-tooltips-in-tkinter
    """
    def __init__(self, widget, text='widget info'):
        print(type(widget))
        self.waittime = 500     # milliseconds
        self.wraplength = 180   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        # x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a top level window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1,
                              wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
