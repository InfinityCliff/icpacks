import tkinter
import os
from PIL import ImageTk, Image
import re
import numpy as np
import pandas as pd

icons = {'bookmark': 'add_bookmark.png',
         'clear': 'clear.png',
         'fileopen': 'fileopen.png',
         'folder': 'folder.png',
         'minus': 'minus.png',
         'plus': 'plus.png',
         'theme': 'theme.png'
         }


def icon(icon_name, size=16):
    """returns image for use in menu icons

        :param icon_name:str: name of icon to retrieve in icons dict
        :param size:int: size of icon to be returned
        """
    filename = os.path.dirname(__file__) + '\\rsc\\' + icons[icon_name]
    img = Image.open(filename)
    if img.width > size:
        img = img.resize((size, size), Image.ANTIALIAS)

    return ImageTk.PhotoImage(img)


def image_to_canvas(subframe, photo, row=0, column=0, padx=2, pady=1, sticky='nsew', x1=0, y1=0, anchor='nw', canvas=None):
    """place graph image on canvas, and place canvas in subframe

        :param subframe:tkinter.Frame: frame to contain canvas(s)
        :param photo:pyimage: graph image to add to canvas
        :param row:int: grid row
        :param column:int: grid column
        :param padx:int: x padding for widget
        :param pady:int: y padding for widget
        :param sticky:str: grid sticky
        :param x1:int: x coordinate
        :param y1:int: y coordinate
        :param anchor:Str: image anchor location
        :param canvas:tkinter.Canvas: canvas to add image to, if none will create and add to subframe 
    """
    if canvas is None:
        canvas = tkinter.Canvas(subframe)
    canvas.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
    canvas.create_image(x1, y1, image=photo, anchor=anchor)

    return photo, canvas


def create_menu(window, menu_def):
    """creates a mneu from the provided dict in the provided window

        :param window:tkinter.Tk: frame to contain menu
        :param menu_def:tuple: menu structure definition
        
    Menu Format:
    menu_format = (('', '', '', ''),   # Tuple of strings for top row items, for single item define as ('item',)
                                       # dict keys of items from first tuple, values are ('menu item', 'command') pairs
                                       # for single ('menu item', 'command') pair define as (('menu item', 'command'),)
                    ({'File': (('Save', '>save'), ('Export Price List', '>export'), ('Exit', self._menu_exit)),
                      'Edit': (('Undo', '>undo'), ('Redo', '>redo')),
                      'Settings': ('Theme',    # Use a string as first item in tuple to indicate a sub-menu
                                               # follow with ('menu item', 'command') pairs
                                   (('Default', '>def'), ('Flat', '>flat'), ('Dark', '>dark'))), 
                      'Help': (('VDOT Bid Tabs', '>tab'), ('About', '>about'))}))
                      
                      to add sperator: ('---', None)
    """
    # TODO - test for things like one top row item and one command pair item
    def create_sub_menu(submenu_def):
        """returns sub menu to add to menu cascade
        
            :param submenu_def:tuple: (('menu item', 'command'), () pairs, use str as first item in tuple to create
                        submenu cascade
        """
        sub_menu_ = tkinter.Menu(tearoff=0)
        for sub_menu_item in submenu_def:
            if type(sub_menu_item) is tuple:
                if sub_menu_item[0] == '---':
                    sub_menu_.add_separator()
                else:
                    try:
                        img = icon(sub_menu_item[2])
                        icon_list.append(img)
                    except IndexError:
                        img = None
                    sub_menu_.add_command(label=sub_menu_item[0], command=sub_menu_item[1], image=img,
                                          compound=tkinter.LEFT)
            else:
                sub_menu_b = create_sub_menu(submenu_def[1])
                sub_menu_.add_cascade(label=sub_menu_item, menu=sub_menu_b)
                return sub_menu_
        return sub_menu_

    icon_list = []
    top_menu = tkinter.Menu(window, tearoff=1)
    for top_menu_item in menu_def[0]:
        sub_menu = create_sub_menu(menu_def[1][top_menu_item])
        top_menu.add_cascade(label=top_menu_item, menu=sub_menu)

    window.config(menu=top_menu)


