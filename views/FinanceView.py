import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import colorchooser
from tkinter import StringVar, OptionMenu
from tkinter import font
from tkinter import Tk, Canvas, Frame, Scrollbar, Label, Button, VERTICAL, RIGHT, LEFT, Y
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image, ImageTk, ImageOps, ImageStat
import os
import shutil


class FinanceView(Tk):
    def __init__(self):
        super().__init__()
        self.title('Finance Program')
        self.geometry('800x600+255+100')
        self.controller_root = None
        self.selected_picture_or_color = None

    def window_reg(self,message = ' '):
        self.message_label = ttk.Label(self, text=message, font=("Arial", 12))
        self.message_label.pack(pady=20)

        self.container_frame = Frame(self, width=400, height=450, bg="#D3D3D3")
        self.container_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.container_frame.grid_propagate(False)
        self.container_frame.columnconfigure(0, weight=1)

        self.name_label = ttk.Label(self.container_frame, text='Name', font=("Arial", 16), background="#D3D3D3")
        self.name_label.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        self.name_entry = ttk.Entry(self.container_frame,width=30,font=("Arial", 13))
        self.name_entry.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.gmail_label = ttk.Label(self.container_frame, text="Gmail", font=("Arial", 16), background="#D3D3D3")
        self.gmail_label.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.gmail_entry = ttk.Entry(self.container_frame,width=30,font=("Arial", 13))
        self.gmail_entry.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.password_label = ttk.Label(self.container_frame, text="Password", font=("Arial", 16), background="#D3D3D3")
        self.password_label.grid(row=4, column=0, pady=10, padx=20, sticky="n")
        self.password_entry = ttk.Entry(self.container_frame, show="*",width=30,font=("Arial", 13))
        self.password_entry.grid(row=5, column=0, pady=10, padx=20, sticky="n")

        self.password_repeat_label = ttk.Label(self.container_frame, text="Password repeat", font=("Arial", 16), background="#D3D3D3")
        self.password_repeat_label.grid(row=6, column=0, pady=10, padx=20, sticky="n")
        self.password_repeat_entry = ttk.Entry(self.container_frame, show="*",width=30,font=("Arial", 13))
        self.password_repeat_entry.grid(row=7, column=0, pady=10, padx=20, sticky="n")

        self.submit_button_reg = ttk.Button(self.container_frame, text="Registration",width=30)
        self.submit_button_reg.grid(row=8, column=0, pady=20, padx=20, sticky="n")

        self.submit_button_log = ttk.Button(self, text="Login",width=20)
        self.submit_button_log.place(x=750, y=10, anchor="ne")


    def window_log(self,message = ' '):
        self.message_label = ttk.Label(self, text=message, font=("Arial", 12))
        self.message_label.pack(pady=20)

        self.container_frame = Frame(self, bg="#D3D3D3")
        self.container_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.container_frame.columnconfigure(0, weight=1)

        self.gmail_label = ttk.Label(self.container_frame, text="Gmail", font=("Arial", 16), background="#D3D3D3")
        self.gmail_label.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        self.gmail_entry = ttk.Entry(self.container_frame,width=30,font=("Arial", 13))
        self.gmail_entry.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.password_label = ttk.Label(self.container_frame, text="Password", font=("Arial", 16), background="#D3D3D3")
        self.password_label.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.password_entry = ttk.Entry(self.container_frame, show="*",width=30,font=("Arial", 13))
        self.password_entry.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.submit_button_log = ttk.Button(self.container_frame, text="Login",width=30)
        self.submit_button_log.grid(row=4, column=0, pady=20, padx=20, sticky="n")


    def get_user_input_reg(self):
        name = self.name_entry.get()
        gmail = self.gmail_entry.get()
        password = self.password_entry.get()
        password_repeat = self.password_repeat_entry.get()
        return name, gmail, password, password_repeat


    def get_user_input_log(self):
        gmail = self.gmail_entry.get()
        password = self.password_entry.get()
        return gmail, password


    def clear_widgets(self):
        for widget in self.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()


    def set_controller(self, controller):
            self.controller_root = controller


    def load_icons(self, opened_window, on_click_callback=None):
        images_folder = r'C:\Finans_programm\images\icons'
        self.images = []
        self.photo_icons = []
        for filename in os.listdir(images_folder):
            if opened_window == 'window_transaction':
                if "bookWhite" in filename or "Black" in filename or 'xplus' in filename:
                    if "bookBlack" not in filename and "counteragentBlack" not in filename and "categoryBlack" not in filename and "subcategoryBlack" not in filename:
                        image_path = os.path.join(images_folder, filename)
                        self.canvas = Canvas(self.container_frame, bg='#D3D3D3', height=70, width=75)
                        self.canvas.pack(side='left')
                        image = Image.open(image_path)
                        photo_icon = ImageTk.PhotoImage(image)
                        self.images.append(image)  
                        self.photo_icons.append(photo_icon)  
                        self.canvas.create_image(40, 35, anchor='center', image=photo_icon)
                        if "bookWhite" not in filename:
                            if 'xplus' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.transaction_on_plus_click())
                            elif on_click_callback != None:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: on_click_callback(path))

            elif opened_window == 'window_cards':
                if "cardWhite" in filename or "Black" in filename or 'xplus' in filename:
                    if "cardBlack" not in filename and "counteragentBlack" not in filename and "categoryBlack" not in filename and "subcategoryBlack" not in filename:
                        image_path = os.path.join(images_folder, filename)
                        self.canvas = Canvas(self.container_frame, bg='#D3D3D3', height=70, width=75)
                        self.canvas.pack(side='left')
                        image = Image.open(image_path)
                        photo_icon = ImageTk.PhotoImage(image)
                        self.images.append(image)  
                        self.photo_icons.append(photo_icon)  
                        self.canvas.create_image(40, 35, anchor='center', image=photo_icon)
                        if "cardWhite" not in filename:
                            if 'xplus' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.card_on_plus_click())
                            elif on_click_callback is not None:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: on_click_callback(path))

            elif opened_window == 'window_dollar':
                if "dollarWhite" in filename or "Black" in filename or 'xplus' in filename:
                    if "dollarBlack" not in filename and "counteragentBlack" not in filename and "categoryBlack" not in filename and "subcategoryBlack" not in filename:
                        image_path = os.path.join(images_folder, filename)
                        self.canvas = Canvas(self.container_frame, bg='#D3D3D3', height=70, width=75)
                        self.canvas.pack(side='left')
                        image = Image.open(image_path)
                        photo_icon = ImageTk.PhotoImage(image)
                        self.images.append(image)  
                        self.photo_icons.append(photo_icon)  
                        self.canvas.create_image(40, 35, anchor='center', image=photo_icon)
                        if "dollarWhite" not in filename:
                            if 'xplus' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.window_dollar_on_plus_click())
                            elif on_click_callback != None:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: on_click_callback(path))

            elif opened_window == 'window_statistic':
                if "statisticWhite" in filename or "Black" in filename and 'xplus' not in filename:
                    if "statisticBlack" not in filename and "counteragentBlack" not in filename and "categoryBlack" not in filename and "subcategoryBlack" not in filename:
                        image_path = os.path.join(images_folder, filename)
                        self.canvas = Canvas(self.container_frame, bg='#D3D3D3', height=70, width=75)
                        self.canvas.pack(side='left')
                        image = Image.open(image_path)
                        photo_icon = ImageTk.PhotoImage(image)
                        self.images.append(image)  
                        self.photo_icons.append(photo_icon)  
                        self.canvas.create_image(40, 35, anchor='center', image=photo_icon)
                        if "statisticWhite" not in filename:
                            self.canvas.bind("<Button-1>", lambda event, path=image_path: on_click_callback(path))

            elif opened_window == 'window_counteragents':
                if "ucounterpartiesWhite" in filename or "Black" in filename and 'xplus' not in filename:
                    if "ucounterpartiesBlack" not in filename:
                        image_path = os.path.join(images_folder, filename)
                        self.canvas = Canvas(self.container_frame, bg='#D3D3D3', height=70, width=75)
                        self.canvas.pack(side='left')
                        image = Image.open(image_path).convert("RGBA")
                        photo_icon = ImageTk.PhotoImage(image)
                        self.images.append(image)  
                        self.photo_icons.append(photo_icon)  
                        self.canvas.create_image(40, 35, anchor='center', image=photo_icon)
                        if "ucounterpartiesWhite" not in filename:
                            self.canvas.bind("<Button-1>", lambda event, path=image_path: on_click_callback(path))
                            if 'counteragentBlack' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.window_add_counteragent())

                            if 'categoryBlack' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.window_add_category())

                            if 'subcategoryBlack' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.window_add_subcategory())


    def create_middle_window(self):
        self.new_window = Toplevel(self)
        self.new_window.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 400) // 2
        self.new_window.geometry(f"{700}x{400}+{x}+{y}")


    def create_fullscreen_window(self):
        self.new_window = Toplevel(self)
        self.new_window.grab_set()

        self.new_window.overrideredirect(True)  
        self.new_window.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        header = Frame(self.new_window, bg="#000000", height=20)
        header.pack(fill="x", side="top")

        close_button = Button(
            header, text="✕", command=self.refresh_cards,
            bg="#000000", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", borderwidth=0, padx=10, pady=2
        )
        close_button.pack(side="right", padx=5, pady=2)

        def on_enter(e):
            close_button.config(bg="red", fg="white")

        def on_leave(e):
            close_button.config(bg="#000000", fg="white")

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)


    def transaction_on_plus_click(self):
        self.create_middle_window()

        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        subcategory_list = self.controller_root.update_subcategory_list()

        option_typetransaction = ['Расход', 'Доход']
        option_cardchoise = self.controller_root.update_card_list()
        option_counterparty = [name for _, name in counterparty_list]

        def update_categories(*args):  
            selected_counterparty_name = self.selected_counterparty.get()
            selected_counterparty_id = None
            
            for counterparty in counterparty_list:
                if counterparty[1] == selected_counterparty_name:
                    selected_counterparty_id = counterparty[0]
                    break
            filtered_categories = [name for _, name, counterparty_id in category_list if counterparty_id == selected_counterparty_id]
            self.selected_categires.set("Выбор категории")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.selected_categires, category))

        self.label_counterparty = ttk.Label(self.new_window, width=30, text='Выбор контрагента', font=("Arial", 16))
        self.label_counterparty.grid(row=1, column=0, pady=0, padx=20, sticky="n")
        self.selected_counterparty = tk.StringVar(value='Выбор контрагента')
        self.counterparty_menu = ttk.OptionMenu(self.new_window, self.selected_counterparty, None, *option_counterparty)
        self.counterparty_menu.configure(style="Custom.TMenubutton")
        self.counterparty_menu.config(width=25)
        self.counterparty_menu.grid(row=2,column=0,padx=20,pady=0,sticky="w")

        self.selected_counterparty.trace("w", update_categories)

        def update_subcategories(*args):
            selected_categires_name = self.selected_categires.get()
            selected_categires_id = None
            
            for categorie in category_list:
                if categorie[1] == selected_categires_name:
                    selected_categires_id = categorie[0]
                    break
            filtered_subcategories = [name for _, name, categorie_id in subcategory_list if categorie_id == selected_categires_id]
            self.selected_subcategires.set("Выбор категории")  
            self.namesubcategorie_menu['menu'].delete(0, 'end')  
            for subcategories in filtered_subcategories:
                self.namesubcategorie_menu['menu'].add_command(label=subcategories, command=tk._setit(self.selected_subcategires, subcategories))

        self.label_namecategorie = ttk.Label(self.new_window, width=30, text='Название категории', font=("Arial", 16))
        self.label_namecategorie.grid(row=3, column=0, pady=0, padx=20, sticky="n")
        self.selected_categires = tk.StringVar(value="Выбор категории")
        self.namecategorie_menu = ttk.OptionMenu(self.new_window, self.selected_categires, None)
        self.namecategorie_menu.configure(style="Custom.TMenubutton")
        self.namecategorie_menu.config(width=25)
        self.namecategorie_menu.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.selected_categires.trace("w", update_subcategories)

        self.label_namesubcategorie = ttk.Label(self.new_window, width=30, text='Название подкатегории', font=("Arial", 16))
        self.label_namesubcategorie.grid(row=5, column=0, pady=0, padx=20, sticky="n")
        self.selected_subcategires = tk.StringVar(value="Выбор подкатегории")
        self.namesubcategorie_menu = ttk.OptionMenu(self.new_window, self.selected_subcategires, None)
        self.namesubcategorie_menu.configure(style="Custom.TMenubutton")
        self.namesubcategorie_menu.config(width=25)
        self.namesubcategorie_menu.grid(row=6, column=0, padx=20, pady=0, sticky="w")

        self.label_typetransaction = ttk.Label(self.new_window, width=30, text='Тип транзакции', font=("Arial", 16))
        self.label_typetransaction.grid(row=7, column=0, pady=0, padx=20, sticky="n")
        self.selected_type_transaction = tk.StringVar(value='Выбор типа транзакции')
        self.type_transaction_menu = ttk.OptionMenu(self.new_window, self.selected_type_transaction, None, *option_typetransaction)
        self.type_transaction_menu.configure(style="Custom.TMenubutton")
        self.type_transaction_menu.config(width=25)
        self.type_transaction_menu.grid(row=8, column=0, padx=20, pady=0, sticky="w")

        self.label_sumstransaction = ttk.Label(self.new_window, width=30, text='Сумма транзакции', font=("Arial", 16))
        self.label_sumstransaction.grid(row=9, column=0, pady=0, padx=20, sticky="n")
        self.sumstransaction_entry = ttk.Entry(self.new_window, width=27, font=("Arial", 13))
        self.sumstransaction_entry.grid(row=10, column=0, padx=20, pady=5, sticky="w")

        self.currency_label = ttk.Label(self.new_window, text="", font=("Arial", 13))
        self.currency_label.grid(row=10, column=0, pady=10, padx=(225, 0), sticky="w")

        def update_currency(*args):
            selected_card = self.selected_choisecard.get()
            self.currency = self.controller_root.update_card_currency(selected_card)
            if self.currency:
                self.currency_label.config(text=f" {self.currency}")
            else:
                self.currency_label.config(text="")

        self.label_choisecard = ttk.Label(self.new_window, width=30, text='Выбор карты', font=("Arial", 16))
        self.label_choisecard.grid(row=11, column=0, pady=0, padx=20, sticky="n")
        self.selected_choisecard = tk.StringVar(value='Выбор карты')
        self.choisecard_menu = ttk.OptionMenu(self.new_window, self.selected_choisecard, None, *option_cardchoise)
        self.choisecard_menu.configure(style="Custom.TMenubutton")
        self.choisecard_menu.config(width=25)
        self.choisecard_menu.grid(row=12, column=0, padx=20, pady=0, sticky="w")

        self.selected_choisecard.trace("w", update_currency)

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6, pady=0, padx=0, sticky="n")

        self.submit_button_card = ttk.Button(self.new_window, text="Добавить", width=30)
        self.submit_button_card.config(command=self.controller_root.add_transaction)
        self.submit_button_card.grid(row=13, column=0, pady=10, padx=20, sticky="n")


    def get_transaction_information(self):
        counteragent = self.selected_counterparty.get()
        category = self.selected_categires.get()
        subcategory = self.selected_subcategires.get()
        type_transaction = self.selected_type_transaction.get()  
        amount = self.sumstransaction_entry.get()
        choisecard_menu = self.selected_choisecard.get()  
        currency = self.currency
        date = self.selected_date()
        return counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date


    def card_on_plus_click(self):
        self.create_middle_window()

        self.label_namecard = ttk.Label(self.new_window, width=30, text='Название карты', font=("Arial", 16))
        self.label_namecard.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.name_card_entry = ttk.Entry(self.new_window, width=30, font=("Arial", 13))
        self.name_card_entry.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.label_typecard = ttk.Label(self.new_window, width=30, text='Тип карты', font=("Arial", 16))
        self.label_typecard.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        self.type_card_entry = ttk.Entry(self.new_window, width=30, font=("Arial", 13))
        self.type_card_entry.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.label_balancecard = ttk.Label(self.new_window, width=30, text='Баланс карты', font=("Arial", 16))
        self.label_balancecard.grid(row=5, column=0, pady=10, padx=20, sticky="n")
        self.balance_card_entry = ttk.Entry(self.new_window, width=30, font=("Arial", 13))
        self.balance_card_entry.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        options = ['UAH', 'EUR', 'USD']
        self.selected_currency = tk.StringVar(value="Выберите валюту")
        self.dropdown = ttk.OptionMenu(self.new_window, self.selected_currency, *options)
        self.dropdown.grid(row=6, column=0, pady=10, padx=(237.3, 0), sticky="w")

        self.submit_button_open_file = tk.Button(self.new_window, text='Выбор картинки', command=self.open_file)
        self.submit_button_open_file.grid(row=7, column=0, pady=5, padx=10, sticky="w")

        self.image_rgb = ImageTk.PhotoImage(file=r'C:\Finans_programm\images\image_buttom\rgb20.png')
        self.submit_buttom_color = ttk.Button(self.new_window, image=self.image_rgb, width=10, command=self.choose_color)
        self.submit_buttom_color.grid(row=7, column=0, pady=7, padx=110, sticky="w")

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6 ,pady=0, padx = 0,   sticky="n")

        self.submit_button_card = ttk.Button(self.new_window, text="Добавить", width=30)
        self.submit_button_card.config(command=self.controller_root.add_new_card)
        self.submit_button_card.grid(row=8, column=0, pady=10, padx=20, sticky="n")


    def get_add_card_information(self):
        name_card = self.name_card_entry.get()
        type_card = self.type_card_entry.get()
        balance_card = self.balance_card_entry.get()
        selected_currency = self.selected_currency.get()
        return name_card,type_card,balance_card,selected_currency,self.selected_picture_or_color,self.selected_date()


    def statistic_on_plus_click(self):
        self.create_middle_window()


    def window_dollar_on_plus_click(self):
        self.create_middle_window()


    def window_add_counteragent(self):
        self.create_middle_window()

        center_frame = tk.Frame(self.new_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_name = Label(center_frame, text="Имя контрагента", font=("Arial", 10))
        self.label_name.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.name_counterparty_entry = Entry(center_frame, font=("Arial", 10))
        self.name_counterparty_entry.grid(row=1, column=0, pady=5, padx=10)

        self.submit_button_add_counterparty = Button(center_frame, text="Добавить контрагента", font=("Arial", 10))
        self.submit_button_add_counterparty.config(command=self.controller_root.submit_data_add_counterparty)
        self.submit_button_add_counterparty.grid(row=2, column=0, pady=10)


    def window_add_category(self):
        self.create_middle_window()
        self.counterparty_list = self.controller_root.update_counterparty_list()
        self.counterparty_dict = {name: id for id, name in self.counterparty_list}
        counterparty_names = [name for _, name in self.counterparty_list]

        center_frame = tk.Frame(self.new_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_name = Label(center_frame, text="Имя категории", font=("Arial", 10))
        self.label_name.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.name_category_entry = Entry(center_frame, font=("Arial", 10))
        self.name_category_entry.grid(row=1, column=0, pady=5, padx=10)

        self.label_counterparty = Label(center_frame, text="Контрагент", font=("Arial", 10))
        self.label_counterparty.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        self.select_counterpart = tk.StringVar(value="Выбрать контрагента")
        self.counterparty_id_category_menu = ttk.OptionMenu(center_frame, self.select_counterpart, None, *counterparty_names)
        self.counterparty_id_category_menu.grid(row=3, column=0, pady=5, padx=10)

        self.submit_button_add_category = Button(center_frame, text="Добавить категорию", font=("Arial", 10))
        self.submit_button_add_category.config(command=self.controller_root.submit_data_add_category)
        self.submit_button_add_category.grid(row=4, column=0, pady=10)


    def window_add_subcategory(self):
        self.create_middle_window()
        self.category_for_subcategory = self.controller_root.update_category_for_subcategory()
        self.category_for_subcategory_dict = {name: id for id, name in self.category_for_subcategory}
        category_for_subcategory_names = [name for _, name in self.category_for_subcategory]

        center_frame = tk.Frame(self.new_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_name = Label(center_frame, text="Имя подкатегории", font=("Arial", 10))
        self.label_name.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.name_subcategory_entry = Entry(center_frame, font=("Arial", 10))
        self.name_subcategory_entry.grid(row=1, column=0, pady=5, padx=10)

        self.label_category = Label(center_frame, text="Категория", font=("Arial", 10))
        self.label_category.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        self.select_category = tk.StringVar(value="Выбрать категорию")
        self.category_id_subcategory_menu = ttk.OptionMenu(center_frame, self.select_category, None, *category_for_subcategory_names)
        self.category_id_subcategory_menu.grid(row=3, column=0, pady=5, padx=10)

        self.submit_button_add_subcategory = Button(center_frame, text="Добавить подкатегорию", font=("Arial", 10))
        self.submit_button_add_subcategory.config(command=self.controller_root.submit_data_add_subcategory)
        self.submit_button_add_subcategory.grid(row=4, column=0, pady=10)


    def get_counterparty_input(self):
        name = self.name_counterparty_entry.get()
        return name


    def get_category_input(self):
        name = self.name_category_entry.get()
        counterparty_name = self.select_counterpart.get()
        counterparty_id = self.counterparty_dict.get(counterparty_name)
        return name, counterparty_id


    def get_subcategory_input(self):
        name = self.name_subcategory_entry.get()
        category_name = self.select_category.get()
        category_id = self.category_for_subcategory_dict.get(category_name)
        return name,category_id


    def selected_date(self):
        selected_date = self.calendar.get_date()
        full_date = datetime.strptime(selected_date, "%m/%d/%y").date()
        return full_date


    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("Все файлы", "*.*"), ("Текстовые файлы", "*.txt"), ("Изображения", "*.png;*.jpg;*.jpeg"))
        )
        if file_path:
            selected_file = file_path
            try:
                os.mkdir('C://Finans_programm/images/background_card')
            except FileExistsError:
                pass

            destination_folder = 'C://Finans_programm/images/background_card'
            destination_path = os.path.join(destination_folder, os.path.basename(file_path))
            shutil.move(file_path, destination_path)
            print(f"Файл перемещен в: {destination_path}")
            self.selected_picture_or_color = destination_path
        else:
            print("Файл не выбран")


    def choose_color(self):
        color = colorchooser.askcolor(title='Choose color')[1]
        if color:
            self.selected_picture_or_color = color


    def format_balance(self, balance):
        return f"{balance:,.0f}".replace(",", ".")


    def format_date(self, date):
        try:
            if isinstance(date, datetime):
                return date.strftime("%d.%m.%Y")
            else:
                date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                return date_obj.strftime("%d.%m.%Y")
        except ValueError:
            return date 


    def get_inverse_color(self,image):
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        stat = ImageStat.Stat(image)
        r, g, b = stat.mean[:3]
        brightness = (r * 0.299 + g * 0.587 + b * 0.114) 
        return "black" if brightness > 127 else "white"


    def creater_window(self):
        self.state("zoomed")


    def apply_row_colors(self, tree):
        for index, item in enumerate(tree.get_children()):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            tree.item(item, tags=(tag,))
            values = tree.item(item, "values")
            transaction_type = values[3]  
            if transaction_type == "Доход":
                tree.item(item, tags=(tag, "income"))
            elif transaction_type == "Расход":
                tree.item(item, tags=(tag, "expense"))

        tree.tag_configure("evenrow", background="#f0f0f0")
        tree.tag_configure("oddrow", background="#ffffff")
        tree.tag_configure("income", foreground="green")
        tree.tag_configure("expense", foreground="red")


    def sort_column(self, tree, col, reverse):
        data_list = [(tree.set(child, col), child) for child in tree.get_children('')]
        for index, (val, child) in enumerate(data_list):
            try:
                data_list[index] = (float(val), child)
            except ValueError:
                pass
        data_list.sort(reverse=reverse, key=lambda x: x[0])
        for index, (_, child) in enumerate(data_list):
            tree.move(child, '', index)
        self.apply_row_colors(tree)
        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))


    def refresh_transaction(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.window_transaction()
        self.load_icons('window_transaction', self.controller_root.title_icons)


    def window_transaction(self):
        self.creater_window()

        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        self.table_frame = Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(self.table_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        columns = ("Название транзакции", "Категория", "Подкатегория", "Тип транзакции", "Сумма", "Тип валюты", "Карта", "Дата транзакции")

        tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", yscrollcommand=vsb.set)
        tree.pack(fill="both", expand=True)
        vsb.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_column(tree, c, False))
            tree.column(col, width=100)

        transactions = self.controller_root.update_transaction()

        for index, transaction in enumerate(transactions):
            background_tag = "evenrow" if index % 2 == 0 else "oddrow"
            tree.insert("", "end", values=transaction[1:], tags=(background_tag), iid=transaction[0])  


        def on_tree_select(event):
            selected_item = tree.focus()  
            if selected_item:
                transaction_id = selected_item  
                self.choice_edit_delete(transaction_id)
                self.who_window_transaction = 'main'

        tree.bind("<ButtonRelease-1>", on_tree_select)

        self.apply_row_colors(tree)
        tree.tag_configure("evenrow", background="#f0f0f0")
        tree.tag_configure("oddrow", background="#ffffff")


    def choice_edit_delete(self,transaction_id):
        self.create_middle_window()

        result = self.controller_root.submit_update_id_transaction(transaction_id)

        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        subcategory_list = self.controller_root.update_subcategory_list()

        option_typetransaction = ['Расход', 'Доход']
        option_cardchoise = self.controller_root.update_card_list()
        option_counterparty = [name for _, name in counterparty_list]
        self.selected_before_card = result[7]

        def update_categories(*args):  
            selected_counterparty_name = self.selected_counterparty.get()
            selected_counterparty_id = None
            
            for counterparty in counterparty_list:
                if counterparty[1] == selected_counterparty_name:
                    selected_counterparty_id = counterparty[0]
                    break
            filtered_categories = [name for _, name, counterparty_id in category_list if counterparty_id == selected_counterparty_id]
            self.selected_categires.set("Выбор категории")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.selected_categires, category))

        self.label_counterparty = ttk.Label(self.new_window, width=30, text='Выбор контрагента', font=("Arial", 16))
        self.label_counterparty.grid(row=1, column=0, pady=0, padx=20, sticky="n")
        self.selected_counterparty = tk.StringVar(value=result[1])
        self.counterparty_menu = ttk.OptionMenu(self.new_window, self.selected_counterparty, None, *option_counterparty)
        self.counterparty_menu.configure(style="Custom.TMenubutton")
        self.counterparty_menu.config(width=25)
        self.counterparty_menu.grid(row=2,column=0,padx=20,pady=0,sticky="w")

        self.selected_counterparty.trace("w", update_categories)

        def update_subcategories(*args):
            selected_categires_name = self.selected_categires.get()
            selected_categires_id = None
            
            for categorie in category_list:
                if categorie[1] == selected_categires_name:
                    selected_categires_id = categorie[0]
                    break
            filtered_subcategories = [name for _, name, categorie_id in subcategory_list if categorie_id == selected_categires_id]
            self.selected_subcategires.set("Выбор категории")  
            self.namesubcategorie_menu['menu'].delete(0, 'end')  
            for subcategories in filtered_subcategories:
                self.namesubcategorie_menu['menu'].add_command(label=subcategories, command=tk._setit(self.selected_subcategires, subcategories))

        self.label_namecategorie = ttk.Label(self.new_window, width=30, text='Название категории', font=("Arial", 16))
        self.label_namecategorie.grid(row=3, column=0, pady=0, padx=20, sticky="n")
        self.selected_categires = tk.StringVar(value=result[2])
        self.namecategorie_menu = ttk.OptionMenu(self.new_window, self.selected_categires, None)
        self.namecategorie_menu.configure(style="Custom.TMenubutton")
        self.namecategorie_menu.config(width=25)
        self.namecategorie_menu.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.selected_categires.trace("w", update_subcategories)

        self.label_namesubcategorie = ttk.Label(self.new_window, width=30, text='Название подкатегории', font=("Arial", 16))
        self.label_namesubcategorie.grid(row=5, column=0, pady=0, padx=20, sticky="n")
        self.selected_subcategires = tk.StringVar(value=result[3])
        self.namesubcategorie_menu = ttk.OptionMenu(self.new_window, self.selected_subcategires, None)
        self.namesubcategorie_menu.configure(style="Custom.TMenubutton")
        self.namesubcategorie_menu.config(width=25)
        self.namesubcategorie_menu.grid(row=6, column=0, padx=20, pady=0, sticky="w")

        self.label_typetransaction = ttk.Label(self.new_window, width=30, text='Тип транзакции', font=("Arial", 16))
        self.label_typetransaction.grid(row=7, column=0, pady=0, padx=20, sticky="n")
        self.selected_type_transaction = tk.StringVar(value=result[4])
        self.type_transaction_menu = ttk.OptionMenu(self.new_window, self.selected_type_transaction, None, *option_typetransaction)
        self.type_transaction_menu.configure(style="Custom.TMenubutton")
        self.type_transaction_menu.config(width=25)
        self.type_transaction_menu.grid(row=8, column=0, padx=20, pady=0, sticky="w")

        self.label_sumstransaction = ttk.Label(self.new_window, width=30, text='Сумма транзакции', font=("Arial", 16))
        self.label_sumstransaction.grid(row=9, column=0, pady=0, padx=20, sticky="n")
        self.sumstransaction_entry = ttk.Entry(self.new_window, width=27, font=("Arial", 13))
        self.sumstransaction_entry.insert(0,result[5])
        self.sumstransaction_entry.grid(row=10, column=0, padx=20, pady=5, sticky="w")

        self.currency_label = ttk.Label(self.new_window, text="", font=("Arial", 13))
        self.currency_label.grid(row=10, column=0, pady=10, padx=(225, 0), sticky="w")

        def update_currency(*args):
            selected_card = self.selected_choisecard.get()

            self.currency = self.controller_root.update_card_currency(selected_card)
            if self.currency:
                self.currency_label.config(text=f" {self.currency}")
            else:
                self.currency_label.config(text="")

        self.label_choisecard = ttk.Label(self.new_window, width=30, text='Выбор карты', font=("Arial", 16))
        self.label_choisecard.grid(row=11, column=0, pady=0, padx=20, sticky="n")
        self.selected_choisecard = tk.StringVar(value=result[7])
        self.choisecard_menu = ttk.OptionMenu(self.new_window, self.selected_choisecard, None, *option_cardchoise)
        self.choisecard_menu.configure(style="Custom.TMenubutton")
        self.choisecard_menu.config(width=25)
        self.choisecard_menu.grid(row=12, column=0, padx=20, pady=0, sticky="w")
    
        self.selected_choisecard.trace_add("write", update_currency)
        update_currency()

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6, pady=0, padx=0, sticky="n")

        self.buttom_edit = Button(self.new_window, text='Редактировать')
        self.buttom_edit.config(command=self.controller_root.submit_edit_transaction)
        self.buttom_edit.grid(row=13, column=0, padx=20, pady=0, sticky="w")

        self.buttom_delete = Button(self.new_window, text='Удалить')
        self.buttom_delete.config(command=lambda: self.controller_root.submit_delete_transaction(transaction_id))
        self.buttom_delete.grid(row=13, column=1, padx=20, pady=0, sticky="w")


    def edit_transaction(self):
        counteragent = self.selected_counterparty.get()
        category = self.selected_categires.get()
        subcategory = self.selected_subcategires.get()
        type_transaction = self.selected_type_transaction.get()  
        amount = self.sumstransaction_entry.get()
        choisecard_menu = self.selected_choisecard.get()  
        currency = self.currency
        date = self.selected_date()
        return counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, self.who_window_transaction, self.selected_before_card


    def delete_transaction(self):
        return self.who_window_transaction


    def on_card_click(self, card_id):
        self.controller_root.submit_update_personal_card_transaction(card_id) 


    def refresh_cards(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()

        self.window_cards(self.controller_root.get_select_card_all())
        self.load_icons('window_cards', self.controller_root.title_icons)


    def window_cards(self, cards):
        self.creater_window()

        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        cards_frame = Frame(self)
        cards_frame.pack(fill="both", expand=True)

        card_in_row = 3  
        for i in range(card_in_row):
            cards_frame.columnconfigure(i, weight=1)

        def create_transparent_overlay(size, alpha=120):
            overlay = Image.new("RGBA", size, (169, 169, 169, alpha))
            return ImageTk.PhotoImage(overlay)

        overlay_image = create_transparent_overlay((350, 180))

        for i, card in enumerate(cards):
            (card_id, name, type_pocket, type_currency,
            data_made, data_change, count_money, bg_color, bg_picture) = card

            if isinstance(data_made, str):
                data_made_dt = datetime.strptime(data_made, "%d-%m-%Y")
            else:
                data_made_dt = data_made

            date_now = datetime.now()

            card_frame = Frame(cards_frame, width=350, height=180, bg=bg_color)
            card_frame.card_id = card_id
            card_frame.bind("<Button-1>", lambda event, card_frame=card_frame: self.on_card_click(card_frame.card_id))
            card_frame.grid(row=i // card_in_row, column=i % card_in_row, padx=10, pady=10)

            canvas = Canvas(card_frame, width=350, height=180, bg=bg_color, bd=0, highlightthickness=0)
            canvas.place(relx=0, rely=0, anchor="nw")

            text_color = "white"

            if bg_picture:
                try:
                    image = Image.open(bg_picture)
                    target_size = (350, 180)
                    image = ImageOps.fit(image, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                    text_color = self.get_inverse_color(image)
                    background_image = ImageTk.PhotoImage(image)
                    canvas.create_image(0, 0, image=background_image, anchor="nw")
                    card_frame.image = background_image
                except Exception as e:
                    print(f"Error loading image: {e}")

            if name:
                canvas.create_text(20, 35, text=name, fill=text_color, font=("Arial", 12, "bold"), anchor="w")
            if data_made:
                formatted_date = data_made_dt.strftime("%d-%m-%Y")  
                canvas.create_text(20, 75, text=formatted_date, fill=text_color, font=("Arial", 10), anchor="w")
            if count_money:
                formatted_balance = self.format_balance(count_money) if count_money != 0 else "0"
                canvas.create_text(330, 160, text=f"{formatted_balance} {type_currency}", fill=text_color, font=("Arial", 10), anchor="e")

            if date_now > data_made_dt:
                canvas.create_image(0, 0, image=overlay_image, anchor="nw")
                card_frame.overlay_image = overlay_image

            canvas.bind("<Button-1>", lambda event, card_frame=card_frame: self.on_card_click(card_frame.card_id))


    def add_personal_transactoin(self,name_curryncy):
        self.create_middle_window()

        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        subcategory_list = self.controller_root.update_subcategory_list()

        option_typetransaction = ['Расход', 'Доход']
        option_cardchoise = name_curryncy[0][0]
        self.currency = name_curryncy[0][1]
        option_counterparty = [name for _, name in counterparty_list]
        def update_categories(*args):  
            selected_counterparty_name = self.selected_counterparty.get()
            selected_counterparty_id = None
            
            for counterparty in counterparty_list:
                if counterparty[1] == selected_counterparty_name:
                    selected_counterparty_id = counterparty[0]
                    break
            filtered_categories = [name for _, name, counterparty_id in category_list if counterparty_id == selected_counterparty_id]
            self.selected_categires.set("Выбор категории")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.selected_categires, category))

        self.label_counterparty = ttk.Label(self.new_window, width=30, text='Выбор контрагента', font=("Arial", 16))
        self.label_counterparty.grid(row=1, column=0, pady=0, padx=20, sticky="n")
        self.selected_counterparty = tk.StringVar(value='Выбор контрагента')
        self.counterparty_menu = ttk.OptionMenu(self.new_window, self.selected_counterparty, None, *option_counterparty)
        self.counterparty_menu.configure(style="Custom.TMenubutton")
        self.counterparty_menu.config(width=25)
        self.counterparty_menu.grid(row=2,column=0,padx=20,pady=0,sticky="w")

        self.selected_counterparty.trace("w", update_categories)

        def update_subcategories(*args):
            selected_categires_name = self.selected_categires.get()
            selected_categires_id = None
            for categorie in category_list:
                if categorie[1] == selected_categires_name:
                    selected_categires_id = categorie[0]
                    break
            filtered_subcategories = [name for _, name, categorie_id in subcategory_list if categorie_id == selected_categires_id]
            self.selected_subcategires.set("Выбор категории")  
            self.namesubcategorie_menu['menu'].delete(0, 'end')  
            for subcategories in filtered_subcategories:
                self.namesubcategorie_menu['menu'].add_command(label=subcategories, command=tk._setit(self.selected_subcategires, subcategories))

        self.label_namecategorie = ttk.Label(self.new_window, width=30, text='Название категории', font=("Arial", 16))
        self.label_namecategorie.grid(row=3, column=0, pady=0, padx=20, sticky="n")
        self.selected_categires = tk.StringVar(value="Выбор категории")
        self.namecategorie_menu = ttk.OptionMenu(self.new_window, self.selected_categires, None)
        self.namecategorie_menu.configure(style="Custom.TMenubutton")
        self.namecategorie_menu.config(width=25)
        self.namecategorie_menu.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.selected_categires.trace("w", update_subcategories)

        self.label_namesubcategorie = ttk.Label(self.new_window, width=30, text='Название подкатегории', font=("Arial", 16))
        self.label_namesubcategorie.grid(row=5, column=0, pady=0, padx=20, sticky="n")
        self.selected_subcategires = tk.StringVar(value="Выбор подкатегории")
        self.namesubcategorie_menu = ttk.OptionMenu(self.new_window, self.selected_subcategires, None)
        self.namesubcategorie_menu.configure(style="Custom.TMenubutton")
        self.namesubcategorie_menu.config(width=25)
        self.namesubcategorie_menu.grid(row=6, column=0, padx=20, pady=0, sticky="w")

        self.label_typetransaction = ttk.Label(self.new_window, width=30, text='Тип транзакции', font=("Arial", 16))
        self.label_typetransaction.grid(row=7, column=0, pady=0, padx=20, sticky="n")
        self.selected_type_transaction = tk.StringVar(value='Выбор типа транзакции')
        self.type_transaction_menu = ttk.OptionMenu(self.new_window, self.selected_type_transaction, None, *option_typetransaction)
        self.type_transaction_menu.configure(style="Custom.TMenubutton")
        self.type_transaction_menu.config(width=25)
        self.type_transaction_menu.grid(row=8, column=0, padx=20, pady=0, sticky="w")

        self.label_sumstransaction = ttk.Label(self.new_window, width=30, text='Сумма транзакции', font=("Arial", 16))
        self.label_sumstransaction.grid(row=9, column=0, pady=0, padx=20, sticky="n")
        self.sumstransaction_entry = ttk.Entry(self.new_window, width=27, font=("Arial", 13))
        self.sumstransaction_entry.grid(row=10, column=0, padx=20, pady=5, sticky="w")

        self.currency_label = ttk.Label(self.new_window, text=f"{self.currency}", font=("Arial", 13))
        self.currency_label.grid(row=10, column=0, pady=10, padx=(230, 0), sticky="w")

        self.label_choisecard = ttk.Label(self.new_window, width=30, text='Выбор карты', font=("Arial", 16))
        self.label_choisecard.grid(row=11, column=0, pady=0, padx=20, sticky="n")
        self.selected_choisecard = tk.StringVar(value='Выбор карты')
        self.choisecard_menu = ttk.OptionMenu(self.new_window, self.selected_choisecard, option_cardchoise)
        self.choisecard_menu.configure(style="Custom.TMenubutton")
        self.choisecard_menu.config(width=25)
        self.choisecard_menu.grid(row=12, column=0, padx=20, pady=0, sticky="w")

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6, pady=0, padx=0, sticky="n")

        self.submit_button_card = ttk.Button(self.new_window, text="Добавить", width=30)
        self.submit_button_card.config(command=self.controller_root.add_transaction_personal)
        self.submit_button_card.grid(row=13, column=0, pady=10, padx=20, sticky="n")


    def refresh_personal_transaction(self,tr_card):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.personal_transaction_card(tr_card)


    def personal_transaction_card(self, tr_card):
        self.create_fullscreen_window()

        self.container_frame = Frame(self.new_window, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        self.table_frame = Frame(self.new_window)
        self.table_frame.pack(fill="both", expand=False)
        card_name_currency = self.controller_root.update_card_name_currency()
        self.add_personal_transaction = Button(
            self.container_frame,
            text="+",
            command=lambda: self.add_personal_transactoin(card_name_currency)
        )
        self.add_personal_transaction.grid(column=0, columnspan=1, pady=2, sticky="e")

        vsb = ttk.Scrollbar(self.new_window, orient="vertical")
        vsb.pack(side="right", fill="y")

        columns = ("Название транзакции", "Категория", "Подкатегория", "Тип транзакции", "Сумма", "Тип валюты", "Карта", "Дата транзакции")

        self.tree = ttk.Treeview(
            self.new_window,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set
        )
        self.tree.pack(fill="both", expand=True)
        vsb.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_column(self.tree, c, False))
            self.tree.column(col, width=100)

        self.fill_treeview(tr_card)


        def on_tree_select(event):
            selected_item = self.tree.focus()  
            if selected_item:
                transaction_id = selected_item  
                self.choice_edit_delete(transaction_id)
                self.who_window_transaction = 'personal'

        self.tree.bind("<ButtonRelease-1>", on_tree_select)


        self.apply_row_colors(self.tree)
        self.tree.tag_configure("evenrow", background="#f2f2f2")
        self.tree.tag_configure("oddrow", background="#ffffff")

        self.new_window.protocol("WM_DELETE_WINDOW", self.controller_root.close_transaction_personal)


    def fill_treeview(self, tr_card):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, transaction in enumerate(tr_card):
            background_tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=transaction[1:], tags=(background_tag), iid=transaction[0])


    def window_dollars(self):
        self.creater_window()
        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")


    def window_statistic(self):
        self.creater_window()
        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")


    def window_counteragents(self):
        self.creater_window()
        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        list_counterparty = self.controller_root.update_counterparty_list()
        list_category = self.controller_root.update_category_list()
        list_subcategory = self.controller_root.update_subcategory_list()
        

        categories_by_counterparty = {}
        for category in list_category:
            counterparty_id = category[2]
            if counterparty_id not in categories_by_counterparty:
                categories_by_counterparty[counterparty_id] = []
            categories_by_counterparty[counterparty_id].append(category)

        subcategories_by_category = {}
        for subcategory in list_subcategory:
            category_id = subcategory[2]
            if category_id not in subcategories_by_category:
                subcategories_by_category[category_id] = []
            subcategories_by_category[category_id].append(subcategory)


        self.tree_frame = Frame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)


        self.tree_frame.grid_rowconfigure(0, weight=1)  
        self.tree_frame.grid_columnconfigure(0, weight=1, uniform="columns")  
        self.tree_frame.grid_columnconfigure(1, weight=1, uniform="columns") 
        self.tree_frame.grid_columnconfigure(2, weight=2, uniform="columns")  

        self.left_column = Frame(self.tree_frame)
        self.left_column.grid(row=0, column=0, sticky="nsew")

        self.right_column = Frame(self.tree_frame)
        self.right_column.grid(row=0, column=1, sticky="nsew")

        self.white_column = Frame(self.tree_frame, bg="white")
        self.white_column.grid(row=0, column=2, sticky="nsew")

        self.tree_left = ttk.Treeview(self.left_column)
        self.tree_left.pack(fill="both", expand=True)

        self.tree_right = ttk.Treeview(self.right_column)
        self.tree_right.pack(fill="both", expand=True)

        label = Label(self.white_column, bg="white")
        label.pack(fill="both", expand=True)


        left = True

        for counterparty_id, counterparty_name in list_counterparty:
            target_tree = self.tree_left if left else self.tree_right
            left = not left
            counterparty_node = target_tree.insert("", "end", text=f"{counterparty_name} ▶", values=counterparty_id, tags= "Контрагент", open=False)

            if counterparty_id in categories_by_counterparty:
                for category in categories_by_counterparty[counterparty_id]:
                    category_id, category_name = category[0], category[1]
                    category_node = target_tree.insert(counterparty_node, "end", text=f"{category_name} ▶", values=category_id, tags = "Категория", open=False)

                    if category_id in subcategories_by_category:
                        for subcategory in subcategories_by_category[category_id]:
                            subcategory_id, subcategory_name = subcategory[0], subcategory[1]
                            subcategory_node = target_tree.insert(category_node, "end", text=subcategory_name, values=subcategory_id, tags = "Подкатегория", open=False)



        self.tree_left.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.tree_left.bind("<<TreeviewOpen>>", lambda event: self.toggle_arrow(event, "▶", "▼", self.tree_left))
        self.tree_left.bind("<<TreeviewClose>>", lambda event: self.toggle_arrow(event, "▼", "▶", self.tree_left))
        self.tree_right.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.tree_right.bind("<<TreeviewOpen>>", lambda event: self.toggle_arrow(event, "▶", "▼", self.tree_right))
        self.tree_right.bind("<<TreeviewClose>>", lambda event: self.toggle_arrow(event, "▼", "▶", self.tree_right))


    def on_item_selected(self, event):
        tree = event.widget  
        selected_items = tree.selection()  
        if not selected_items:
            return

        selected_item = selected_items[0]  
        item = tree.item(selected_item)  
        item_text = item["text"]  
        item_id = item["values"][0]
        
        for widget in self.white_column.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(self.white_column, bg="white")
        header_frame.pack(fill="x", padx=10, pady=5)

        title_label = tk.Label(header_frame, text=f"Выбрано: {item_text}", font=("Arial", 14, "bold"), bg="white")
        title_label.pack()

        item_type = "Неизвестно"
        related_data = []

        if item_id:
            item_type = item['tags'][0]

            if item_type == "Контрагент":
                related_data = self.controller_root.get_counterpart_info(item_id)
            elif item_type == "Категория":
                related_data = self.controller_root.get_subcategories_by_category(item_id)

        type_label = tk.Label(header_frame, text=f"Тип: {item_type}", font=("Arial", 12), bg="white")
        type_label.pack()

        separator = tk.Frame(self.white_column, height=2, bg="gray")
        separator.pack(fill="x", padx=5, pady=5)

        bottom_frame = tk.Frame(self.white_column, bg="white")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)

        col1 = tk.Frame(bottom_frame, bg="white")
        col2 = tk.Frame(bottom_frame, bg="white")
        col3 = tk.Frame(bottom_frame, bg="white")

        col1.grid(row=0, column=0, sticky="nsew", padx=10)
        col2.grid(row=0, column=1, sticky="nsew", padx=10)
        col3.grid(row=0, column=2, sticky="nsew", padx=10)

        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        tk.Label(col1, font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(col2, font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(col3, font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w")

        edit_icon = PhotoImage(file="images/image_buttom/change.png")  
        delete_icon = PhotoImage(file="images/image_buttom/dustbin.png")  

        counteragent_data = (item_id, item_text[0:-2])

        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side="right")

        edit_button_counteragent = tk.Button(button_frame, image=edit_icon, command=lambda: self.edit_category_subcategory(counteragent_data))
        edit_button_counteragent.image = edit_icon  
        edit_button_counteragent.pack(side=TOP,anchor="ne")

        delete_button_counteragent = tk.Button(button_frame, image=delete_icon, command=lambda: self.delete_category_subcategory(counteragent_data))
        delete_button_counteragent.image = delete_icon  
        delete_button_counteragent.pack(side=TOP,anchor="ne")

        row_index = 1  

        if related_data:
            for i, data in enumerate(related_data):
                if i % 3 == 0:
                    target_col = col1
                elif i % 3 == 1:
                    target_col = col2
                else:
                    target_col = col3

                label = tk.Label(target_col, text=data[1], bg="white", font=("Arial", 12))
                label.grid(row=row_index, column=0, sticky="w", pady=5)

                edit_button = tk.Button(target_col, image=edit_icon, command=lambda data=data: self.edit_category_subcategory(data))
                edit_button.image = edit_icon  
                edit_button.grid(row=row_index, column=1, sticky="e", padx=5)

                delete_button = tk.Button(target_col, image=delete_icon, command=lambda data=data: self.delete_category_subcategory(data))
                delete_button.image = delete_icon  
                delete_button.grid(row=row_index, column=2, sticky="e", padx=5)

                row_index += 1 

        else:
            tk.Label(col1, text="Нет данных", bg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w")





    def edit_category_subcategory(self, data):
        print(f"Редактировать: {data}")



    def delete_category_subcategory(self, data):
        print(f"Удалить: {data}")




    def toggle_arrow(self, event, old_symbol, new_symbol, tree):
        item = tree.focus()
        text = tree.item(item, "text")
        if old_symbol in text:
            tree.item(item, text=text.replace(old_symbol, new_symbol))




"""
5.СДЕЛАТЬ УДАЛЕНИЕ КОНТР,КАТЕГОР,ПОДКАТЕГОР
6.СДЕЛАТЬ РЕДАКТИРОВАНИЕ КОНТР,КАТЕГОР,ПОДКАТЕГОР

"""



"""

ОСТАЛОСЬ ЧТО БЫ ПЕРЕЙТИ

Закончить удаление и редактирваоние категорий и подкатегорий
Добавить кнопку удаления и редактирования контрагента
ДОБАВИТЬ В добавление категории или подкатегории что бы подтягивало контрагента или категорию
Нормальное размещение кнопки добавления в ПЕРСОНАЛЬНЫЕ ТРАНЗАКЦИИ
УДАЛЕНИЕ КАРТЫ




"""


