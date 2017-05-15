"""
Module: tkinter_exp

Methods:
    icon: returns image for use in menu icons
    image_to_canvas: place graph image on canvas, and place canvas in subframe
    create_menu: creates a menu from the provided dict in the provided window
    create_sub_menu: returns sub menu to add to menu cascade
    clear_subframe: clears and recreates subframe
    populate_list_box: populates a list box in the GUI with the data provided
    add_price_data -----------------------may want to delete this as the table takes care of this

class:
    TableFrame: creates a Dataframe linked to a tkinter frame
    ListBoxController: creates a list box with specified control elements and a scroll bar
    ScrollFrame: creates a canvas with scroll bar
    CreateToolTip: create a tooltip for a given widget
"""

import tkinter
import os
from PIL import ImageTk, Image
import re
import numpy as np
import pandas as pd
import string_exp

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
    """creates a menu from the provided dict in the provided window

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


class TableFrame(pd.DataFrame):

    def __init__(self, window, data=None, index=None, columns=None, orient='columns',
                 row=0, column=0, sticky='nsew', columnspan=1,
                 bold=None, currency=None, float_=None, int_=None, blank='--'):
        """creates a Dataframe linked to a tkinter frame
        
            :param: window:tkinter.Frame|Labelframe: containter for TableFrame
            
            -- Dataframe parameters:
            :param: data:dict, list, of df: data to be put in TableFrame
            :param: index:list: row labels (df index)
            :param: column:list: columns labels (df columns)
            :param: orient:str: The "orientation" of the data. If the keys of the passed dict
                    should be the columns of the resulting DataFrame, pass 'columns'
                    (default). Otherwise if the keys should be rows, pass 'index'.
                    
            -- tkinter parameters:
            :param: row:int: row in window
            :param: column:int: column in window
            :param: sticky:str: tkinter.Frame resource
            :param: columnspan:int: columnspan in window
            
            -- formatting parameters:
            :param: bold:tuple: columns or rows to be bolded, 0 indexed with or without index/headers.
                    Designate by: ('col0, 'col2', 'row1')
            :param: currency: columns or rows to be formated as currency '$0.00', 0 indexed with or without 
                    index/headers.  Designate by: ('col0, 'col2', 'row1')
            :param: float_: columns or rows to be formated as float '0.00', 0 indexed with or without index/headers.
                    Designate by: ('col0, 'col2', 'row1') # TODO be able to set precision
            :param: int: columns or rows to be formated as int '0', 0 indexed with or without index/headers.
                    Designate by: ('col0, 'col2', 'row1')  # TODO not working, need to code
        Methods:
            TODO ADD-------------------------------
            
            
        Usage notes:
            - after createing or altering the datafrme, need to call <draw_table> to display changes in tkinter window
            - to change column data: 
                t3['Average'] = [12, 12, 12, 12, 12, 12]
                        is equivalent to
                t3.column('Average', [13, 13, 13, 13, 13, 13])
                        as self is derived from pd.DataFrame
                        
        =EXAMPLES============================================================================
                print('------------------------------------------')
                print('From composite lists:')
                
                data_lst = [['00', '01', '02', '03'],
                            ['10', '11', '12', '13'],
                            ['20', '21', '22', '23'],
                            ['30', '31', '32', '33'],
                            ['40', '41', '42', '43'],
                            ['50', '51', '52', '53']]
                
                t1 = tkinter_exp.TableFrame(main, row=2, data=data_lst,
                                            index=[2014, 2013, 2012, 2011, 2010, 2009],
                                            columns=['Average', 'Min', 'Max', 'Count'])
                t1.draw_table()
                
                print('------------------------------------------')
                print('From DataFrame:')
                
                data_array = np.array([np.arange(6)]*4).T
                data_df = pd.DataFrame(data_array)
                t2 = tkinter_exp.TableFrame(main, row=3, data=data_df,
                                            index=[2014, 2013, 2012, 2011, 2010, 2009],
                                            columns=['Average', 'Min', 'Max', 'Count'])
                t2.draw_table()
                
                print('------------------------------------------')
                print('From dict:')
                
                data_dict = {2014: ['00', '01', '02', '03'],
                             2013: ['10', '11', '12', '13'],
                             2012: ['20', '21', '22', '23'],
                             2011: ['30', '31', '32', '33'],
                             2010: ['40', '41', '42', '43'],
                             2009: ['50', '51', '52', '53']}
                t3 = tkinter_exp.TableFrame(main, row=4, data=data_dict, orient='index', columns=['Average', 'Min',
                                            'Max', 'Count'])
                t3.draw_table() 
                
        =RESULTS=============================================================================
                ------------------------------------------
                From composite lists:
                     Average Min Max Count
                2014      00  01  02    03
                2013      10  11  12    13
                2012      20  21  22    23
                2011      30  31  32    33
                2010      40  41  42    43
                2009      50  51  52    53
                ------------------------------------------
                From DataFrame:
                      Average  Min  Max  Count
                2014        0    0    0      0
                2013        1    1    1      1
                2012        2    2    2      2
                2011        3    3    3      3
                2010        4    4    4      4
                2009        5    5    5      5
                ------------------------------------------
                From dict:
                     Average Min Max Count
                2009      50  51  52    53
                2010      40  41  42    43
                2011      30  31  32    33
                2012      20  21  22    23
                2013      10  11  12    13
                2014      00  01  02    03     
        """
        if type(data) is pd.DataFrame:
            if index is None:
                index = data.index.values
            if columns is None:
                columns = data.columns
            super().__init__(data=data)
            self.rename(columns=dict(zip(data.columns, columns)), inplace=True)
            self.index = index
        elif type(data) is dict:
            df = pd.DataFrame.from_dict(data=data, orient=orient)
            super().__init__(data=df)
            self.rename(columns=dict(zip(df.columns, columns)), inplace=True)

        else:
            super().__init__(data=data, index=index, columns=columns)

        self._formattting = self._build_formatting()

        self.frame = tkinter.Frame(window)
        self.frame.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)

        self.visible_columns = True
        self.visible_index = True
        self.sub_frame = tkinter.Frame(self.frame)
        self.sub_frame.grid(row=0, column=0, sticky='nsew')
        self.blank_cell = blank

    def update(self, other, join='left', overwrite=True, filter_func=None, raise_conflict=False):
        super().update(other, join='left', overwrite=True, filter_func=None, raise_conflict=False)

    def update_data(self, new_data):
        """
        Replaces data in table, does not alter index or column labels
        
        Args:
            :param: new_data:df, dict, list: should have same shape as existing df, not including the index and columns            
        """
        # TODO add exception for shape of new data not matching existing data frame, or trim/expand to fit
        if type(new_data) == np.ndarray:
            new_data = pd.DataFrame(new_data)
        elif type(new_data) == dict:
            new_data = pd.DataFrame.from_dict(new_data)
        elif type(new_data) == pd.DataFrame:
            pass
        else:
            return

        new_data.set_index(self.index.values, inplace=True)
        new_data.columns = self.columns
        for column in self.columns:
            self[column] = new_data[column]

    def hide_index(self, val=True):
        # TODO develop usage
        """send true to hide index column, false to show"""
        self.visible_index = val

    def hide_columns(self, val=True):
        # TODO develop usage
        """send true to hide column labels, false to show"""
        self.visible_columns = val

    def default_col(self, rows):
        """ returns a list of blank 'rows' """
        return [self.blank_cell] * rows

    def add_label(self, row, col, text, fontstyle='normal'):
        """Adds label to subframe
        
        Args:
            :param: row:int: row in subframe 
            :param: col:int col in subframe
            :param: text:str: label text
            :param: fontstyle:str: label fontstyle
        """
        lbl = tkinter.Label(self.sub_frame, text=text, font=('arial', 10, fontstyle))
        lbl.grid(row=row, column=col, sticky='nsew')

        return lbl

    def _label_dict_from_df(self):
        label_dict = {}
        label_dict['index'] = {}
        label_dict['columns'] = {}

        col = 0 + self.visible_index
        for col_label in self.columns:
            row = 0 + self.visible_columns
            label_dict[col_label] = {}
            label_dict['columns'][col_label] = tkinter.Label(self.sub_frame, text=col_label)
            label_dict['columns'][col_label].grid(row=0, column=col, sticky='nsew')
            for index in self.index.values:
                label_dict['index'][row] = tkinter.Label(self.sub_frame, text=index)
                label_dict['index'][row].grid(row=row, column=0, sticky='nsew')
                text = self[col_label][index]
                label_dict[col_label][index] = tkinter.Label(self.sub_frame, text=text)
                label_dict[col_label][index].grid(row=row, column=col, sticky='nsew')
                row += 1
            col += 1

        return label_dict

    def draw_table(self):
        """Draws df on subframe"""
        self.sub_frame = clear_subframe(self.frame, self.sub_frame)

        labels_dict = self._label_dict_from_df()
        col = 0
        row = 1
        # add index to table
        if self.visible_index:
            # index_labels = list(self.index.tolist())
            font_dict = self._formattting['index']
            for item in list(self.index.tolist()):
                labels_dict['index'][row]['text'] = item
                labels_dict['index'][row]['font'] = (font_dict['fontname'], font_dict['fontsize'],
                                                     font_dict['fontstyle'])
                # self.add_label(row=row, col=col, text=item)
                row += 1
            col += 1

        # add headers to table
        header_labels = list(self)
        row = 0
        if self.visible_columns:
            font_dict = self._formattting['header']
            for col_label in header_labels:
                labels_dict['columns'][col_label]['font'] = (font_dict['fontname'], font_dict['fontsize'],
                                                             font_dict['fontstyle'])
                # self.add_label(row=row, col=col, text=col_label)
                col += 1


        col = 0 + self.visible_index
        for col_label in self.columns:
            # print('c', col)
            row = 0 + self.visible_columns
            for index in self.index.values:
                # print('r', row)
                # labels_dict[col_label][index]['text'] = self[col_label][index]
                # labels_dict[col_label][index].grid(row=row, column=col, sticky='nsew')
                if row == 0:
                    font_dict = self._formattting['header']
                elif col == 0:
                    font_dict = self._formattting['index']
                else:
                    font_dict = self._formattting[col_label][index]
                # print(labels_dict[col_label][index]['text'])
                labels_dict[col_label][index]['font'] = (font_dict['fontname'], font_dict['fontsize'],
                                                         font_dict['fontstyle'])
                row += 1
            col += 1

        self.frame.update()
        # print(self)

    def insert_row(self, row, value, sort=None):
        """inserts a row in the table at specified lcoation
        
        Args:
            :param: row:int: row position to insert (zero based)
            :param: value:list: row values to insert
            :param: sort:str: sort direction after insertion, default is None
        """
        self.loc[row] = value
        if sort is not None:
            if sort.upper() in ['F', 'FORWARD', 'YES']:
                ascending = True
            elif sort.upper() in ['R', 'REVERSE', 'REVERSED', 'BACKWARDS']:
                ascending = False
            self.sort_index(inplace=True, ascending=ascending)

    def insert(self, loc, column, value, allow_duplicates=False):
        # TODO may not need, can probably just use the inherited method
        """inserts a column in the table at specified location
        Args:
            :param:
            :param:
            :param:
            :param: 
            
        """
        super().insert(loc, column, value, allow_duplicates)
        # self.reindex()

    def _build_formatting(self):
        format_dict = {}
        for col_label in self.columns:
            format_dict[col_label] = {}
            for year in self.index.values:
                format_dict[col_label][year] = {'fontname': 'arial', 'fontsize': 10, 'fontstyle': 'normal'}
        format_dict['index'] = {'fontname': 'arial', 'fontsize': 10, 'fontstyle': 'normal'}
        format_dict['header'] = {'fontname': 'arial', 'fontsize': 10, 'fontstyle': 'normal'}
        return format_dict

    def column_format(self, col, format_='', dec=2,  fontname='arial', fontstyle='normal', fontsize=10):
        for index, value in self[col].iteritems():
            text = string_exp.format_text(dec, format_, value)
            self.loc[index, col] = text
            self._formattting[col][index] = {'fontname': fontname, 'fontsize': fontsize, 'fontstyle': fontstyle}

    def header_format(self, format_='', dec=2, fontname='arial', fontstyle='normal', fontsize=10):
        for header in self.columns:
            self.rename(columns={header: string_exp.format_text(dec, format_, header)})
            self._formattting['header'] = {'fontname': fontname, 'fontsize': fontsize, 'fontstyle': fontstyle}

    def row_format(self, row, format_='', dec=2, fontname='arial', fontstyle='normal', fontsize=10):
        for column in self.columns:
            text = self[column][row]
            self.loc[row, column] = string_exp.format_text(dec, format_, text)
            self._formattting[column][row] = {'fontname': fontname, 'fontsize': fontsize, 'fontstyle': fontstyle}

    def i_column(self, col, data):
        """
            t3['Average'] = [12, 12, 12, 12, 12, 12] is equivalent to
            t3.column('Average', [13, 13, 13, 13, 13, 13]), with exception as listed under data:
        :param col:int: column index
        :param data: data to replace in column, must be same length as number of rows, if data is longer then end of
                list will be truncated, if shorter blank items will be appended to end 
        :return: no return
        """
        while len(data) > len(self):
            del data[-1]
        while len(data) < len(self):
            data.append(self.blank_cell)

        self.iloc[:, col] = data

    def column(self, col, data):
        """
            t3['Average'] = [12, 12, 12, 12, 12, 12] is equivalent to
            t3.column('Average', [13, 13, 13, 13, 13, 13]), with exception as listed under data:
        :param col:str: column label
        :param data: data to replace in column, must be same length as number of rows, if data is longer then end of
                list will be truncated, if shorter blank items will be appended to end 
        :return: no return
        """
        while len(data) > len(self):
            del data[-1]
        while len(data) < len(self):
            data.append(self.blank_cell)

        self[col] = data

    def i_row(self, row, data):
        """
        
        :param row:int: row index
        :param data: data to replace in row, must be same length as number of columns, if data is longer then end of
                list will be truncated, if shorter blank items will be appended to end 
        :return: no return 
        """
        while len(data) > len(self.columns):
            del data[-1]
        while len(data) < len(self.columns):
            data.append(self.blank_cell)

        self.iloc[row] = data

    def row(self, row, data):
        """
        
        :param row:str: index label
        :param data: data to replace in row, must be same length as number of columns, if data is longer then end of
                list will be truncated, if shorter blank items will be appended to end 
        :return: no return 
        """
        while len(data) > len(self.columns):
            del data[-1]
        while len(data) < len(self.columns):
            data.append(self.blank_cell)

        self.loc[row] = data

    def row_rename(self):
        # TODO develop method
        pass

    def column_rename(self):
        # TODO develop method
        pass


class ListBoxController(tkinter.Listbox):
    """creates a list box with specified control buttons and a scroll bar"""

    def __init__(self, window, row=0, column=0, sticky='nsew', buttons='+-c', duplicates=False, issorted=True,
                 widget_link=None):
        """ 
            :param: window:tkinter.Frame type object to contain controller
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