def clear_subframe(frame, subframe):
    """clears and recreates subframe

        :param frame:tkinter.Frame or LabelFrame: container for subframe
        :param subframe:tkinter.Frame or LabelFrame: containter for graphs
    """
    subframe.destroy()  # clear subframe
    subframe = tkinter.Frame(frame)
    subframe.grid(row=0, column=0, sticky='nsew')

    return subframe


def populate_list_box(listbox, data, select='keys'):
    """populates a list box in the GUI with the data provided.
    data can be of type 'dict or list'
    
        :param listbox:Tkinter.Listbox: list box to add data to
        :param data:dict or list: data to add to list box
        :param select:Str: 'keys' add dict keys - Default, 
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
    
        :param frame:tkinter.Frame or Labelframe: main frame
        :param subframe:tkinter.Frame : subframe to be cleared
        :param data:pandas.DataFrame: data to be displayed
        :param col_order:list: use to set order of columns or exclude columns from table, only provided will be
            returned.  
        :param col_titles:list: Title for column to use in table
        :param row:int: grid row
        :param column:int: grid column
        :param sub_sticky:str: grid sticky for subframe
        :param table_sticky:str: grid sticky for table labels
        :param headerfont:tuple: font for text in header
        :param tablefont:tuple: font for text in table
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


class TableController(tkinter.Frame):

    def __init__(self, window, size, index=None, header=None, row=0, column=0, sticky='nsew', columnspan=1,
                 bold=None, currency=None, float_=None, int_=None, blank='--'):
        """creates a table
        
            :param: window:tkinter.Frame|Labelframe: containter for tablecontroller
            :param: row:int: row in window
            :param: column:int: column in window
            :param: columnspan:int: columnspan in window
            :param: size:str: size of table - columns x rows 
            :param: bold:tuple: columns or rows to be bolded, 0 indexed with or without index/headers.
                    Designate by: ('col0, 'col2', 'row1')
            :param: currency: columns or rows to be formated as currency '$0.00', 0 indexed with or without 
                    index/headers.  Designate by: ('col0, 'col2', 'row1')
            :param: float_: columns or rows to be formated as float '0.00', 0 indexed with or without index/headers.
                    Designate by: ('col0, 'col2', 'row1') # TODO be able to set precision
            :param: int: columns or rows to be formated as int '0', 0 indexed with or without index/headers.
                    Designate by: ('col0, 'col2', 'row1')  # TODO not working, need to code
        """
        super().__init__(window)
        super().grid(row=row, column=column, sticky=sticky, columnspan=columnspan)

        cols, rows = [int(x) for x in size.split('x')]

        if index is not None:
            self.index_is_set = True
        else:
            self.index_is_set = False

        if header is not None:
            self.header_is_set = True
            col_range = header.copy()
        else:
            self.header_is_set = False
            col_range = range(cols)

        self.sub_frame = tkinter.Frame(self)
        self.sub_frame.grid(row=0, column=0, sticky='nsew')
        self.blank_cell = blank
        self.df = pd.DataFrame(index=index, columns=header)
        for colname in col_range:
            self.df[colname] = self.default_col(rows)

        self.draw_table()

    def update_data(self, new_data, join='left', overwrite=True, filter_func=None, raise_conflict=False):
        if type(new_data) == np.ndarray:
            new_data = pd.DataFrame(new_data)
        elif type(new_data) == dict:
            new_data = pd.DataFrame.from_dict(new_data)
        elif type(new_data) == pd.DataFrame:
            pass
        else:
            return

        new_data.set_index(self.df.index.values, inplace=True)
        new_data.columns = self.df.columns
        print(new_data)
        for column in self.df.columns:
            print(column)
            self.df[column] = new_data[column]

        self.draw_table()

    def default_col(self, rows):
        return [self.blank_cell] * rows

    def add_label(self, row, col, text, fontstyle='normal'):
        lbl = tkinter.Label(self.sub_frame, text=text, font=('arial', 10, fontstyle))
        lbl.grid(row=row, column=col, sticky='nsew')
        return lbl

    def draw_table(self):
        self.sub_frame = clear_subframe(self, self.sub_frame)

        col = 0
        row = 1
        # add index to table
        if self.index_is_set:
            index_labels = list(self.df.index.tolist())
            for item in index_labels:
                self.add_label(row=row, col=col, text=item)
                row += 1
            col += 1

        # add headers to table
        header_labels = list(self.df)
        row = 0
        if self.header_is_set:
            for col_label in header_labels:
                self.add_label(row=row, col=col, text=col_label)
                col += 1

        # add data to table
        col = 0 + self.index_is_set
        for col_label in header_labels:
            row = 1
            for item in self.df[col_label]:
                self.add_label(row=row, col=col, text=item)
                row += 1
            col += 1

        self.update()
        print(self)
        print(self.df.index.values)

    def insert_row(self, row, value, sort=None):
        """inserts a row in the table at specified lcoation"""
        self.df.loc[row] = value
        if sort is not None:
            if sort.upper() in ['F', 'FORWARD', 'YES']:
                ascending = True
            elif sort.upper() in ['R', 'REVERSE', 'REVERSED', 'BACKWARDS']:
                ascending = False
            self.df.sort_index(inplace=True, ascending=ascending)

        self.draw_table()

    def insert(self, loc, column, value, allow_duplicates=False):
        """inserts a column in the table at specified location"""
        self.df.insert(loc, column, value)
        self.df.reindex()
        self.draw_table()

    def column(self, col, data=None, format_=None, dec=2,  fontname='arial', fontstyle='normal',
               fontsize=10):
        font = ('arial', 10, 'normal')

        if data is not None:
            formated_data = []
            # format accordingly
            for label_text in data:
                if format_ is not None:
                    if 'float' in format_:
                        fc = '{0:.' + str(dec) + 'f}'
                        formated_data.append(fc.format(float(label_text)))
                    if '$' in format_:
                        non_decimal = re.compile(r'[^\d.]+')  # regex to strip off non number info
                        text = non_decimal.sub('', label_text)
                        fc = '${0:.' + str(dec) + 'f}'
                        formated_data.append(fc.format(float(text)))
                    if 'int' in format_:
                        # noinspection
                        non_decimal = re.compile(r'[^\d.]+')  # regex to strip off non number info
                        text = non_decimal.sub('', label_text)
                        formated_data.append(int(text))
                else:
                    formated_data = data.copy()

            # reassign formatted text, etc to label
            if type(col) is str:
                print(self.df[col], '----------------------')
                self.df[col] = formated_data
            if type(col) is int:
                self.df.iloc[col] = formated_data
            # self.table_dict[rowname][col]['font'] = (fontname, fontsize, fontstyle)
        self.draw_table()

    def row(self, row, data=None, format_=None, dec=2,  _isheader=False, fontname='arial', fontstyle='normal',
            fontsize=10):
        font = ('arial', 10, 'normal')

        if _isheader:
            range_start = 0
        else:
            range_start = self.df.index

        for col in range(range_start, self.df.column_count()):
            if data is not None:
                data = self.df.validate_data('row', data)
                label_text = data[col]  # grab label text from provided data set
            else:
                rowname = 'row' + str(row)
                label_text = self.df.table_dict[rowname]['text'][col]  # otherwise grab existing label text

            # format accordingly
            if format_ is not None:
                if 'float' in format_:
                    fc = '{0:.' + str(dec) + 'f}'
                    label_text = fc.format(float(label_text))
                if '$' in format_:
                    print(label_text)
                    fc = '${0:.' + str(dec) + 'f}'
                    label_text = fc.format(float(label_text))
                    print(label_text)
                if 'int' in format_:
                    non_decimal = re.compile(r'[^\d.]+')  # regex to strip off non number info
                    label_text = non_decimal.sub('', label_text)
                    label_text = int(label_text)

            # reassign text, etc to label
            rowname = 'row' + str(row)
            self.df.table_dict[rowname]['text'][col] = label_text
            # self.table_dict[rowname][col]['font'] = (fontname, fontsize, fontstyle)
        self.draw_table()

    def _apply_format(self, text, colrow, where, ordinal1, ordinal2, ordinal_prime, format_code, num_type):
        """apply formating to label text
        
            :param: text:str: string to be formateed
            :param: colrow:str: indicator for column or row to be formated, shoould be 'col' or 'row'
            :param: where:tuple: which data set to detrmine if formatting has been specified
            :param: ordinal1:int: column or row being evaluated
            :param: ordinal2:int: used in determienation of current row/colum evaluation so formatiing not applied 
                    to header and index labels
            :param: ordinal_prime:bool: used to determine if header or index, as nuber formatting is not applied to
                    header and index labels 
            :param: format_code:str, .format like: formatting to apply
            :param: num_type: class: converts text to number before applying format
        """
        result = text  # default if no conditions below are true
        non_decimal = re.compile(r'[^\d.]+')  # regex to strip off non number info
        text = non_decimal.sub('', text)  # strip off non numbers

        if colrow + str(ordinal1) in where:  # if the column or row, 'col1' -- 'row1', etc is in data set
            # ensure formatting not applied to header and index labels
            if (ordinal_prime and ordinal2 > 0) or (not ordinal_prime):
                result = format_code.format(num_type(text))  # apply formatting

        return result


class ListBoxController(tkinter.Listbox):
    """creates a list box with specified control elements and a scroll bar"""

    def __init__(self, window, row=0, column=0, sticky='nsew', buttons='+-c', duplicates=False, issorted=True,
                 widget_link=None):
        """ :param: window:tkinter.Frame type object to contain controller
            :param: row:int: row in `window` to add `self.frame`
            :param: col:int: column in `window` to add `self.frame`
            :param: sticky:str: for grid
            :param: buttons:str: buttons to add to controller, order of string indicates order of buttons
                    + : add 
                    - : delete
                    c : clear
            :param: duplicates:bool: True to allow duplicates in list
            :param: issorted:cool: True if list to be always sorted
            :param: widget_link:tkinter.widget: widget providing information to add to list, must have a .get()
            """
        self.frame = tkinter.Frame(window)
        self.frame.grid(row=row, column=column, sticky=sticky)

        super().__init__(self.frame)
        super().grid(row=0, column=0, sticky='nsew', columnspan=4)

        self.widget_link = widget_link

        self.duplicates = duplicates
        self.issorted = issorted

        self.img_list = []
        self._create_buttons(buttons)

    def clear(self):
        self.delete(0, tkinter.END)

    def list_items(self):
        return list(self.get(0, tkinter.END))

    def _create_buttons(self, but_type):
        col = 4
        for b in reversed(but_type):
            if b == '-':
                icon_name = 'minus'
                col -= 1
                command = self.delete_item
            elif b == '+':
                icon_name = 'plus'
                col -= 1
                command = self.add_item
            elif b == 'c':
                icon_name = 'clear'
                col -= 1
                command = self.clear
            else:
                return None

            img = icon(icon_name)
            self.img_list.append(img)
            but = tkinter.Button(self.frame, command=command, image=img)
            but.grid(row=1, column=col, sticky='nsew')

    def add_item(self):
        print(self.widget_link.get())
        listbox_items = self.list_items()
        if not self.duplicates:
            if self.widget_link.get() not in listbox_items:
                self.insert(tkinter.END, self.widget_link.get())
                listbox_items.append(self.widget_link.get())
        else:
            self.insert(tkinter.END, self.widget_link.get())
            listbox_items.append(self.widget_link.get())

        if self.issorted:
            self.clear()
            for f in sorted(listbox_items):
                self.insert(tkinter.END, f)

    def delete_item(self):
        pass


class ScrollFrame(tkinter.Canvas):
    """ creates a canvas with scroll bar
    
    Methods:
        __init__:
        onframeconfigure::
        scroll_frame: returns the frame on the canvas that is used to scroll, any widgets should be placed here
    
    http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame
    """

    def __init__(self, window):
        super().__init__(window)

        self.frame = tkinter.Frame(self)
        self.vsb = tkinter.Scrollbar(window, orient='vertical', command=self.yview)   # self.canvas.yview)

        self.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')

        self.create_window((4, 4), window=self.frame, anchor='nw')

        self.frame.bind('<Configure>', lambda event, canvas=self:  self.onframeconfigure())

    def onframeconfigure(self):
        """Reset the scroll region to encompass the inner frame"""
        self.configure(scrollregion=self.bbox("all"))

    def scroll_frame(self):
        return self.frame


class CreateToolTip(object):  # TODO not working, tooltip does not display on buttons, may only work on list boxes, etc
    """
    create a tooltip for a given widget
    link: http://stackoverflow.com/questions/3221956/what-is-the-simplest-way-to-make-tooltips-in-tkinter
    """
    def __init__(self, widget, text='widget info'):
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

if __name__ == '__main__':
    main = tkinter.Tk()

    main.mainloop()
