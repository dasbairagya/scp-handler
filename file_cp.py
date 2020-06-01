#!/usr/bin/python
# Dev: Gopal Dasbairagya
# 01 May,2020
# v.5.31
#test with nl/file/favicon.ico
try:
    import threading
    import json
    import os, sys
    from os import path
    from tkinter import *
    import tkinter as tk
    from tkinter import filedialog
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import askdirectory
    from tkinter import messagebox
    from tkinter import ttk
    import openpyxl
    import subprocess
    import time
except ImportError:
    print("Trying to Install required module: tk\n")
    os.system('python3 -m pip install tk')
    print("Trying to Install required module: subprocess\n")
    os.system('python3 -m pip install subprocess')
    print("Trying to Install required module: openpyxl\n")
    os.system('python3 -m pip install openpyxl ')
finally:
    import threading
    import json
    import os, sys
    from os import path
    from tkinter import *
    import tkinter as tk
    from tkinter import filedialog
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import askdirectory
    from tkinter import messagebox
    from tkinter import ttk
    from tkinter.ttk import *
    import openpyxl
    import subprocess
    import time


class Main:
    '''File handling class using scp'''

    def __init__(self, root):
        self.currdir = os.getcwd()
        self.root = root
        # self.icon = PhotoImage(file='sshsh.png')
        # self.root.iconphoto(False, self.icon)
        self.root.title("SCP Handler")
        self.root.geometry("700x340")
        self.bg_tab1 = "#999"
        self.bg_tab2 = "#ccc"
        self.local_path = ""
        self.remote_path = ""
        self.ssh = ''
        self.prefix = u"\u001b[33m"
        self.suffix = u"\u001b[0m"
        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # get dynamically current dir
        self.json_path = self.dir_path+'/ssh.json'
        path = '/app/web/sites'

        style = ttk.Style()
        style.theme_create("GDB", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] }},
            "TNotebook.Tab": {
                "configure": {"padding": [40, 5], "background": self.bg_tab1},
                "map": {"background": [("selected", self.bg_tab2)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use("GDB")
        menubar = Menu(self.root, cursor="hand2", fg="white", bg="gray")
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Reset", command=self.reset_all)
        # filemenu.add_command(label="Open", command=self.donothing)
        menubar.add_cascade(label="Setting", menu=filemenu)
        self.root.config(menu=menubar)

        tab_parent = ttk.Notebook(self.root, cursor="hand2")
        self.tab_parent = tab_parent
        tab_parent.pack(expand=1, fill='both')

        self.tab1 = self.add_tab(tab_parent)
        self.tab2 = self.add_tab(tab_parent)
        self.tab3 = self.add_tab(tab_parent)

        tab_parent.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        tab_parent.add(self.tab1, text="SCP")
        tab_parent.add(self.tab2, text="CONSOLE")
        tab_parent.add(self.tab3, text="SSH")


        # All Input Variables
        self.local_path = StringVar()
        self.remote_path = StringVar()
        self.country = StringVar()
        self.branch = StringVar()
        self.radio = IntVar()
        self.radio.set(1)

        self.remote_branch_= StringVar()
        self.remote_ssh_= StringVar()


        #WIDGETS FOR TAB ONE--------------------------------------------
        R1 = ttk.Radiobutton(self.tab1, text="Upload", variable=self.radio, value=1, cursor="hand2", command=self.select_radio)
        R1.grid(row=0, column=3, padx=15, sticky='w')

        R2 = ttk.Radiobutton(self.tab1, text="Download", variable=self.radio, value=2, cursor="hand2", command=self.select_radio)
        R2.grid(row=0, column=4, padx=15, sticky='w')

        label_branch = self.add_label(self.tab1, text="Branch:")
        label_branch.grid(row=0, column=0, padx=15, pady=15, sticky='w')

        self.field_branch = ttk.Combobox(self.tab1, textvariable=self.branch, state="readonly", width=28)
        #field_branch['values'] = ("Master", "Revamp", "Staging")#statically added values
        # dynamically add the values to the combobox from .json's brnch elem if exits the file else show no value added yet
        self.field_branch['values'] = self.get_all_branches()
        self.field_branch.current(0)
        # self.field_branch.bind('<<ComboboxSelected>>', (lambda _: self.get_ssh_by_branch(self.branch)))
        self.field_branch.grid(row=0, column=1, padx=15, pady=15, sticky='w')


        label_country = self.add_label(self.tab1, text="Country:")
        label_country.grid(row=1, column=0, padx=15, pady=15, sticky='w')

        field_country = ttk.Combobox(self.tab1, textvariable=self.country, state="readonly", width=28)
        field_country['values'] = (
        "default", "us", "uk", "be", "se", "ca", "nl", "it", "ch", "sg", "hk", "my", "de", "me", "au",
        "in", "cl", "es", "at", "fi", "hu", "mx", "nz", "fr", "ro", "si", "sk", "cz", "pl", "hr", "co",
        "br")
        field_country.bind('<<ComboboxSelected>>', self.modified)
        field_country.grid(row=1, column=1, padx=15, pady=15, sticky='w')


        label_local_path = self.add_label(self.tab1, text="Local Path:")
        label_local_path.grid(row=2, column=0, padx=15, pady=15, sticky='w')

        field_local_path = self.add_field(self.tab1, textvariable=self.local_path, width=30)
        field_local_path.grid(row=2, column=1, padx=15, pady=15, sticky='w')

        self.buttonBrowseFile = tk.Button(self.tab1, text='Browse File', command=self.browse_file, width=8, bg='#fff', bd=3, cursor="hand2")
        self.buttonBrowseFile.grid(row=2, column=3, padx=15, pady=15, sticky='w')

        buttonBrowseDir = tk.Button(self.tab1, text='Browse Folder', command=self.browse_dir, width=10, bg='#fff', bd=3, cursor="hand2")
        buttonBrowseDir.grid(row=2, column=4, padx=15, pady=15, sticky='w')

        label_remote_path = self.add_label(self.tab1, text="Remote Path:")
        label_remote_path.grid(row=3, column=0, padx=15, pady=15, sticky='w')

        field_remote_path = self.add_field(self.tab1, textvariable=self.remote_path, width=30, )
        field_remote_path.bind('<ButtonRelease-3>', (lambda _: self.callback(self.remote_path)))
        field_remote_path.grid(row=3, column=1, padx=15, pady=15, sticky='w')


        self.buttonUpload = tk.Button(self.tab1, text="Upload", width=10, bg='blue', fg='white', bd=4, cursor="hand2", relief=RAISED, command=self.upload)
        self.buttonUpload.grid(row=4, column=3, padx=15, pady=15, sticky='w')

        self.buttonDownload = tk.Button(self.tab1, text="Download", width=10, bg='green', fg='white', bd=4, cursor="tcross", relief=RAISED, state=DISABLED, command=self.download)
        self.buttonDownload.grid(row=4, column=4, padx=15, pady=15, sticky='w')




        #WIDGETS FOR TAB TWO--------------------------------------------
        scrollbar = Scrollbar(self.tab2)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.console = Text(self.tab2)
        self.console.pack(fill=BOTH, expand=1)
        self.console_log('Your actions gonna reflect here..')
        # for i in range(10):
        #     self.console.insert(END, f"This is an example line {i}\n")
        # attach textbox to scrollbar
        self.console.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.console.yview)

        # WIDGETS FOR TAB THREE--------------------------------------------
        label_remote_brnach_ = self.add_label(self.tab3, text="Branch:")
        label_remote_brnach_.grid(row=0, column=0, padx=15, pady=15, sticky='w')

        field_remote_brnach_ = self.add_field(self.tab3, textvariable=self.remote_branch_, width=30)
        field_remote_brnach_.grid(row=0, column=1, padx=15, pady=15, sticky='w')

        label_remote_ssh = self.add_label(self.tab3, text="SSH:")
        label_remote_ssh.grid(row=0, column=2, padx=15, pady=15, sticky='w')

        # field_remote_ssh = self.add_field(self.tab3, textvariable=self.remote_ssh_, width=30, )
        self.field_remote_ssh = Text(self.tab3, width=30, height=4)
        self.field_remote_ssh.grid(row=0, column=3, padx=15, pady=15, sticky='w')

        #TAB3 BUTTON FRAME------------------------------------------------------------

        btn_frame = Frame(self.tab3)
        btn_frame.place(x=10, y=80, width=400)


        #buttons will place in button frame
        btnAdd = tk.Button(btn_frame, text="Add", width=5, bg='green', fg='white', bd=4, cursor="hand2", relief=RAISED, command=self.add_ssh ).grid(row=4, column=0, padx=10, pady=10)
        btnUpdate = tk.Button(btn_frame, text="Update", width=5, bg='orange', fg='white', bd=4, cursor="hand2", relief=RAISED, command=self.update_ssh).grid(row=4, column=1, padx=10, pady=10)
        btnDelete = tk.Button(btn_frame, text="Delete", width=5, bg='red', fg='white', bd=4, cursor="hand2", relief=RAISED, command=self.delete_ssh).grid(row=4, column=2, padx=10, pady=10)
        btnClear = tk.Button(btn_frame, text="Clear", width=5, bg='gray', fg='white', bd=4, cursor="hand2", relief=RAISED, command=self.clear).grid(row=4, column=3, padx=10, pady=10)

        #TAB3 TABLE Frame -------------------------------------------------------------------------------------------------
        style = ttk.Style()
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.configure("Custom.Treeview.Heading",
                        background="gray", foreground="white", relief="flat")
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])
        table_frame = Frame(self.tab3, relief=RIDGE)
        table_frame.place(x=15, y=150, width=670, height=130)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.data_table = ttk.Treeview(table_frame, style="Custom.Treeview", column=("sl","branch", "ssh"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.data_table.xview)
        scroll_y.config(command=self.data_table.yview)
        self.data_table.heading('sl', text="Sl.")
        self.data_table.heading('branch', text="BRANCH")
        self.data_table.heading('ssh', text="SSH")
        self.data_table['show'] = 'headings'
        self.data_table.column("sl", width=10)
        self.data_table.column("branch", width=10)
        self.data_table.column("ssh", width=300)
        self.data_table.pack(fill=BOTH, expand=1, side=tk.TOP)
        self.data_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.data_table.tag_configure('odd', background='#E8E8E8')
        self.data_table.tag_configure('even', background='#DFDFDF')
        self.fetch_data()


        # ------------------------------------------------------------------
        country = self.country.get()
        if country == "":
            country = 'default'
        r_path = f'/app/web/sites/{country}/files/'
        field_remote_path.insert(0, r_path)

        self.maxValue = 120
        self.currentValue = 0
        self.max = 120
        self.step = tk.DoubleVar()
        self.step.set(0)

        #--------------------------------------------------------------------
    def reset_all(self):
        self.branch.set("")
        self.country.set("")
        self.local_path.set("")
        self.remote_path.set("")

    def get_all_branches(self):
        # print("all branches")
        branches = []
        if os.path.exists(self.json_path):
            # reading from json file
            with open(self.json_path, 'r') as openfile:
                data = json.load(openfile)

            length = len(data['auth'])
            if length > 0:
                for i in range(length):
                    branches.append(data['auth'][i]['branch'])
            else:
                msg='No elements found in ssh.json'
                messagebox.showerror(title="Error", message=msg)
                branches.append('--No branch found--')
                self.tab_parent.select(2)  # select the ssh tab if no branch added for the first time


        else:
            msg='Please add branch first!'
            messagebox.showerror(title="Error", message=msg)
            self.tab_parent.select(2) #select the ssh tab if no branch added for the first time
            branches.append('--No branch found--')

        return branches

    def get_ssh_by_branch(self, branch):
        '''dynamically get the ssh by branch form data['auth] if .json file exits else show info about not exits ssh.json'''
        if os.path.exists(self.json_path):

            with open(self.json_path, 'r') as data_file:
                data = json.load(data_file)

            # print(data['auth'])
            # get all the elements inside the data['auth'] e.g [{},{},{}, ...]
            for element in data['auth']:
                # print(element)
                if element['branch'] == branch:
                    # print(element['ssh'])
                    self.console_log("ssh : " + element['ssh'])
                    return element['ssh']

            #ststically declear as constant
            # switcher = { 'Revamp': self.REVAMP,
            #              'Master': self.MASTER,
            #              'Staging': self.STAGING
            #              }
            # default_br = self.REVAMP
            # return switcher.get(branch, default_br)

        else:
            self.console_log("ssh.json file not found!")
            messagebox.showerror(title='Error', message='ssh.json file not found!')
            return

    def add_ssh(self):
        '''store data in json format in ssh.json'''
        if self.remote_branch_.get() != "" and self.field_remote_ssh.get('1.0','end-1c') != "" :
            branch = self.remote_branch_.get()
            ssh = self.field_remote_ssh.get('1.0','end-1c')
            data = {}
            data['auth'] = []
            path = self.json_path
            #if path does reside
            if os.path.exists(path):
                # reading from json file
                with open(path, 'r') as openfile:
                    data = json.load(openfile)

                #prevent if branch exits !!
                for i in range(len(data['auth'])):
                    if branch == data['auth'][i]['branch']:
                        # print("Branch already exits!")
                        self.console_log("branch already exits!!")
                        messagebox.showerror(title='Error', message='Branch already exits!')
                        return

                #append new data with the fetched datas
                data['auth'].append({'branch': branch, 'ssh': ssh})
                #overwrite the file
                json_object = json.dumps(data, indent = 4)
                with open(path, 'w') as outfile:
                    outfile.write(json_object)

                # print("Data added!!")
                self.fetch_data()
                self.console_log("Branch added!!")
                messagebox.showinfo(title='Success', message='Branch added!!')
                # update the combobox value for branch in scp tab as well
                self.field_branch['values'] = self.get_all_branches()
                self.field_branch.current(0)

            else:
                #create the file for the first time
                data['auth'].append({'branch': branch, 'ssh': ssh})
                json_object = json.dumps(data, indent = 4)
                with open(path, 'w') as outfile:
                    outfile.write(json_object)

                self.fetch_data()
                self.console_log("Json data created!!")
                messagebox.showinfo(title='Success', message='Json data created!!')
                # print("Json data created!!")
                # update the combobox value for branch in scp tab as well
                self.field_branch['values'] = self.get_all_branches()
                self.field_branch.current(0)

        else:
            # print("Please provide the values ")
            self.console_log("Please provide the values")
            messagebox.showerror(title='Error', message='Please provide the values')

    def update_ssh(self):
        '''update data in json format in ssh.json'''
        # in order to fix newline in textarea output we should change END to end-1c; The -1c deletes 1 character, while -2c would mean delete two characters, and so on.
        if self.remote_branch_.get() != "" and self.field_remote_ssh.get('1.0','end-1c') != "" :
            branch = self.remote_branch_.get()
            ssh = self.field_remote_ssh.get('1.0',"end-1c")
            data = {}
            data['auth'] = []
            path = self.json_path
            #if path does reside
            if os.path.exists(path):
                # reading from json file
                with open(path, 'r') as openfile:
                    data = json.load(openfile)

                match_found = 0
                for i in range(len(data['auth'])):
                    if data['auth'][i]['branch'] == branch:
                        data['auth'][i]['ssh'] = ssh
                        match_found+=1

                if match_found==0:
                    self.console_log("Branch not found!!")
                    messagebox.showerror(title='Error', message='Branch not found!!')
                    return

                # overwrite the file
                json_object = json.dumps(data, indent=4)
                with open(path, 'w') as outfile:
                    outfile.write(json_object)
                self.fetch_data()
                self.console_log("ssh has been updated!!")
                messagebox.showinfo(title='Success', message='SSH has been updated!!')
                # update the combobox value for branch in scp tab as well
                self.field_branch['values'] = self.get_all_branches()
                self.field_branch.current(0)

            else:
                self.console_log("ssh.json file not found!")
                messagebox.showerror(title='Error', message='ssh.json file not found!')
                return

        else:
            # print("Please provide branch and ssh")
            self.console_log("Please provide branch and ssh")
            messagebox.showerror(title='Error', message='Please provide branch and ssh')

    def delete_ssh(self):
        '''delete element from json data in ssh.json and overwrite the file'''
        if self.remote_branch_.get()!="":
            branch = self.remote_branch_.get()
            ssh = self.field_remote_ssh.get('1.0', "end-2c")
            data = {}
            data['auth'] = []
            path = self.json_path
            response = self.alert()

            if response=='yes':
                #load the data from json
                with open(path, 'r') as data_file:
                    data = json.load(data_file)

                # print(data['auth'])
                #get all the elements inside the data['auth'] e.g [{},{},{}, ...]
                index = 0
                for element in data['auth']:
                    if branch==element['branch']:
                        # print(element['branch'])
                        return_value = data['auth'].pop(index)
                        # print('Return Value:', return_value)
                        # element.pop()
                    index+=1

                # print('Updated List:', data)

                # overwrite the file as multiline format
                json_object = json.dumps(data, indent=4)
                with open(path, 'w') as outfile:
                    outfile.write(json_object)

                # overwrite the file in single line format
                # with open(path, 'w') as data_file:
                #     data = json.dump(data, data_file)

                self.fetch_data()
                self.clear()
                #update the combobox value for branch in scp tab as well
                self.field_branch['values'] = self.get_all_branches()
                self.field_branch.current(0)

            else:
                pass
        else:
            messagebox.showerror("Error", "Please select a Branch!")

    def clear(self):
        self.remote_branch_.set("")
        self.field_remote_ssh.delete('1.0', END)

    def alert(self):
        MsgBox = messagebox.askquestion('Delete', 'Are you sure you want to delete the record', icon='warning')
        return MsgBox

    def fetch_data(self):
        '''retrieve data ssh.json and loop through the data table'''
        path = self.json_path
        # print(path)
        if not os.path.exists(path):
            return
        # reading from json file
        with open(path, 'r') as openfile:
            data = json.load(openfile)
        # print(data)
        # print(len(data['auth']))
        # print(data['auth'][0]['branch'])
        # print(data['auth'][0]['ssh'])
        self.data_table.delete(*self.data_table.get_children())
        for i in range(len(data['auth'])):
            if i % 2 == 0:
                self.data_table.insert('', END, values=(i+1, data['auth'][i]['branch'], data['auth'][i]['ssh']), tags="even")
            else:
                self.data_table.insert('', END, values=(i+1, data['auth'][i]['branch'], data['auth'][i]['ssh']), tags="odd")

    def get_cursor(self, ev):
        cursor_row = self.data_table.focus()
        if cursor_row:
            content = self.data_table.item(cursor_row)
            row = content['values']
            # print(row)
            self.remote_branch_.set(row[1])
            self.field_remote_ssh.delete("1.0", END)
            self.field_remote_ssh.insert(END, row[2])
        else:
            pass

    def callback(self, sv):
        print('Remote path: '+sv.get())
        self.console_log("Remote path : " + sv.get())

    def modified(self, e):
        # print('country and remote path changed!\n Right click on remote path to check')

        country = self.country.get()
        r_path = f'/app/web/sites/{country}/files/'
        self.remote_path.set(r_path)
        self.console_log("Remote path : "+r_path)

        # print('remote path: '+self.remote_path.get())

    def add_progbar(self):

        s = ttk.Style()
        s.configure("black.Horizontal.TProgressbar", background='green')
        self.progressbar = Progressbar(self.tab1, length=250, style='black.Horizontal.TProgressbar', mode="determinate")
        self.progressbar.grid(row=4, column=1, padx=15, pady=15, sticky='w')

        self.progressbar["value"] = self.currentValue
        self.progressbar["maximum"] = self.maxValue

    def progress(self, currentValue):
        self.progressbar["value"] = currentValue
        # print(currentValue)

    def start_progressbar(self):
        self.add_progbar()
        self.progressbar.start()

    def stop_progressbar(self):
        # self.progressbar.configure(value=self.maxValue)
        self.progress(self.maxValue)
        self.progressbar.update()
        self.progressbar.stop()

    def destroy_progressbar(self):
        self.progressbar.destroy()

    def add_tab(self, tab_parent):
        return ttk.Frame(tab_parent)

    def add_button(self, frame, text, cmd):
        return tk.Button(frame, text=text, command=cmd)

    def add_label(self, frame, text=None):
        return tk.Label(frame, text=text)

    def add_field(self, frame, textvariable, width=30):
        return tk.Entry(frame, textvariable=textvariable, width=width)

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "SCP":
            self.browse_file_btn_state = 'disable'

            # print("Scp tab selected")
        if tab_text == "CONSOLE":
            self.browse_file_btn_state =  'normal'
            # print("Console tab selected")

    def select_radio(self):
        #change the buttons status based on radio selection
        option = self.radio.get()
        # selection = "You selected the option " + str(self.radio.get())
        # print(selection)
        if option==2:
            self.buttonUpload.config(state=DISABLED, cursor='cross')
            self.buttonBrowseFile.config(state=DISABLED, cursor='cross')
            self.buttonDownload.config(state=NORMAL, cursor='hand2')
            self.console_log("-------------download-------------")
        else:
            self.buttonUpload.config(state=NORMAL, cursor='hand2')
            self.buttonBrowseFile.config(state=NORMAL, cursor='hand2')
            self.buttonDownload.config(state=DISABLED, cursor='cross')
            self.console_log("-------------upload---------------")


    def browse_file(self):
        try:
            file = askopenfilename(initialdir=self.currdir, title="Select file",
                                   filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg")))
            #print(file)
            if os.path.exists(file):
                self.source = file
                self.local_path.set(self.source)
                self.console_log('Local path: '+self.source)
                # print('Local Path: '+self.source)
            else:
                if self.local_path.get() is None:
                    messagebox.showerror(title='Error', message='Please choose a file')

        except:
            # print("No file choosen!")
            messagebox.showerror(title='Error', message='No file choosen!')
            # print(self.local_path.get())

    def browse_dir(self):
        try:
            file = askdirectory(initialdir=self.currdir, title='Please select a directory')

            if os.path.exists(file):
                self.source = file
                self.local_path.set(self.source)
                self.console_log('Local path: ' + self.source)
                # print('Local Path: '+self.source)
            else:
                if self.local_path.get()=="":
                    messagebox.showerror(title='Error', message='Please choose a folder')
                if self.local_path.get()!="" and os.path.isdir(self.local_path.get())==False:
                    messagebox.showerror(title='Error', message='current path is not a folder')

        except:
            # print("No folder choosen!")
            messagebox.showerror(title='Error', message='No folder choosen!')
            # print(self.local_path.get())

    def console_log(self, cmd):
        self.console.insert(END, f"{cmd}\n")

    def communicate(self):
        #IMC-VAR-Go-to-Market-Hub-Sales-Sheet.pdf
        # print('communicating start')
        (out, err) = self.proc.communicate() #todo: var out always retuns nothing, don't know why
        # print(f'[\nreturncode: {self.proc.returncode} \nerror: {err} \noutput: {out} \n]')

        if self.proc.returncode==0:
            time.sleep(1)
            messagebox.showinfo(title='Success', message="Process Complete!")
            self.console_log("Process Complete!\n----------------")
            self.destroy_progressbar()

        if err:
            time.sleep(1)
            self.console_log("Error " + err.strip())
            messagebox.showerror(title="Failed!", message=str(err))
            self.destroy_progressbar()

        # print('communicating end')

    def progress_bar(self):
        # print("polling start!")
        self.add_progbar()
        i = 1
        while self.proc.poll() is None:
            self.progress(i**2)
            time.sleep(1)
            self.progressbar.update()
            i += 1
        else:
            self.progress(self.maxValue)
            self.progressbar.update()
            time.sleep(1)
            # self.stop_progressbar()
            # print("polling end!")

        #destroy the progressbar
        # self.destroy_progressbar()

    def upload(self):
        source = self.local_path.get()
        destination = self.remote_path.get()
        country = self.country.get()
        branch = self.branch.get()
        ssh = self.get_ssh_by_branch(branch)
        if source and destination and country and branch is not None:
            self.console_log("source: "+source)
            self.console_log("destination: "+destination)

            response = messagebox.askyesno(title="Uploading", message="Continue Uploading?")
            if response==True:
                cmd = 'scp -r '+ source +' '+ ssh  + destination
                self.console_log("command: " + cmd)
                # return
                try:
                    # run command using subprocess
                    self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8', stderr=subprocess.PIPE, shell=True)  # shell=True is required for string command
                    self.console_log("Please wait..")
                    # run polling and communicating in separate threads to avoid root freezing
                    t1 = threading.Thread(target=self.progress_bar)
                    t2 = threading.Thread(target=self.communicate)# run
                    t1.start()
                    t2.start()

                except:
                    # popup error msg
                    messagebox.showerror(title="Failed!", message="Something went wrong!")

        else:
            messagebox.showerror(title="Field Value Missing..", message="All fields are required")


    def download(self):
        destination = self.local_path.get()
        source= self.remote_path.get()
        country = self.country.get()
        branch = self.branch.get()
        ssh = self.get_ssh_by_branch(branch)
        if source and destination and country and branch is not None:
            self.console_log("source: " + source)
            self.console_log("destination: " + destination)

            response = messagebox.askyesno(title="Downloading", message="Continue Downloading?")
            if response==True:
                cmd = 'scp -r '+ ssh + source +' '+destination
                self.console_log("command: " + cmd)
                # return
                try:
                    #run command using subprocess
                    self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='utf-8', stderr=subprocess.PIPE, shell=True)
                    self.console_log("Please wait..")
                    # run polling and communicating in separate threads to avoid root freezing
                    t1 = threading.Thread(target=self.progress_bar)
                    t2 = threading.Thread(target=self.communicate)  # ',' required for single arg
                    t1.start()
                    time.sleep(1)
                    t2.start()

                    # while t2.is_alive():
                    #     print('communicating..')
                    #     time.sleep(3)


                except:
                    # popup error msg
                    messagebox.showerror(title="Failed!", message="Something went wrong!")
        else:
            messagebox.showerror(title="Field Value Missing..", message="All fields are required")


if __name__ == '__main__':
    root = Tk()
    # root.grid_rowconfigure(0, weight=1)
    # root.grid_columnconfigure(0, weight=1)
    # root.resizable(0, 0)
    # img = PhotoImage(file='sshsh.png')
    # root.tk.call
    # root.iconbitmap('/home/gopal/PycharmProjects/App/tkinter/scp/favicon.ico')
    ob = Main(root)
    root.mainloop()
