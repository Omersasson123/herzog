from tkinter import *
import os
import pandas as pd

#get directory path
dir_path = os.getcwd()

#look at file we want
cyber_path = dir_path + '/cybersecurity_startup_companies.csv'
multi_national_path = dir_path + '/export_multinational_companies.csv'
#get csv file
cyber_csv = pd.read_csv(cyber_path)
multi_national_csv = pd.read_csv(multi_national_path)

#company names list
cyber_startup_names = cyber_csv['Company Name'].tolist()
multi_national_names = multi_national_csv['Name of Company'].tolist()

#create tkinter frame and intitialize size
win = Tk()
win.geometry("700x350")
'''
#set correct first companyshown
variable = StringVar(win)
variable.set(cyber_startup_names[0]) # default value

company_drop_down = OptionMenu(win, variable, *multi_national_names)
company_drop_down.pack()
'''
#drop down to decide threshold
threshold_list = [i for i in range(0, 101)]

input_threshold = StringVar(win)
input_threshold.set(0)

threshold_drop_down = OptionMenu(win, input_threshold, *threshold_list)
threshold_drop_down.pack()

#searchable drop down
def search(event):
    curr_search = event.widget.get()

    if curr_search == '':
        shown_list = multi_national_names
    else:
        shown_list = []
        for item in multi_national_names:
            if curr_search.lower() in item.lower():
                shown_list.append(item)
    update_search(shown_list) 
    
    
def update_search(shown_list):
    listbox.delete(0, 'end')

    for item in shown_list:
        listbox.insert('end', item)

entry = Entry(win)
entry.pack()
entry.bind('<KeyRelease>', search)

listbox = Listbox(win)
listbox.pack()
update_search(multi_national_names)

def print_selected():
    print(listbox.get(ANCHOR))
button = Button(win, text = "press", command =print_selected )
button.pack()

#

win.mainloop()
