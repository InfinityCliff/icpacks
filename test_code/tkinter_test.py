import tkinter
import ictkinter
import numpy as np
import pandas as pd
import time

main = tkinter.Tk()

ent = tkinter.Entry(main)
ent.grid(row=0, column=0, sticky='nsew')
# lbl = tkinter.Label(main)
# lbl.grid(row=0, column=0, sticky='nsew')
# lbl['text'] = 'test'
# lbl['font'] = ('arial', 24, 'bold')


#print('------------------------------------------')
#print('From dict:')


data_dict = {2014: ['00', '01', '02', '03'],
             2013: ['10', '11', '12', '13'],
             2012: ['20', '21', '22', '23'],
             2011: ['30', '31', '32', '33'],
             2010: ['40', '41', '42', '43'],
             2009: ['50.0', '51.0', '52.0', '53.0']}

table = ictkinter.TableFrame(main, row=4, data=data_dict, orient='index', columns=['Average', 'Min', 'Max', 'Count'])
print(table)
#print('-------------------------------------------------')
table.row(2014, [12, 12, 12, 12, 12, 12])
#table.i_row(2014, [13, 13, 13, 13, 13, 13])
table.column('Average', [10, 10, 10])
table.column_format('Average', format_='float', fontstyle='bold')
table.column_format('Min', format_='$')
table.column_format('Count', format_='int')

table.show()

table.row_format(2014, format_='float', fontstyle='bold')

table.header_format(fontstyle='bold', fontsize=12)
table.index_format(fontstyle='bold', fontsize=12)

table.show()

main.mainloop()

