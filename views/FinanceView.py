import tkinter as tk
from tkinter import (
    Tk, Canvas, Frame, Scrollbar, Label, Button,
    VERTICAL, RIGHT, LEFT, Y, X, BOTH,
    StringVar, OptionMenu,
    filedialog, messagebox, colorchooser, font
)
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import PIL.Image as PILImage
import PIL.ImageTk as PILImageTk
from PIL import ImageOps, ImageStat
import os
import shutil
import pandas as pd
import matplotlib
import matplotlib.dates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import requests
from bs4 import BeautifulSoup





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

        self.name_label = ttk.Label(self.container_frame, text='Імя', font=("Arial", 16), background="#D3D3D3")
        self.name_label.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        self.name_entry = ttk.Entry(self.container_frame,width=30,font=("Arial", 13))
        self.name_entry.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.gmail_label = ttk.Label(self.container_frame, text="Пошта", font=("Arial", 16), background="#D3D3D3")
        self.gmail_label.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.gmail_entry = ttk.Entry(self.container_frame,width=30,font=("Arial", 13))
        self.gmail_entry.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.password_label = ttk.Label(self.container_frame, text="Пароль", font=("Arial", 16), background="#D3D3D3")
        self.password_label.grid(row=4, column=0, pady=10, padx=20, sticky="n")
        self.password_entry = ttk.Entry(self.container_frame, show="*",width=30,font=("Arial", 13))
        self.password_entry.grid(row=5, column=0, pady=10, padx=20, sticky="n")

        self.password_repeat_label = ttk.Label(self.container_frame, text="Повторення пароля", font=("Arial", 16), background="#D3D3D3")
        self.password_repeat_label.grid(row=6, column=0, pady=10, padx=20, sticky="n")
        self.password_repeat_entry = ttk.Entry(self.container_frame, show="*",width=30,font=("Arial", 13))
        self.password_repeat_entry.grid(row=7, column=0, pady=10, padx=20, sticky="n")

        self.submit_button_reg = ttk.Button(self.container_frame, text="Реєстрація",width=30)
        self.submit_button_reg.grid(row=8, column=0, pady=20, padx=20, sticky="n")

        self.submit_button_log = ttk.Button(self, text="Вхід",width=20)
        self.submit_button_log.place(x=750, y=10, anchor="ne")


    def window_log(self,message = ' '):
        self.message_label = ttk.Label(self, text=message, font=("Arial", 12))
        self.message_label.pack(pady=20)

        self.container_frame = Frame(self, bg="#D3D3D3")
        self.container_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.container_frame.columnconfigure(0, weight=1)

        self.gmail_label = ttk.Label(self.container_frame, text="Пошта", font=("Arial", 16), background="#D3D3D3")
        self.gmail_label.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        self.gmail_entry = ttk.Entry(self.container_frame,width=30,font=("Arial", 13))
        self.gmail_entry.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.password_label = ttk.Label(self.container_frame, text="Пароль", font=("Arial", 16), background="#D3D3D3")
        self.password_label.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.password_entry = ttk.Entry(self.container_frame, show="*",width=30,font=("Arial", 13))
        self.password_entry.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.submit_button_log = ttk.Button(self.container_frame, text="Вхід",width=30)
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
                        image = PILImage.open(image_path)
                        photo_icon = PILImageTk.PhotoImage(image)
                        self.images.append(image)  
                        self.photo_icons.append(photo_icon)  
                        self.canvas.create_image(40, 35, anchor='center', image=photo_icon)
                        if "bookWhite" not in filename:
                            if 'xplus' in filename:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: self.window_add_transactions())
                            elif on_click_callback != None:
                                self.canvas.bind("<Button-1>", lambda event, path=image_path: on_click_callback(path))

            elif opened_window == 'window_cards':
                if "cardWhite" in filename or "Black" in filename or 'xplus' in filename:
                    if "cardBlack" not in filename and "counteragentBlack" not in filename and "categoryBlack" not in filename and "subcategoryBlack" not in filename:
                        image_path = os.path.join(images_folder, filename)
                        self.canvas = Canvas(self.container_frame, bg='#D3D3D3', height=70, width=75)
                        self.canvas.pack(side='left')
                        image = PILImage.open(image_path)
                        photo_icon = PILImageTk.PhotoImage(image)
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
                        image = PILImage.open(image_path)
                        photo_icon = PILImageTk.PhotoImage(image)
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
                        image = PILImage.open(image_path)
                        photo_icon = PILImageTk.PhotoImage(image)
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
                        image = PILImage.open(image_path).convert("RGBA")
                        photo_icon = PILImageTk.PhotoImage(image)
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
        self.new_window = tk.Toplevel(self)
        self.new_window.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 400) // 2
        self.new_window.geometry(f"{700}x{400}+{x}+{y}")


    def create_fullscreen_window(self):
        self.new_window = tk.Toplevel(self)
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


    def window_add_transactions(self):
        self.create_middle_window()

        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        subcategory_list = self.controller_root.update_subcategory_list()

        option_typetransaction = ['Витрата', 'Дохід']
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
            self.selected_categires.set("Вибір Категорії")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.selected_categires, category))

        self.label_counterparty = ttk.Label(self.new_window, width=30, text='Вибір Контрагента', font=("Arial", 16))
        self.label_counterparty.grid(row=1, column=0, pady=0, padx=20, sticky="n")
        self.selected_counterparty = tk.StringVar(value='Вибір Контрагента')
        self.counterparty_menu = ttk.OptionMenu(self.new_window, self.selected_counterparty, None, *option_counterparty)
        self.counterparty_menu.configure(style="Custom.TMenubutton")
        self.counterparty_menu.config(width=25)
        self.counterparty_menu.grid(row=2,column=0,padx=20,pady=0,sticky="w")

        self.selected_counterparty.trace("w", update_categories)

        def update_subcategories(*args):
            selected_counterparty_name = self.selected_counterparty.get()
            selected_categires_name = self.selected_categires.get()
            
            selected_counterparty_id = next((id for id, name in counterparty_list if name == selected_counterparty_name), None)
            selected_categires_id = next(
                (id for id, name, cp_id in category_list
                if name == selected_categires_name and cp_id == selected_counterparty_id),
                None
            )
            filtered_subcategories = [name for _, name, cat_id in subcategory_list if cat_id == selected_categires_id]
            
            self.selected_subcategires.set("Вибір Підкатегорії")
            self.namesubcategorie_menu['menu'].delete(0, 'end')
            for subcat in filtered_subcategories:
                self.namesubcategorie_menu['menu'].add_command(label=subcat, command=tk._setit(self.selected_subcategires, subcat))

        self.label_namecategorie = ttk.Label(self.new_window, width=30, text='Назва Категорії', font=("Arial", 16))
        self.label_namecategorie.grid(row=3, column=0, pady=0, padx=20, sticky="n")
        self.selected_categires = tk.StringVar(value="Вибір Категорії")
        self.namecategorie_menu = ttk.OptionMenu(self.new_window, self.selected_categires, None)
        self.namecategorie_menu.configure(style="Custom.TMenubutton")
        self.namecategorie_menu.config(width=25)
        self.namecategorie_menu.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.selected_categires.trace("w", update_subcategories)

        self.label_namesubcategorie = ttk.Label(self.new_window, width=30, text='Назва Підкатегорії', font=("Arial", 16))
        self.label_namesubcategorie.grid(row=5, column=0, pady=0, padx=20, sticky="n")
        self.selected_subcategires = tk.StringVar(value="Вибір Підкатегорії")
        self.namesubcategorie_menu = ttk.OptionMenu(self.new_window, self.selected_subcategires, None)
        self.namesubcategorie_menu.configure(style="Custom.TMenubutton")
        self.namesubcategorie_menu.config(width=25)
        self.namesubcategorie_menu.grid(row=6, column=0, padx=20, pady=0, sticky="w")

        self.label_typetransaction = ttk.Label(self.new_window, width=30, text='Тип транзакції', font=("Arial", 16))
        self.label_typetransaction.grid(row=7, column=0, pady=0, padx=20, sticky="n")
        self.selected_type_transaction = tk.StringVar(value='Вибір типу транзакції')
        self.type_transaction_menu = ttk.OptionMenu(self.new_window, self.selected_type_transaction, None, *option_typetransaction)
        self.type_transaction_menu.configure(style="Custom.TMenubutton")
        self.type_transaction_menu.config(width=25)
        self.type_transaction_menu.grid(row=8, column=0, padx=20, pady=0, sticky="w")

        self.label_sumstransaction = ttk.Label(self.new_window, width=30, text='Сума транзакції', font=("Arial", 16))
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

        self.label_choisecard = ttk.Label(self.new_window, width=30, text='Вибір картки', font=("Arial", 16))
        self.label_choisecard.grid(row=11, column=0, pady=0, padx=20, sticky="n")
        self.selected_choisecard = tk.StringVar(value='Вибір картки')
        self.choisecard_menu = ttk.OptionMenu(self.new_window, self.selected_choisecard, None, *option_cardchoise)
        self.choisecard_menu.configure(style="Custom.TMenubutton")
        self.choisecard_menu.config(width=25)
        self.choisecard_menu.grid(row=12, column=0, padx=20, pady=0, sticky="w")

        self.selected_choisecard.trace("w", update_currency)

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6, pady=0, padx=0, sticky="n")

        self.submit_button_card = ttk.Button(self.new_window, text="Додати", width=30)
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

        self.label_namecard = ttk.Label(self.new_window, width=30, text='Назва картки', font=("Arial", 16))
        self.label_namecard.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.name_card_entry = ttk.Entry(self.new_window, width=30, font=("Arial", 13))
        self.name_card_entry.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.label_typecard = ttk.Label(self.new_window, width=30, text='Тип картки', font=("Arial", 16))
        self.label_typecard.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        options = ['Debit','Kredit']
        self.selected_type = tk.StringVar(value="Виберіть тип картки")
        
        self.type_card_entry = tk.OptionMenu(self.new_window, self.selected_type, *options)
        self.type_card_entry.config(width=26, font=("Arial", 13)) 
        self.type_card_entry.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.label_balancecard = ttk.Label(self.new_window, width=30, text='Баланс картки', font=("Arial", 16))
        self.label_balancecard.grid(row=5, column=0, pady=10, padx=20, sticky="n")
        self.balance_card_entry = ttk.Entry(self.new_window, width=30, font=("Arial", 13))
        self.balance_card_entry.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        options = ['UAH', 'EUR', 'USD']
        self.selected_currency = tk.StringVar(value="Виберіть валюту")
        self.dropdown = ttk.OptionMenu(self.new_window, self.selected_currency, *options)
        self.dropdown.grid(row=6, column=0, pady=10, padx=(237.3, 0), sticky="w")

        self.submit_button_open_file = tk.Button(self.new_window, text='Вибір картинку', command=self.open_file)
        self.submit_button_open_file.grid(row=7, column=0, pady=5, padx=20, sticky="w")

        self.image_rgb = PILImageTk.PhotoImage(file=r'C:\Finans_programm\images\image_buttom\rgb20.png')
        self.submit_buttom_color = ttk.Button(self.new_window, image=self.image_rgb, width=10, command=self.choose_color)
        self.submit_buttom_color.grid(row=7, column=0, pady=7, padx=120, sticky="w")

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6 ,pady=0, padx = 0,   sticky="n")

        self.submit_button_card = ttk.Button(self.new_window, text="Додати", width=30)
        self.submit_button_card.config(command=self.add_card)
        self.submit_button_card.grid(row=8, column=0, pady=10, padx=20, sticky="n")


    def add_card(self):
        name_card = self.name_card_entry.get().strip()
        selected_type = self.selected_type.get()
        balance = self.balance_card_entry.get().strip()

        if not name_card or selected_type == "Виберіть тип картки" or not balance:
            messagebox.showerror("Помилка", "Будь ласка, заповніть усі обов'язкові поля.")
            return

        if not hasattr(self, 'selected_picture_or_color') or not self.selected_picture_or_color:
            messagebox.showerror("Помилка", "Будь ласка, виберіть зображення або колір для картки.")
            return

        existing_names = self.controller_root.get_user_card_names()
        if name_card in existing_names:
            messagebox.showerror("Помилка", "Карта з такою назвою вже існує!")
            return

        self.controller_root.add_new_card()

        messagebox.showinfo("Успіх", "Карта успішно додана!")


    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Виберіть файл",
            filetypes=(("Усі файли", "*.*"), ("Текстові файли", "*.txt"), ("Зображення", "*.png;*.jpg;*.jpeg")))
        if file_path:
            selected_file = file_path
            try:
                os.mkdir('C://Finans_programm/images/background_card')
            except FileExistsError:
                pass

            destination_folder = 'C://Finans_programm/images/background_card'
            destination_path = os.path.join(destination_folder, os.path.basename(file_path))
            shutil.move(file_path, destination_path)
            print(f"Файл переміщений у: {destination_path}")
            self.selected_picture_or_color = destination_path
        else:
            messagebox.showerror("Файл не вибраний")

    def choose_color(self):
        color = colorchooser.askcolor(title='Виберіть колір')[1]
        if color:
            self.selected_picture_or_color = color


    def get_add_card_information(self):
        name_card = self.name_card_entry.get()
        type_card = self.selected_type.get()  
        balance_card = self.balance_card_entry.get()
        selected_currency = self.selected_currency.get()
        data_made_dt = self.selected_date()  
        date_now = datetime.now().date()    
        status = True
        if date_now > data_made_dt:
            status = None 

        return name_card, type_card, balance_card, selected_currency, self.selected_picture_or_color, data_made_dt, status




    def window_add_counteragent(self):
        self.create_middle_window()

        center_frame = tk.Frame(self.new_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.label_name = Label(center_frame, text="Ім'я Контрагента", font=("Arial", 10))
        self.label_name.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.name_counterparty_entry = tk.Entry(center_frame, font=("Arial", 10))
        self.name_counterparty_entry.grid(row=1, column=0, pady=5, padx=10)

        self.submit_button_add_counterparty = Button(center_frame, text="Додати Контрагента", font=("Arial", 10))
        self.submit_button_add_counterparty.config(command=self.controller_root.submit_data_add_counterparty)
        self.submit_button_add_counterparty.grid(row=2, column=0, pady=10)


    def window_add_category(self):
        self.create_middle_window()
        self.counterparty_list = self.controller_root.update_counterparty_list()
        self.counterparty_dict = {name: id for id, name in self.counterparty_list}
        counterparty_names = [name for _, name in self.counterparty_list]

        center_frame = tk.Frame(self.new_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_name = Label(center_frame, text="Ім'я Категорії", font=("Arial", 10))
        self.label_name.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.name_category_entry = tk.Entry(center_frame, font=("Arial", 10))
        self.name_category_entry.grid(row=1, column=0, pady=5, padx=10)

        self.label_counterparty = Label(center_frame, text="Контрагент", font=("Arial", 10))
        self.label_counterparty.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        self.select_counterpart = tk.StringVar(value="Вибрати Контрагента")
        self.counterparty_id_category_menu = ttk.OptionMenu(center_frame, self.select_counterpart, None, *counterparty_names)
        self.counterparty_id_category_menu.grid(row=3, column=0, pady=5, padx=10)

        self.submit_button_add_category = Button(center_frame, text="Додати Категорію", font=("Arial", 10))
        self.submit_button_add_category.config(command=self.controller_root.submit_data_add_category)
        self.submit_button_add_category.grid(row=4, column=0, pady=10)


    def window_add_subcategory(self):
        self.create_middle_window()
        self.category_for_subcategory = self.controller_root.update_category_for_subcategory()
        self.category_for_subcategory_dict = {name: id for id, name in self.category_for_subcategory}
        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        option_counterparty = [name for _, name in counterparty_list]
        center_frame = tk.Frame(self.new_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")


        def update_categories(*args):  
            selected_counterparty_name = self.selected_counterparty.get()
            selected_counterparty_id = None
            
            for counterparty in counterparty_list:
                if counterparty[1] == selected_counterparty_name:
                    selected_counterparty_id = counterparty[0]
                    break
            filtered_categories = [name for _, name, counterparty_id in category_list if counterparty_id == selected_counterparty_id]
            self.select_category.set("Вибір Категорії")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.select_category, category))

        self.label_counterparty = ttk.Label(center_frame, width=20, text='Вибір Контрагента', font=("Arial", 10))
        self.label_counterparty.grid(row=0, column=0, pady=5, padx=10)
        self.selected_counterparty = tk.StringVar(value='Вибір Контрагента')
        self.counterparty_menu = ttk.OptionMenu(center_frame, self.selected_counterparty, None, *option_counterparty)
        self.counterparty_menu.grid(row=1, column=0, pady=5, padx=10)
        self.selected_counterparty.trace("w", update_categories)

        self.label_namecategorie = ttk.Label(center_frame, width=20, text='Назва Категорії', font=("Arial", 10))
        self.label_namecategorie.grid(row=2, column=0, pady=0, padx=20, sticky="n")
        self.select_category = tk.StringVar(value="Вибір Категорії")
        self.namecategorie_menu = ttk.OptionMenu(center_frame, self.select_category, None)
        self.namecategorie_menu.grid(row=3, column=0, pady=5, padx=10)

        self.label_name = Label(center_frame, width=20, text="Ім'я Підкатегорії", font=("Arial", 10))
        self.label_name.grid(row=4, column=0, pady=5, padx=10)
        self.name_subcategory_entry = tk.Entry(center_frame, font=("Arial", 10))
        self.name_subcategory_entry.grid(row=5, column=0, pady=5, padx=10)

        self.submit_button_add_subcategory = Button(center_frame, text="Додати подкатегорию", font=("Arial", 10))
        self.submit_button_add_subcategory.config(command=self.controller_root.submit_data_add_subcategory)
        self.submit_button_add_subcategory.grid(row=6, column=0, pady=10)


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


    def get_inverse_color(self, image):
        if image.mode != "RGB":
            image = image.convert("RGB")

        stat = ImageStat.Stat(image)
        r, g, b = stat.mean[:3]
        brightness = round(r * 0.299 + g * 0.587 + b * 0.114)

        return "black" if brightness > 127 else "white"


    def creater_window(self):
        self.state("zoomed")


    def apply_row_colors(self, tree):
        for index, item in enumerate(tree.get_children()):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            tree.item(item, tags=(tag,))
            values = tree.item(item, "values")
            transaction_type = values[3]  
            if transaction_type == "Дохід":
                tree.item(item, tags=(tag, "income"))
            elif transaction_type == "Витрата":
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


    def refresh_counteragents(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.window_counteragents()
        self.load_icons('window_counteragents', self.controller_root.title_icons)


    def refresh_cards(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()

        self.window_cards(self.controller_root.get_select_card_all())
        self.load_icons('window_cards', self.controller_root.title_icons)


    def refresh_dollar(self):
        all_frame = [f for f in self.children]
        for fname in all_frame:
            self.nametowidget(fname).destroy()
        self.window_dollars()
        self.load_icons('window_dollar', self.controller_root.title_icons)


    def refresh_personal_transaction(self,tr_card):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.personal_transaction_card(tr_card)


    def window_transaction(self):
        self.creater_window()

        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        self.table_frame = Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(self.table_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        columns = ("Назва транзакції", "Категорія", "Підкатегорія", "Тип транзакції", "Сума", "Тип валюти", "Карта", "Дата транзакції")

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

        def clear_tree_selection(event, tree_widget=tree):
            widget = event.widget
            try:
                if tree_widget.winfo_exists() and widget != tree_widget and not isinstance(widget, ttk.Treeview):
                    sel = tree_widget.selection()
                    if sel:
                        tree_widget.selection_remove(sel)
                    tree_widget.focus("")
            except tk.TclError:
                pass

        self.bind_all("<Button-1>", lambda e: clear_tree_selection(e, tree), add="+")



    def choice_edit_delete(self,transaction_id):
        self.create_middle_window()

        result = self.controller_root.submit_update_id_transaction(transaction_id)

        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        subcategory_list = self.controller_root.update_subcategory_list()

        option_typetransaction = ['Витрата', 'Дохід']
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
            self.selected_categires.set("Вибір Категорії")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.selected_categires, category))

        self.label_counterparty = ttk.Label(self.new_window, width=30, text='Вибір Контрагента', font=("Arial", 16))
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
            self.selected_subcategires.set("Вибір Підкатегорії")  
            self.namesubcategorie_menu['menu'].delete(0, 'end')  
            for subcategories in filtered_subcategories:
                self.namesubcategorie_menu['menu'].add_command(label=subcategories, command=tk._setit(self.selected_subcategires, subcategories))

        self.label_namecategorie = ttk.Label(self.new_window, width=30, text='Назва Категорії', font=("Arial", 16))
        self.label_namecategorie.grid(row=3, column=0, pady=0, padx=20, sticky="n")
        self.selected_categires = tk.StringVar(value=result[2])
        self.namecategorie_menu = ttk.OptionMenu(self.new_window, self.selected_categires, None)
        self.namecategorie_menu.configure(style="Custom.TMenubutton")
        self.namecategorie_menu.config(width=25)
        self.namecategorie_menu.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.selected_categires.trace("w", update_subcategories)

        self.label_namesubcategorie = ttk.Label(self.new_window, width=30, text='Назва Підкатегорії', font=("Arial", 16))
        self.label_namesubcategorie.grid(row=5, column=0, pady=0, padx=20, sticky="n")
        self.selected_subcategires = tk.StringVar(value=result[3])
        self.namesubcategorie_menu = ttk.OptionMenu(self.new_window, self.selected_subcategires, None)
        self.namesubcategorie_menu.configure(style="Custom.TMenubutton")
        self.namesubcategorie_menu.config(width=25)
        self.namesubcategorie_menu.grid(row=6, column=0, padx=20, pady=0, sticky="w")

        self.label_typetransaction = ttk.Label(self.new_window, width=30, text='Тип транзакції', font=("Arial", 16))
        self.label_typetransaction.grid(row=7, column=0, pady=0, padx=20, sticky="n")
        self.selected_type_transaction = tk.StringVar(value=result[4])
        self.type_transaction_menu = ttk.OptionMenu(self.new_window, self.selected_type_transaction, None, *option_typetransaction)
        self.type_transaction_menu.configure(style="Custom.TMenubutton")
        self.type_transaction_menu.config(width=25)
        self.type_transaction_menu.grid(row=8, column=0, padx=20, pady=0, sticky="w")

        self.label_sumstransaction = ttk.Label(self.new_window, width=30, text='Сума транзакції', font=("Arial", 16))
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

        self.label_choisecard = ttk.Label(self.new_window, width=30, text='Вибір картки', font=("Arial", 16))
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

        self.buttom_edit = Button(self.new_window, text='Редагувати')
        self.buttom_edit.config(command=self.controller_root.submit_edit_transaction)
        self.buttom_edit.grid(row=13, column=0, padx=20, pady=0, sticky="w")

        self.buttom_delete = Button(self.new_window, text='Видалити')
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


    def window_cards(self, cards):
        self.creater_window()

        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        scrollable_frame = Frame(self)
        scrollable_frame.pack(fill="both", expand=True)

        canvas = Canvas(scrollable_frame, borderwidth=0, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vsb.set)

        self.cards_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.cards_frame.bind("<Configure>", on_configure)

        card_in_row = 4
        for i in range(card_in_row):
            self.cards_frame.columnconfigure(i, weight=1)


        def create_transparent_overlay(size, alpha=120):
            overlay = PILImage.new("RGBA", size, (169, 169, 169, alpha))
            return PILImageTk.PhotoImage(overlay)

        overlay_image = create_transparent_overlay((380, 210))

        for i, card in enumerate(cards):
            (card_id, name, type_pocket, type_currency,
            data_made, data_change, count_money, bg_color, bg_picture, status) = card

            if isinstance(data_made, str):
                data_made_dt = datetime.strptime(data_made, "%d-%m-%Y")
            else:
                data_made_dt = data_made

            card_frame = Frame(self.cards_frame, width=380, height=210, bg=bg_color)
            card_frame.card_id = card_id
            card_frame.bind("<Button-1>", lambda event, card_frame=card_frame: self.on_card_click(card_frame.card_id))
            row = i // card_in_row
            col = i % card_in_row
            card_frame.grid(row=row, column=col, padx=50, pady=30, sticky="nsew")
            self.cards_frame.rowconfigure(row, weight=1)

            canvas_card = Canvas(card_frame, width=380, height=210, bg=bg_color, bd=0, highlightthickness=0)
            canvas_card.place(relx=0, rely=0, anchor="nw")

            text_color = "white"

            if bg_picture:
                try:
                    image = PILImage.open(bg_picture)
                    image = ImageOps.fit(image, (380, 210), method=PILImage.Resampling.LANCZOS, centering=(0.5, 0.5))
                    text_color = self.get_inverse_color(image)
                    background_image = PILImageTk.PhotoImage(image)
                    canvas_card.create_image(0, 0, image=background_image, anchor="nw")
                    card_frame.image = background_image
                except Exception as e:
                    messagebox.showerror("Помилка","Помилка завантаження зображення")

            if name:
                canvas_card.create_text(25, 35, text=name, fill=text_color, font=("Arial", 15, "bold"), anchor="w")
            if data_made:
                formatted_date = data_made_dt.strftime("%d-%m-%Y")
                canvas_card.create_text(25, 75, text=formatted_date, fill=text_color, font=("Arial", 13), anchor="w")
            if count_money:
                formatted_balance = self.format_balance(count_money) if count_money != 0 else "0"
                canvas_card.create_text(360, 190, text=f"{formatted_balance} {type_currency}", fill=text_color, font=("Arial", 13), anchor="e")

            if status is None:
                canvas_card.create_image(0, 0, image=overlay_image, anchor="nw")
                card_frame.overlay_image = overlay_image

            canvas_card.bind("<Button-1>", lambda event, c_id=card_id: self.on_card_click(c_id))


    def add_personal_transactoin(self,name_curryncy):
        self.create_middle_window()

        counterparty_list = self.controller_root.update_counterparty_list()
        category_list = self.controller_root.update_category_list()
        subcategory_list = self.controller_root.update_subcategory_list()

        option_typetransaction = ['Витрата', 'Дохід']
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
            self.selected_categires.set("Вибір Категорії")  
            self.namecategorie_menu['menu'].delete(0, 'end')  
            for category in filtered_categories:
                self.namecategorie_menu['menu'].add_command(label=category, command=tk._setit(self.selected_categires, category))

        self.label_counterparty = ttk.Label(self.new_window, width=30, text='Вибір Контрагента', font=("Arial", 16))
        self.label_counterparty.grid(row=1, column=0, pady=0, padx=20, sticky="n")
        self.selected_counterparty = tk.StringVar(value='Вибір Контрагента')
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
            self.selected_subcategires.set("Вибір Підкатегорії")  
            self.namesubcategorie_menu['menu'].delete(0, 'end')  
            for subcategories in filtered_subcategories:
                self.namesubcategorie_menu['menu'].add_command(label=subcategories, command=tk._setit(self.selected_subcategires, subcategories))

        self.label_namecategorie = ttk.Label(self.new_window, width=30, text='Назва Категорії', font=("Arial", 16))
        self.label_namecategorie.grid(row=3, column=0, pady=0, padx=20, sticky="n")
        self.selected_categires = tk.StringVar(value="Вибір Категорії")
        self.namecategorie_menu = ttk.OptionMenu(self.new_window, self.selected_categires, None)
        self.namecategorie_menu.configure(style="Custom.TMenubutton")
        self.namecategorie_menu.config(width=25)
        self.namecategorie_menu.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        self.selected_categires.trace("w", update_subcategories)

        self.label_namesubcategorie = ttk.Label(self.new_window, width=30, text='Назва Підкатегорії', font=("Arial", 16))
        self.label_namesubcategorie.grid(row=5, column=0, pady=0, padx=20, sticky="n")
        self.selected_subcategires = tk.StringVar(value="Вибір Підкатегорії")
        self.namesubcategorie_menu = ttk.OptionMenu(self.new_window, self.selected_subcategires, None)
        self.namesubcategorie_menu.configure(style="Custom.TMenubutton")
        self.namesubcategorie_menu.config(width=25)
        self.namesubcategorie_menu.grid(row=6, column=0, padx=20, pady=0, sticky="w")

        self.label_typetransaction = ttk.Label(self.new_window, width=30, text='Тип транзакції', font=("Arial", 16))
        self.label_typetransaction.grid(row=7, column=0, pady=0, padx=20, sticky="n")
        self.selected_type_transaction = tk.StringVar(value='Вибір типу транзакції')
        self.type_transaction_menu = ttk.OptionMenu(self.new_window, self.selected_type_transaction, None, *option_typetransaction)
        self.type_transaction_menu.configure(style="Custom.TMenubutton")
        self.type_transaction_menu.config(width=25)
        self.type_transaction_menu.grid(row=8, column=0, padx=20, pady=0, sticky="w")

        self.label_sumstransaction = ttk.Label(self.new_window, width=30, text='Сума транзакції', font=("Arial", 16))
        self.label_sumstransaction.grid(row=9, column=0, pady=0, padx=20, sticky="n")
        self.sumstransaction_entry = ttk.Entry(self.new_window, width=27, font=("Arial", 13))
        self.sumstransaction_entry.grid(row=10, column=0, padx=20, pady=5, sticky="w")

        self.currency_label = ttk.Label(self.new_window, text=f"{self.currency}", font=("Arial", 13))
        self.currency_label.grid(row=10, column=0, pady=10, padx=(230, 0), sticky="w")

        self.label_choisecard = ttk.Label(self.new_window, width=30, text='Вибір картки', font=("Arial", 16))
        self.label_choisecard.grid(row=11, column=0, pady=0, padx=20, sticky="n")
        self.selected_choisecard = tk.StringVar(value='Вибір картки')
        self.choisecard_menu = ttk.OptionMenu(self.new_window, self.selected_choisecard, option_cardchoise)
        self.choisecard_menu.configure(style="Custom.TMenubutton")
        self.choisecard_menu.config(width=25)
        self.choisecard_menu.grid(row=12, column=0, padx=20, pady=0, sticky="w")

        self.calendar = Calendar(self.new_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=2, column=1, rowspan=6, pady=0, padx=0, sticky="n")

        self.submit_button_card = ttk.Button(self.new_window, text="Додати", width=30)
        self.submit_button_card.config(command=self.controller_root.add_transaction_personal)
        self.submit_button_card.grid(row=13, column=0, pady=10, padx=20, sticky="n")



    def personal_transaction_card(self, tr_card):
        self.create_fullscreen_window()
        self.new_window.focus()  

        self.container_frame = Frame(self.new_window, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        self.table_frame = Frame(self.new_window)
        self.table_frame.pack(fill="both", expand=False)

        card_name_currency = self.controller_root.update_card_name_currency()

        add_tr_icon = PILImageTk.PhotoImage(file="images/icons_for_personal_card/xplus.png")  
        edit_delete_icon = PILImageTk.PhotoImage(file="images/icons_for_personal_card/settings.png")  

        self.edit_delete_button = tk.Button(
            self.container_frame,
            image=edit_delete_icon,
            command=lambda: self.controller_root.show_card_by_name(card_name_currency[0][0])
        )
        self.edit_delete_button.image = edit_delete_icon  
        self.edit_delete_button.grid(column=0, row=0, pady=2, padx=5, sticky="w")

        self.add_tr_button = tk.Button(
            self.container_frame,
            image=add_tr_icon,
            command=lambda: self.add_personal_transactoin(card_name_currency)
        )
        self.add_tr_button.image = add_tr_icon  
        self.add_tr_button.grid(column=1, row=0, pady=2, padx=5, sticky="w")

        vsb = ttk.Scrollbar(self.new_window, orient="vertical")
        vsb.pack(side="right", fill="y")

        columns = (
            "Назва транзакції", "Категорія", "Підкатегорія", "Тип транзакції",
            "Сума", "Тип валюти", "Карта", "Дата транзакції"
        )

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

        def clear_tree_selection(event, tree_widget=self.tree):
            widget = event.widget
            try:
                if tree_widget.winfo_exists() and widget != tree_widget and not isinstance(widget, ttk.Treeview):
                    sel = tree_widget.selection()
                    if sel:
                        tree_widget.selection_remove(sel)
                    tree_widget.focus("")
            except tk.TclError:
                pass

        self.new_window.bind("<Button-1>", lambda e: clear_tree_selection(e, self.tree), add="+")

        def on_close():
            try:
                self.new_window.unbind("<Button-1>")
            except Exception:
                pass
            self.new_window.destroy()

        self.new_window.protocol("WM_DELETE_WINDOW", on_close)


    def choice_edit_delete_card(self, card):
        if not card:
            self.create_middle_window()
            label = ttk.Label(self.new_window, width=30, text="Карта не знайдена", font=("Arial", 16))
            label.pack()
            return

        self.create_middle_window()

        (card_id, card_name, type_pocket, type_currency,
        data_made, data_change, count_money, bg_color, bg_picture, status) = card

        CARD_WIDTH = 420
        CARD_HEIGHT = 240

        card_frame = Frame(self.new_window, width=CARD_WIDTH, height=CARD_HEIGHT, bg=bg_color)
        card_frame.pack(padx=30, pady=10)

        canvas_card = Canvas(card_frame, width=CARD_WIDTH, height=CARD_HEIGHT, bg=bg_color, bd=0, highlightthickness=0)
        canvas_card.place(x=0, y=0)

        text_color = "white"
        entry_bg_color = bg_color

        if bg_picture:
            image = PILImage.open(bg_picture)
            if image.mode != "RGB":
                image = image.convert("RGB")

            image = ImageOps.fit(image, (CARD_WIDTH, CARD_HEIGHT), method=PILImage.Resampling.LANCZOS)
            stat = ImageStat.Stat(image)
            r, g, b = map(int, stat.mean[:3])
            entry_bg_color = f"#{r:02x}{g:02x}{b:02x}"
            brightness = r * 0.299 + g * 0.587 + b * 0.114
            text_color = "black" if brightness > 127 else "white"

            background_image = PILImageTk.PhotoImage(image)
            canvas_card.create_image(0, 0, image=background_image, anchor="nw")
            card_frame.image = background_image

        if status is None:
            overlay = PILImage.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (169, 169, 169, 100))
            overlay_img = PILImageTk.PhotoImage(overlay)
            canvas_card.create_image(0, 0, image=overlay_img, anchor="nw")
            card_frame.overlay = overlay_img

        entry_style = {
            "font": ("Arial", 14, "bold"),
            "fg": text_color,
            "bg": entry_bg_color,
            "bd": 0,
            "highlightthickness": 0,
            "insertbackground": text_color
        }

        def validate_date_input(event=None):
            content = entry_date.get()
            digits = ''.join(filter(str.isdigit, content))[:8]

            day = month = year = ''
            if len(digits) >= 2:
                day = digits[:2]
            elif len(digits) > 0:
                day = digits[:1]

            if len(digits) >= 4:
                month = digits[2:4]
            elif len(digits) > 2:
                month = digits[2:3]

            if month and not (1 <= int(month) <= 12):
                month = ''

            if len(digits) >= 5:
                year = digits[4:]

            formatted = day
            if month:
                formatted += '-' + month
            elif len(digits) > 2:
                formatted += '-'
            if year:
                formatted += '-' + year

            entry_date.delete(0, 'end')
            entry_date.insert(0, formatted)

            if len(digits) == 8 and month and day:
                try:
                    d, m, y = int(day), int(month), int(year)
                    datetime(y, m, d)  
                except ValueError:
                    try:
                        max_day = (datetime(y if m < 12 else y + 1, (m % 12) + 1, 1) - timedelta(days=1)).day
                        d = min(d, max_day)
                        corrected = f"{d:02}-{m:02}-{y:04}"
                        entry_date.delete(0, 'end')
                        entry_date.insert(0, corrected)
                    except:
                        pass  

        entry_name = PILImage(card_frame, **entry_style)
        entry_name.insert(0, card_name)
        entry_name.place(x=25, y=35, width=200)

        entry_date = PILImage(card_frame, **entry_style)
        formatted_date = data_made if isinstance(data_made, str) else data_made.strftime("%d-%m-%Y")
        entry_date.insert(0, formatted_date)
        entry_date.place(x=25, y=75, width=120)
        entry_date.bind("<KeyRelease>", validate_date_input)

        entry_money = tk.Entry(card_frame, **entry_style, justify="right")
        entry_money.insert(0, str(count_money))
        entry_money.place(x=330, y=210, width=100, anchor="e")

        currency_var = StringVar(value=type_currency)
        currency_menu = OptionMenu(card_frame, currency_var, "UAH", "EUR", "USD")
        currency_menu.config(font=("Arial", 10), bg=entry_bg_color, fg=text_color, highlightthickness=0)
        currency_menu["menu"].config(font=("Arial", 10))
        currency_menu.place(x=340, y=210, width=60, anchor="w")

        type_var = StringVar(value=type_pocket)
        type_menu = OptionMenu(card_frame,type_var, "Debit", "Kredit")
        type_menu.config(font=("Arial", 10), bg=entry_bg_color, fg=text_color, highlightthickness=0)
        type_menu["menu"].config(font=("Arial", 10))
        type_menu.place(x=280, y=35, width=120)

        button_frame = Frame(self.new_window, bg="#f0f0f0")
        button_frame.pack(pady=10)
        def validate_and_update():
            new_name = entry_name.get().strip()
            new_type = type_var.get().strip()
            new_currency = currency_var.get().strip()
            new_money = entry_money.get().strip()
            new_date = entry_date.get().strip()

            if not new_name or not new_money or not new_date:
                messagebox.showerror("Помилка", "Заповніть усі поля")
                return

            try:
                parsed_date = datetime.strptime(new_date, "%d-%m-%Y")
                formatted_date_for_db = parsed_date.strftime("%Y-%m-%d")
                float_money = float(new_money)
            except ValueError:
                messagebox.showerror("Помилка", "Невірний формат дати (ДД-ММ-РРРР)")
                return
            except Exception:
                messagebox.showerror("Помилка", "Неправильне значення")
                return

            if new_name != card_name:  
                if self.controller_root.is_card_name_exist(new_name):
                    messagebox.showerror("Помилка", "Карта з таким ім'ям вже існує")
                    return

            self.controller_root.try_edit_card(
                card_id, new_name, new_type, new_currency, float_money, formatted_date_for_db
            )

            messagebox.showinfo("Успіх", "Карта оновлена")
            self.new_window.destroy()

        edit_btn = Button(button_frame, text="Редагувати", command=validate_and_update, bg="#90EE90", font=("Arial", 10), width=20)
        edit_btn.pack(side="left", padx=10)

        delete_btn = Button(button_frame, text="Видалити", command=lambda card_id = card_id: self.controller_root.try_delete_card(card_id), bg="#FF7F7F", font=("Arial", 10), width=20)
        delete_btn.pack(side="right", padx=10)


    def fill_treeview(self, tr_card):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, transaction in enumerate(tr_card):
            background_tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=transaction[1:], tags=(background_tag), iid=transaction[0])


    def window_dollar_on_plus_click(self):
        self.create_middle_window()
        self.label_iso_currency = Label(self.new_window, text="Введіть ISO валюти", font=("Arial", 10))
        self.label_iso_currency.pack()

        self.entry_iso_currency_input = tk.Entry(self.new_window, font=("Arial", 10))
        self.entry_iso_currency_input.pack()

        self.submit_iso_currency = Button(
            self.new_window,
            text="Додати",
            font=("Arial", 10),
            command=lambda: self.handle_currency_submit()
        )
        self.submit_iso_currency.pack()


    def handle_currency_submit(self):
        value = self.entry_iso_currency_input.get()
        self.get_check_valid_currency(value)


    def get_check_valid_currency(self, entry_iso_currency):
        currency_value = self.controller_root.get_select_actualy_amount()
        base_currency = currency_value[1] 

        result = self.controller_root.tool_currency_parsing(entry_iso_currency, base_currency)

        if result is None:
            messagebox.showerror(
                'Помилка',
                f"Такого типу валюти не знайдено!: {entry_iso_currency}"
            )
            return

        added_currency, rate = result
        self.controller_root.submit_currency_parsing_left_panel(added_currency,rate)

        self.clear_widgets()
        self.refresh_dollar()


    def window_dollars(self):
        self.creater_window()
        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        currency_value = self.controller_root.get_select_actualy_amount()
        if not currency_value:
            messagebox.showerror("Помилка", "Не вдалося отримати основну валюту")
            return

        self.base_currency = currency_value[1]

        updated = self.controller_root.ensure_currencies_loaded()

        if not updated:
            messagebox.showwarning(
                "Немає інтернету",
                "Курси валют не оновлено.\n"
                "Використовуються збережені значення."
            )

        currencies = self.controller_root.get_currency_parsing_left_panel()
        main_frame = Frame(self, bg="#E0E0E0")
        main_frame.pack(fill=BOTH, expand=True)

        self.left_panel = Frame(main_frame, width=300, bg="#B1B1B1")
        self.left_panel.pack(side=LEFT, fill="y")

        for currency, rate in currencies.items():
            if currency == self.base_currency:
                continue

            row = Frame(self.left_panel, bg="#B1B1B1")
            row.pack(fill=X, padx=6, pady=6)

            Label(
                row,
                text=f"{currency} {rate}",
                bg="#B1B1B1",
                font=("Arial", 14, "bold"),
                anchor="w"
            ).pack(side=LEFT, fill=X, expand=True)

            Button(
                row,
                text="+",
                width=3,
                command=lambda key=currency: self.change_main_currency(key)
            ).pack(side=RIGHT)

            Frame(self.left_panel, bg="black", height=2).pack(fill=X)

        self.right_panel = Frame(main_frame, bg="#E0E0E0")
        self.right_panel.pack(side=LEFT, fill=BOTH, expand=True)

        self.active_currency_frame = Frame(self.right_panel, bg="#E0E0E0")
        self.active_currency_frame.pack(fill=X, padx=20, pady=10)

        self.draw_active_currency(self.base_currency)

        # ===== Панель управления графиком =====
        control_frame = Frame(self.right_panel, bg="#E0E0E0")
        control_frame.pack(fill=X, padx=20, pady=(5, 0))

        Label(control_frame, text="Валюта:", bg="#E0E0E0").pack(side=LEFT)

        available_currencies = [
            c for c in currencies.keys()
            if c != self.base_currency
        ]

        # если нет валют — просто не рисуем график
        if not available_currencies:
            Label(
                self.right_panel,
                text="Додайте іншу валюту для графіку",
                bg="#E0E0E0",
                fg="gray",
                font=("Arial", 12)
            ).pack(pady=20)
            return

        self.chart_currency_var = tk.StringVar(value=available_currencies[0])

        currency_box = ttk.Combobox(
            control_frame,
            values=available_currencies,
            textvariable=self.chart_currency_var,
            state="readonly",
            width=8
        )
        currency_box.pack(side=LEFT, padx=5)

        Label(control_frame, text="Днів:", bg="#E0E0E0").pack(side=LEFT)

        self.chart_days_var = tk.IntVar(value=30)

        days_box = ttk.Combobox(
            control_frame,
            values=[7, 14, 30, 90, 180, 365],
            textvariable=self.chart_days_var,
            state="readonly",
            width=6
        )
        days_box.pack(side=LEFT, padx=5)

        Label(control_frame, text="Колір:", bg="#E0E0E0").pack(side=LEFT)

        self.chart_color_var = tk.StringVar(value="red")

        color_box = ttk.Combobox(
            control_frame,
            values=["red", "blue", "green", "black", "orange"],
            textvariable=self.chart_color_var,
            state="readonly",
            width=8
        )
        color_box.pack(side=LEFT, padx=5)

        Button(
            control_frame,
            text="Показати",
            command=lambda: self.draw_currency_chart(
                self.chart_currency_var.get(),
                self.chart_days_var.get(),
                self.chart_color_var.get()
            )
        ).pack(side=LEFT, padx=10)


        # ===== Frame для графика =====
        self.chart_frame = Frame(self.right_panel, bg="#CFCFCF")
        self.chart_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.draw_currency_chart(
            self.chart_currency_var.get(),
            self.chart_days_var.get(),
            self.chart_color_var.get()
        )


        for currency in currencies:
            if currency != self.base_currency:
                self.draw_currency_chart(currency)
                break



    def change_main_currency(self, new_currency):
        self.controller_root.change_base_currency_and_recalculate(new_currency)
        self.refresh_dollar()



    def draw_active_currency(self, currency):
        Label(
            self.active_currency_frame,
            text=currency,
            bg="#E0E0E0",
            font=("Arial", 26, "bold"),
            anchor="e"
        ).pack(fill=X)

        Frame(
            self.active_currency_frame,
            bg="black",
            height=3
        ).pack(fill=X, pady=(5, 0))

        Label(
            self.active_currency_frame,
            text="Main currency",
            bg="#E0E0E0",
            fg="#555555",
            font=("Arial", 10),
            anchor="e"
        ).pack(fill=X)


    def draw_currency_chart(self, target_currency, days=30, color="red"):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        history = self.controller_root.fetch_currency_history(
            self.base_currency,
            target_currency,
            days
        )

        if not history:
            Label(
                self.chart_frame,
                text="Немає підключення до інтернету або даних",
                font=("Arial", 14, "bold"),
                fg="gray",
                bg="#CFCFCF"
            ).place(relx=0.5, rely=0.5, anchor="center")
            return

        dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in history]
        values = [v for _, v in history]

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(dates, values, color=color, linewidth=2, label="Курс")
        ax.scatter(dates, values, color=color, s=10)

        ax.set_title(f"{target_currency} / {self.base_currency}")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Курс")
        ax.grid(True, alpha=0.3)
        ax.legend()

        if days <= 14:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        elif days <= 30:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        elif days <= 90:
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        elif days <= 180:
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        else:  
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        fig.autofmt_xdate(rotation=30)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)




    def get_actual_currency(self,key,value):
        if key:
            self.controller_root.get_add_actual_currency(key,value)
            self.controller_root.change_main_currency(key)
            self.clear_widgets()
            self.refresh_dollar()


    def window_statistic(self):
        self.creater_window()
        self.container_frame = Frame(self, height=50, bg="#D3D3D3")
        self.container_frame.pack(fill="x")

        self.left_frame = Frame(self, width=300, height=900, bg="#B1B1B1")
        self.left_frame.pack(side=LEFT, fill="y")

        self.central_figure = Frame(self,bg="white")
        self.central_figure.pack(side=LEFT, fill="both", expand=True)

        self.right_frame = Frame(self, bg="white")
        self.right_frame.pack(side=RIGHT, fill="both", expand=True)

        def clear_central_figure():
            for widget in self.central_figure.winfo_children():
                widget.destroy()

        def clear_right_frame():
            for widget in self.right_frame.winfo_children():
                widget.destroy()

        def right_frame_widget():
            self.month_option_map = ["3 місяця", "6 місяців", "9 місяців", "12 місяців", "За весь час", "За поточний місяць", "За поточний рік", "За минулий рік"]
            option_month = self.month_option_map  

            option_cardchoise = ["Усі картки"] + self.controller_root.update_card_list()

            self.selected_choise_month_menu = tk.StringVar(value='За поточний місяць')
            self.choise_month_menu = ttk.OptionMenu(self.right_frame, self.selected_choise_month_menu, None, *option_month)
            self.choise_month_menu.configure(style="Custom.TMenubutton")
            self.choise_month_menu.config(width=15)
            self.choise_month_menu.pack(anchor="ne", padx=10, pady=5)

            self.selected_choisecard = tk.StringVar(value='Усі картки')
            self.choisecard_menu = ttk.OptionMenu(self.right_frame, self.selected_choisecard, None, *option_cardchoise)
            self.choisecard_menu.configure(style="Custom.TMenubutton")
            self.choisecard_menu.config(width=15)
            self.choisecard_menu.pack(anchor="ne", padx=10, pady=5)


        def show_profit_loss_schedule():
            clear_central_figure()
            result_transaction = self.controller_root.update_transaction()
            clear_right_frame()
            right_frame_widget()

            def get_selected_month():
                clear_central_figure()
                selected_option = self.selected_choise_month_menu.get()
                selected_card = self.selected_choisecard.get()

                columns = ["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                        "Сума", "Тип валюти", "Карта", "Дата транзакції"]

                df = pd.DataFrame(result_transaction, columns=columns)
                df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
                current_year = pd.Timestamp.now().year
                current_mont = pd.Timestamp.now().month

                month_mapping = {
                    "3 місяця": 3,
                    "6 місяців": 6,
                    "9 місяців": 9,
                    "12 місяців": 12
                }

                if selected_option == "За весь час":
                    grouping = "year"

                elif selected_option == "За поточний рік":
                    df = df[df["Дата транзакції"].dt.year == current_year]
                    grouping = "month"

                elif selected_option == "За поточний місяць":
                    df = df[df["Дата транзакції"].dt.month == current_mont]
                    grouping = "month"

                elif selected_option == "За минулий рік":
                    previous_year = current_year - 1
                    df = df[df["Дата транзакції"].dt.year == previous_year]
                    grouping = "month"

                elif selected_option in month_mapping:
                    months_offset = month_mapping[selected_option]
                    now = pd.Timestamp.now()

                    start_date = (now.replace(day=1) - pd.DateOffset(months=months_offset - 1)).replace(day=1)

                    end_date = now.replace(day=1) + pd.offsets.MonthEnd(0)

                    df = df[(df["Дата транзакції"] >= start_date) & (df["Дата транзакції"] <= end_date)]
                    grouping = "month"

                else:
                    messagebox.showerror('Помилка', f"Невірне значення місяця: {selected_option}")
                    clear_right_frame()
                    return

                if selected_card not in ("Усі картки", "Вибір картки"):
                    df = df[df["Карта"] == selected_card]

                if grouping == "year":
                    df["Рік"] = df["Дата транзакції"].dt.year
                    income = df[df["Тип транзакції"] == "Дохід"].groupby("Рік")["Сума"].sum()
                    expenses = df[df["Тип транзакції"] == "Витрата"].groupby("Рік")["Сума"].apply(lambda x: x.abs().sum())
                    x_labels = sorted(set(expenses.index).union(set(income.index)))
                    title = "Доходи та Витрати по роках"
                    xlabel = "Рік"
                    xtick_labels = [str(label) for label in x_labels]

                elif grouping == "month":
                    df["Рік"] = df["Дата транзакції"].dt.year
                    df["Місяць"] = df["Дата транзакції"].dt.month
                    group_cols = ["Рік", "Місяць"]
                    income = df[df["Тип транзакції"] == "Дохід"].groupby(group_cols)["Сума"].sum()
                    expenses = df[df["Тип транзакції"] == "Витрата"].groupby(group_cols)["Сума"].apply(lambda x: x.abs().sum())

                    x_labels = sorted(set(expenses.index).union(set(income.index)))
                    title = "Доходи та Витрати по місяцях"
                    xlabel = "Місяць"

                    month_names_uk = {
                        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень", 5: "Травень", 6: "Червень",
                        7: "Липень", 8: "Серпень", 9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
                    }
                    xtick_labels = [f"{month_names_uk.get(m, str(m))} {y}" for y, m in x_labels]

                x = range(len(x_labels))
                income_values = [income.get(label, 0) for label in x_labels]
                expense_values = [expenses.get(label, 0) for label in x_labels]

                fig = Figure(figsize=(10, 5), dpi=100)
                ax = fig.add_subplot(111)

                bar_width = 0.35
                ax.bar([i - bar_width / 2 for i in x], income_values, width=bar_width, color='green', label='Доходи')
                ax.bar([i + bar_width / 2 for i in x], expense_values, width=bar_width, color='red', label='Витрати')

                ax.set_title(title)
                ax.set_xlabel(xlabel)
                ax.set_ylabel("Сума")
                ax.set_xticks(x)
                ax.set_xticklabels(xtick_labels, rotation=30)
                ax.legend()
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

            self.submit_select_month_for_profit_loss_schedule = ttk.Button(
                self.right_frame, text="Додати", width=15, command=get_selected_month)
            self.submit_select_month_for_profit_loss_schedule.config(width=15)
            self.submit_select_month_for_profit_loss_schedule.pack(anchor="ne", padx=10, pady=10)

            get_selected_month()


        def show_circular_spending_chart():
            clear_central_figure()
            clear_right_frame()
            self.month_option_map = ["3 місяця", "6 місяців", "9 місяців", "12 місяців", "За весь час", "За поточний місяць", "За поточний рік", "За минулий рік"]
            selected_option = tk.StringVar(value="За поточний місяць")

            month_menu = ttk.OptionMenu(self.right_frame, selected_option, None, *self.month_option_map)
            month_menu.config(width=15)
            month_menu.pack(anchor="ne", padx=10, pady=10)

            def draw_chart():
                df = pd.DataFrame(self.controller_root.update_transaction(),
                                columns=["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                                        "Сума", "Тип валюти", "Карта", "Дата транзакції"])
                df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
                df = df[df["Тип транзакції"] == "Витрата"]
                df["Сума"] = df["Сума"].abs()

                now = pd.Timestamp.now()
                current_year = now.year
                current_mont = now.month
                option = selected_option.get()

                month_mapping = {
                    "3 місяця": 3,
                    "6 місяців": 6,
                    "9 місяців": 9,
                    "12 місяців": 12
                }

                if option == "За поточний рік":
                    df = df[df["Дата транзакції"].dt.year == current_year]

                elif option == "За поточний місяць":
                    df = df[(df["Дата транзакції"].dt.month == current_mont) & 
                            (df["Дата транзакції"].dt.year == current_year)]

                elif option == "За минулий рік":
                    df = df[df["Дата транзакції"].dt.year == current_year - 1]

                elif option in month_mapping:
                    months_offset = month_mapping[option]
                    end_date = now.replace(day=1) + pd.offsets.MonthEnd(0)
                    start_date = (now.replace(day=1) - pd.DateOffset(months=months_offset - 1))

                    df = df[(df["Дата транзакції"] >= start_date) & (df["Дата транзакції"] <= end_date)]


                grouped = df.groupby("Категорія")["Сума"].sum()

                clear_central_figure()
                fig = Figure(figsize=(7, 6), dpi=100)
                ax = fig.add_subplot(111)
                ax.pie(grouped, labels=grouped.index, autopct='%1.1f%%')
                ax.set_title("Круговий графік витрат")

                canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

            ttk.Button(self.right_frame, text="Показати", command=draw_chart).pack(anchor="ne", padx=10, pady=10)
            draw_chart()



        def show_income_sources():
            clear_central_figure()
            clear_right_frame()

            self.month_option_map = ["3 місяця", "6 місяців", "9 місяців", "12 місяців", "За весь час", "За поточний місяць", "За поточний рік", "За минулий рік"]
            selected_option = tk.StringVar(value="За поточний місяць")

            month_menu = ttk.OptionMenu(self.right_frame, selected_option, None, *self.month_option_map)
            month_menu.config(width=15)
            month_menu.pack(anchor="ne", padx=10, pady=10)

            def draw_chart():
                df = pd.DataFrame(self.controller_root.update_transaction(),
                                columns=["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                                        "Сума", "Тип валюти", "Карта", "Дата транзакції"])
                df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
                df = df[df["Тип транзакції"] == "Дохід"]
                df["Джерело"] = df["Категорія"]

                now = pd.Timestamp.now()
                current_year = now.year
                current_mont = now.month
                option = selected_option.get()

                month_mapping = {
                    "3 місяця": 3,
                    "6 місяців": 6,
                    "9 місяців": 9,
                    "12 місяців": 12
                }

                if option == "За поточний рік":
                    df = df[df["Дата транзакції"].dt.year == current_year]

                elif option == "За поточний місяць":
                    df = df[(df["Дата транзакції"].dt.month == current_mont) & 
                            (df["Дата транзакції"].dt.year == current_year)]

                elif option == "За минулий рік":
                    df = df[df["Дата транзакції"].dt.year == current_year - 1]

                elif option in month_mapping:
                    months_offset = month_mapping[option]

                    end_date = now.replace(day=1) + pd.offsets.MonthEnd(0)
                    start_date = (now.replace(day=1) - pd.DateOffset(months=months_offset - 1))

                    df = df[(df["Дата транзакції"] >= start_date) & (df["Дата транзакції"] <= end_date)]


                grouped = df.groupby("Джерело")["Сума"].sum()

                clear_central_figure()
                fig = Figure(figsize=(7, 6), dpi=100)
                ax = fig.add_subplot(111)
                ax.pie(grouped, labels=grouped.index, autopct='%1.1f%%')
                ax.set_title("Доходи по джерелах")

                canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

            ttk.Button(self.right_frame, text="Показати", command=draw_chart).pack(anchor="ne", padx=10, pady=10)
            draw_chart()


        def show_balance_over_time():
            clear_central_figure()
            clear_right_frame()
            
            cards_data = self.controller_root.get_cards_with_balance()
            pocket_balances = {name: balance for name, balance in cards_data}

            list_cards = self.controller_root.update_card_list()

            df = pd.DataFrame(self.controller_root.update_transaction(),
                            columns=["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                                    "Сума", "Тип валюти", "Карта", "Дата транзакції"])
            df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
            df["Сума"] = df["Сума"].astype(float)
            df["Баланс"] = df.apply(lambda row: row["Сума"] if row["Тип транзакції"] == "Дохід" else -abs(row["Сума"]), axis=1)
            df.sort_values("Дата транзакції", inplace=True)

            fig = Figure(figsize=(11, 5), dpi=100)
            ax = fig.add_subplot(111)

            color_palette = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
                "#bcbd22", "#17becf"
            ]

            lines = []
            labels = []
            for idx, card in enumerate(list_cards):
                df_card = df[df["Карта"] == card].copy()
                if df_card.empty:
                    continue
                

                start_balance = pocket_balances.get(card, 0)

                df_card["Поточний баланс"] = df_card["Баланс"].cumsum() + start_balance

                color = color_palette[idx % len(color_palette)]
                line, = ax.plot(df_card["Дата транзакції"], df_card["Поточний баланс"],
                                label=card, color=color, linewidth=2, marker='o', markersize=4)
                lines.append(line)
                labels.append(card)

            ax.set_title("Баланс з часом по картках", fontsize=14, fontweight='bold')
            ax.set_xlabel("Дата", fontsize=12)
            ax.set_ylabel("Сума", fontsize=12)
            ax.tick_params(axis='both', labelsize=10)
            ax.legend(title="Картки", fontsize=9, title_fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.5)

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            cursor = mplcursors.cursor(lines, hover=True)

            @cursor.connect("add")
            def on_add(sel):
                x, y = sel.target
                date = matplotlib.dates.num2date(x).strftime("%Y-%m-%d")
                line = sel.artist  
                label = line.get_label()  
                sel.annotation.set(text=f"{label}:\nДата: {date}\nБаланс: {y:.2f}")
                sel.annotation.get_bbox_patch().set(fc="white")

        def show_balance_over_time_all_card():
            clear_central_figure()
            clear_right_frame()

            cards_data = self.controller_root.get_cards_with_balance()
            pocket_balances = {name: balance for name, balance in cards_data}

            total_start_balance = sum(pocket_balances.values())

            df = pd.DataFrame(self.controller_root.update_transaction(),
                            columns=["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                                    "Сума", "Тип валюти", "Карта", "Дата транзакції"])
            df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
            df["Сума"] = df["Сума"].astype(float)
            df["Баланс"] = df.apply(lambda row: row["Сума"] if row["Тип транзакції"] == "Дохід" else -abs(row["Сума"]), axis=1)
            df.sort_values("Дата транзакції", inplace=True)

            df["Загальний баланс"] = df["Баланс"].cumsum() + total_start_balance

            fig = Figure(figsize=(11, 5), dpi=100)
            ax = fig.add_subplot(111)

            line, = ax.plot(df["Дата транзакції"], df["Загальний баланс"],
                            label="Усі картки", color="#048830", linewidth=2, marker='o', markersize=4)

            ax.set_title("Загальний баланс з часом", fontsize=14, fontweight='bold')
            ax.set_xlabel("Дата", fontsize=12)
            ax.set_ylabel("Сума", fontsize=12)
            ax.tick_params(axis='both', labelsize=10)
            ax.legend(fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.5)

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            cursor = mplcursors.cursor([line], hover=True)

            @cursor.connect("add")
            def on_add(sel):
                x, y = sel.target
                date = matplotlib.dates.num2date(x).strftime("%Y-%m-%d")
                sel.annotation.set(text=f"Дата: {date}\nБаланс: {y:.2f}")
                sel.annotation.get_bbox_patch().set(fc="white")


        def show_transaction_activity_heatmap():
            clear_central_figure()
            clear_right_frame()

            df = pd.DataFrame(self.controller_root.update_transaction(),
                            columns=["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                                    "Сума", "Тип валюти", "Карта", "Дата транзакції"])
            df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
            df["День тижня"] = df["Дата транзакції"].dt.day_name()
            df["Година"] = df["Дата транзакції"].dt.hour

            pivot = df.pivot_table(index="Година", columns="День тижня", values="ID", aggfunc="count").fillna(0)

            ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            pivot = pivot.reindex(columns=ordered_days)

            day_name_map = {
                "Monday": "Пн",
                "Tuesday": "Вт",
                "Wednesday": "Ср",
                "Thursday": "Чт",
                "Friday": "Пт",
                "Saturday": "Сб",
                "Sunday": "Нд"
            }
            pivot.columns = [day_name_map.get(col, col) for col in pivot.columns]

            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            cax = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")

            ax.set_xticks(range(len(pivot.columns)))
            ax.set_xticklabels(pivot.columns, rotation=45)
            ax.set_yticks(range(len(pivot.index)))
            ax.set_yticklabels(pivot.index)

            ax.set_title("Теплова карта активності транзакцій")
            fig.colorbar(cax, ax=ax, label="Кількість транзакцій")

            canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)


        def show_contractor_category_expense_timeline():
            clear_central_figure()
            clear_right_frame()


            df = pd.DataFrame(self.controller_root.update_transaction(),
                            columns=["ID", "Контрагент", "Категорія", "Підкатегорія", "Тип транзакції",
                                    "Сума", "Тип валюти", "Карта", "Дата транзакції"])
            df = df[df["Тип транзакції"] == "Витрата"]
            df["Сума"] = df["Сума"].abs()
            df["Дата транзакції"] = pd.to_datetime(df["Дата транзакції"])
            df["Місяць"] = df["Дата транзакції"].dt.to_period("M").astype(str)

            contractors = sorted(df["Контрагент"].dropna().unique())
            selected_contractor = tk.StringVar()
            selected_category = tk.StringVar()

            selected_contractor.set(contractors[0] if contractors else "")
            selected_category.set("")

            ttk.Label(self.right_frame, text="Контрагент:").pack(anchor="ne", padx=10, pady=(10, 0))
            contractor_menu = ttk.OptionMenu(self.right_frame, selected_contractor, selected_contractor.get(), *contractors)
            contractor_menu.pack(anchor="ne", padx=10, pady=(0, 10))

            ttk.Label(self.right_frame, text="Категорія:").pack(anchor="ne", padx=10, pady=(10, 0))
            category_menu = ttk.OptionMenu(self.right_frame, selected_category, "")
            category_menu.pack(anchor="ne", padx=10, pady=(0, 10))

            def update_categories(*args):
                contractor = selected_contractor.get()
                if not contractor:
                    return

                filtered_df = df[df["Контрагент"] == contractor]
                categories = sorted(filtered_df["Категорія"].dropna().unique())

                if categories:
                    selected_category.set(categories[0])
                else:
                    selected_category.set("")

                menu = category_menu["menu"]
                menu.delete(0, "end")
                for cat in categories:
                    menu.add_command(label=cat, command=lambda c=cat: selected_category.set(c))


            def draw_chart():
                clear_central_figure()

                contractor = selected_contractor.get()
                category = selected_category.get()
                if not contractor or not category:
                    return

                filtered_df = df[(df["Контрагент"] == contractor) & (df["Категорія"] == category)]
                grouped = filtered_df.groupby("Місяць")["Сума"].sum()

                fig = Figure(figsize=(10, 5), dpi=100)
                ax = fig.add_subplot(111)
                ax.plot(grouped.index, grouped.values, marker="o", linestyle="-", color="orange")

                ax.set_title(f"Витрати: {contractor} → {category}")
                ax.set_xlabel("Місяць")
                ax.set_ylabel("Сума витрат (грн)")
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, master=self.central_figure)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

            selected_contractor.trace("w", update_categories)

            ttk.Button(self.right_frame, text="Показати", command=draw_chart).pack(anchor="ne", padx=10, pady=10)

            update_categories()
            draw_chart()


        "Выбор категории и показывает траты за время"

        Button(self.left_frame, text="Стовпчикова діаграма Доходи/Витрати", command=show_profit_loss_schedule, height=1, bg="#B1B1B1").pack(fill="x", pady=(10, 0))
        Button(self.left_frame, text="Круговий графік витрат", command=show_circular_spending_chart, height=1, bg="#B1B1B1").pack(fill="x")
        Button(self.left_frame, text="Круговий графік доходів", command=show_income_sources, height=1, bg="#B1B1B1").pack(fill="x")
        Button(self.left_frame, text="Баланс з часом по картам", command=show_balance_over_time, height=1, bg="#B1B1B1").pack(fill="x")
        Button(self.left_frame, text="Баланс з часом за рахунком ", command=show_balance_over_time_all_card, height=1, bg="#B1B1B1").pack(fill="x")

        Button(self.left_frame, text="Теплова карта по днях тижня та годин", command=show_transaction_activity_heatmap, height=1, bg="#B1B1B1").pack(fill="x")
        Button(self.left_frame, text="Витрати за категоріями", command=show_contractor_category_expense_timeline, height=1, bg="#B1B1B1").pack(fill="x")


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
                    category_node = target_tree.insert(counterparty_node, "end", text=f"{category_name} ▶", values=category_id, tags = "Категорія", open=False)

                    if category_id in subcategories_by_category:
                        for subcategory in subcategories_by_category[category_id]:
                            subcategory_id, subcategory_name = subcategory[0], subcategory[1]
                            subcategory_node = target_tree.insert(category_node, "end", text=subcategory_name, values=subcategory_id, tags = "Підкатегорія", open=False)


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

        title_label = tk.Label(header_frame, text=f"Вибрано: {item_text}", font=("Arial", 14, "bold"), bg="white")
        title_label.pack()

        item_type = "Невідомо"
        related_data = []

        if item_id:
            item_type = item['tags'][0]

            if item_type == "Контрагент":
                related_data = self.controller_root.get_counterpart_info(item_id)
            elif item_type == "Категорія":
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

        edit_icon = PILImageTk.PhotoImage(file="images/image_buttom/change.png")  
        delete_icon = PILImageTk.PhotoImage(file="images/image_buttom/dustbin.png")  

        counteragent_data = [item_id, item_text]
        if "▼" in counteragent_data[1] or "▶" in counteragent_data[1]:
            counteragent_data[1] = counteragent_data[1][0:-1]
        

        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side="right")
        

        edit_button_counteragent = tk.Button(button_frame, image=edit_icon, command=lambda data=counteragent_data: self.open_edit_window(data,item_type))
        edit_button_counteragent.image = edit_icon  
        edit_button_counteragent.grid(row=0, column=1, sticky="ne", padx=5, pady=5)  

        delete_button_counteragent = tk.Button(button_frame, image=delete_icon, command=lambda data=counteragent_data: self.open_delete_window(data,item_type))
        delete_button_counteragent.image = delete_icon  
        delete_button_counteragent.grid(row=1, column=1, sticky="ne", padx=5, pady=5)

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

                if item_type == "Контрагент":
                    edit_button = tk.Button(target_col, image=edit_icon, command=lambda data=data: self.open_edit_window(data,'Категорія'))
                    delete_button = tk.Button(target_col, image=delete_icon, command=lambda data=data:  self.open_delete_window(data,'Категорія'))
                elif item_type == "Категорія":
                    edit_button = tk.Button(target_col, image=edit_icon, command=lambda data=data: self.open_edit_window(data,'Підкатегорія'))
                    delete_button = tk.Button(target_col, image=delete_icon, command=lambda data=data:  self.open_delete_window(data,'Підкатегорія'))

                edit_button.image = edit_icon  
                edit_button.grid(row=row_index, column=1, sticky="e", padx=5)

                delete_button.image = delete_icon  
                delete_button.grid(row=row_index, column=2, sticky="e", padx=5)

                row_index += 1 
        else:
            tk.Label(col1, text="Немає даних", bg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w")


    def open_edit_window(self, data, type_item):
        self.create_middle_window()
        edit_window = self.new_window  

        label = tk.Label(edit_window, text=f"Введіть нове Ім'я Контрагента:")
        label.pack(padx=10, pady=5)

        entry = tk.Entry(edit_window)
        entry.insert(0, data[1])  
        entry.pack(padx=10, pady=5)

        def submit_edit():
            new_name = entry.get()  
            if new_name:  

                self.controller_root.submit_edit_conagent_category_subcategory((data[0], new_name), type_item)
                edit_window.destroy()  
                
            else:
                messagebox.showerror("Помилка", "Ім'я не може бути порожнім!")

        submit_button = tk.Button(edit_window, text="Зберегти", command=submit_edit)
        submit_button.pack(padx=10, pady=5)


    def open_delete_window(self, data, type_item):
        self.create_middle_window()
        delete_window = self.new_window  

        label = tk.Label(delete_window, text=f"Ви впевнені, що хочете Видалити {data[1]}?")
        label.pack(padx=10, pady=5)

        def confirm_delete():

            deleted = self.controller_root.submit_delete_conagent_category_subcategory(data, type_item)

            if deleted:
                messagebox.showinfo("Видалення", "Видалено успішно.")
            else:
                messagebox.showwarning("Попередження", "Неможливо Видалити - є зв'язок чи транзакції.")
            delete_window.destroy()

        confirm_button = tk.Button(delete_window, text="Видалити", command=confirm_delete)
        confirm_button.pack(side="left", padx=10, pady=5)

        cancel_button = tk.Button(delete_window, text="Скасування", command=delete_window.destroy)
        cancel_button.pack(side="right", padx=10, pady=5)


    def toggle_arrow(self, event, old_symbol, new_symbol, tree):
        item = tree.focus()
        text = tree.item(item, "text")
        if old_symbol in text:
            tree.item(item, text=text.replace(old_symbol, new_symbol))





