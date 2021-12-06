from tkinter import *
import os
import pandas as pd
#import pandastable
#from pandastable import Table, TableModel

#get directory path
dir_path = os.getcwd()

#look at file we want
cyber_path = dir_path + '/cybersecurity_startup_companies.csv'
multi_national_path = dir_path + '/export_multinational_companies.csv'
#get csv file
cyber_csv = pd.read_csv(cyber_path)
multi_national_csv = pd.read_csv(multi_national_path, index_col=[0])

#company names list
cyber_startup_names = cyber_csv['Company Name'].tolist()
multi_national_names = multi_national_csv.index.unique().tolist()

#create tkinter frame and intitialize size
win = Tk()
win.geometry("700x550")
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
multi_national_names.sort()
update_search(multi_national_names)

#Get file path of pre-processed data 
path = os.getcwd()
path_to_scores = os.path.dirname(path) + '/Herzog_text_parsing/data'

#look at file we want
startup_scores_path = path_to_scores + '/startup_scores.csv'
comptability_scores_path = path_to_scores + '/mult_startup_scores.csv'
#get csv file
startup_scores_csv = pd.read_csv(startup_scores_path)
compatability_scores_csv = pd.read_csv(comptability_scores_path, index_col=[0])
text = None
multi_data = None
def search():
    global text
    global multi_data
    if text != None:
        text.destroy()
    if multi_data != None:
        multi_data.destroy()
    #get values selected from user
    selected_company = listbox.get(ANCHOR)
    selected_threshold = int(input_threshold.get())   
    #only get rows with scores over the threshold
    company_column = compatability_scores_csv[selected_company]
    only_above_threshold = company_column[company_column > selected_threshold]
    #use those to get cybercompanies
    #startup_scores = startup_scores_csv.iloc[only_above_threshold.index]
    scores = compatability_scores_csv.loc[only_above_threshold.index.tolist()]
    #sort by score
    #startup_scores.sort_values(by = 'SCORE', ascending = False, inplace = True)
    scores.sort_values(by = 'SCORE', ascending = False, inplace = True)

    #create frame for pandastable to allow it to be displayed using tkinter
    frame = Frame(win)
    frame.pack(fill='both', expand = True)

    #output top 10 companies or less if less than 10
    row_length = len(scores.index)
    print(row_length)
    if row_length == 0:
        text = Label(text = "Threshold too high, no matches")
        text.pack()
    elif row_length >= 10:
        scores = scores.head(10)
        multi_data = Label(text = multi_national_csv[[' Establishment Year: ', ' Company  Stage: ', 'Estimated  Employees: ', 'Estimated  Revenues', 'Raised  Funding: ', 'Company Tags', 'Location']].loc[selected_company].iloc[0].to_string())
        #print(multi_data)
        text = Label(text = scores[[selected_company, "SCORE"]].to_string())
        #print(scores[[selected_company, "SCORE"]].to_string())
        #pt = Table(frame, dataframe = startup_scores)
        #pt.show()
    else:
        scores = scores.head(row_length)
        #multi_data = Labelmulti_national_csv[[' Establishment Year: ', ' Company  Stage: ', 'Estimated  Employees: ', 'Estimated  Revenues', 'Raised  Funding: ', 'Company Tags', 'Location']].loc[selected_company].iloc[0].to_string()
        #print(multi_data)
        #print(new_table.loc[selected_company][['Name of Company',	'Establishment Year:','Company Stage:', 'Estimated Employees:',	'Estimated Revenues	Raised Funding:', 'Company Tags']].to_string())
        text = Label(text = scores[[selected_company, "SCORE"]].to_string()) #+ '\n' + multi_data)
        #print(scores[[selected_company, "SCORE"]].to_string())
       #pt = Table(frame, dataframe = startup_scores)
        #pt.show()
    text.pack()#.place(relx = 0.5, rely = 0.75, anchor = 'center')
    if multi_data != None:
        multi_data.pack()
    
    

    
    

    


    #print(listbox.get(ANCHOR))
button = Button(win, text = "search", command =search )
button.pack()

#

win.mainloop()
