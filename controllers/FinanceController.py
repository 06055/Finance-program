from tkinter import filedialog, messagebox
import requests


class FinanceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.user_id = None 
        self.view.window_reg()
        self.view.set_controller(self)
        self.view.submit_button_reg.config(command=self.submit_data_reg)
        self.view.submit_button_log.config(command=self.submit_data_show_log)


    def submit_data_reg(self):
        name, gmail, password, password_repeat = self.view.get_user_input_reg()
        result = self.model.model_registration(name, gmail, password, password_repeat)
        if result == "Успішна реєстрація":
            self.view.clear_widgets()
            self.view.window_log(result)
            self.view.submit_button_log.config(command=self.submit_data_log_and_main)
        else:
            self.view.clear_widgets()
            self.view.window_reg(result)
            self.view.submit_button_reg.config(command=self.submit_data_reg)


    def submit_data_show_log(self):
        self.view.clear_widgets()
        self.view.window_log()
        self.view.submit_button_log.config(command=self.submit_data_log_and_main)


    def submit_data_log_and_main(self):
        gmail, password = self.view.get_user_input_log()
        result = self.model.model_logining(gmail, password)
        
        if isinstance(result, tuple) and result[0] == 'Yes':
            self.user_id = result[1]

            self.view.clear_widgets()
            self.view.window_transaction()
            self.view.load_icons('window_transaction', self.title_icons)
        else:
            self.view.clear_widgets()
            self.view.window_log(result)
            self.view.submit_button_log.config(command=self.submit_data_log_and_main)


    def title_icons(self, image_path):
        if "bookBlack" in image_path:
            self.view.clear_widgets()
            self.view.window_transaction()
            self.view.load_icons('window_transaction', self.title_icons)

        elif "cardBlack" in image_path:
            self.view.clear_widgets()
            self.view.window_cards(self.model.select_cars_all(self.user_id))
            self.view.load_icons('window_cards', self.title_icons)

        elif "dollarBlack" in image_path:
            self.view.clear_widgets()
            self.view.window_dollars()
            self.view.load_icons('window_dollar', self.title_icons)

        elif "statisticBlack" in image_path:
            self.view.clear_widgets()
            self.view.window_statistic()
            self.view.load_icons('window_statistic', self.title_icons)

        elif "ucounterpartiesBlack" in image_path:
            self.view.clear_widgets()
            self.view.window_counteragents()
            self.view.load_icons('window_counteragents', self.title_icons)


    def get_select_card_all(self):
        return self.model.select_cars_all(self.user_id)


    def get_subcategories_by_category(self, category_id):
        return self.model.select_subcategories_by_category(category_id)


    def get_counterpart_info(self, counterpart_id):
        return self.model.select_counterpart_info(counterpart_id)


    def get_user_card_names(self):
        return self.model.get_user_card_names(self.user_id)


    def get_cards_with_balance(self):
        return self.model.select_cards_with_balance(self.user_id)


    def get_add_actual_currency(self,key,value):
        result = self.model.add_db_actualy_amount(key,value)
        print(result)


    def get_select_actualy_amount(self):
        get_actual_currency = self.model.select_actualy_amount()
        return get_actual_currency


        
    

    def get_currency_parsing_left_panel(self):
        result = self.model.select_currency_parsing_left_panel()
        return result


    def try_delete_card(self, card_id):
        result = self.model.can_delete_card(card_id)
        if result == None:
            messagebox.showwarning("Неможливо видалити", "Карта не може бути видалена. Переконайтеся, що: \n- Баланс дорівнює 0\n- Термін дії минув чи ні транзакцій")

        if result[0]:
            confirm = messagebox.askyesno("Підтвердження", f"Ви впевнені, що хочете видалити карту {result[1]}?")
            if confirm:
                pass
                self.model.delete_card(card_id,result[1])
                messagebox.showinfo("Видалено", "Карта успішно видалена.")
                self.view.new_window.destroy()
                self.view.refresh_cards()


    def try_edit_card(self, card_id, new_name, new_type, new_currency, float_money, formatted):
        self.model.edit_card(card_id, new_name, new_type, new_currency, float_money, formatted)
        self.view.refresh_cards()


    def add_new_card(self):
        name_card,type_card,balance_card,selected_currency,selected_file_or_color,full_date,status = self.view.get_add_card_information()
        self.model.add_new_card(name_card,type_card,balance_card,selected_currency,selected_file_or_color,full_date,status,self.user_id)
        self.view.new_window.destroy()
        self.view.refresh_cards()



    def add_transaction(self):
        counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date = self.view.get_transaction_information()
        if (
            counteragent == 'Вибір Контрагента' or not counteragent or
            category == 'Вибір Категорії' or not category or
            subcategory == 'Вибір Підкатегорії' or not subcategory or
            type_transaction == 'Вибір типу транзакції' or not type_transaction or
            choisecard_menu == 'Вибір картки' or not choisecard_menu or
            not amount.strip()
        ):
            messagebox.showerror("Помилка", "Будь ласка, заповніть усі поля.")
            return

        try:
            amount_value = float(amount)
            if amount_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка", "Сума має бути додатнім числом.")
            return

        self.model.add_transaction(counteragent, category, subcategory, type_transaction, amount_value, currency, choisecard_menu, date, self.user_id)
        self.view.new_window.destroy()
        self.view.refresh_transaction()


    def add_transaction_personal(self):
        counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date = self.view.get_transaction_information()
        self.model.add_transaction(counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date,self.user_id)
        result = self.model.select_transaction_personal_id(self.actual_id,self.user_id)
        self.view.refresh_personal_transaction(result)


    def close_transaction_personal(self):
        self.view.refresh_cards()


    def submit_data_add_counterparty(self):
        name = self.view.get_counterparty_input()  
        self.model.add_counterparty(name,self.user_id)
        self.view.new_window.destroy()
        self.view.refresh_counteragents()


    def submit_data_add_category(self):
        name, parent_id = self.view.get_category_input()
        self.model.add_category(name, parent_id, self.user_id)
        self.view.new_window.destroy()
        self.view.refresh_counteragents()


    def submit_data_add_subcategory(self):
        name, parent_id = self.view.get_subcategory_input()
        self.model.add_subcategory(name,parent_id,self.user_id)
        self.view.new_window.destroy() 
        self.view.refresh_counteragents()


    def submit_update_personal_card_transaction(self, card_id):
        self.actual_id = card_id
        result = self.model.select_transaction_personal_id(card_id,self.user_id)
        self.view.personal_transaction_card(result)


    def submit_update_id_transaction(self,id_tr):
        self.id_tr = id_tr
        result = self.model.select_info_from_id_transaction(id_tr)
        return result


    def submit_edit_transaction(self):
        result = self.view.edit_transaction()
        
        result = list(result)
        if result[3] == 'Дохід':
            result[4] = abs(float(result[4]))
        else:
            result[4] = -abs(float(result[4]))
        counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, which_window_transaction, selected_before_card = result

        self.model.update_transaction_info(self.id_tr,counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, selected_before_card)
        if which_window_transaction == 'main':
            self.view.new_window.destroy()
            self.view.refresh_transaction()
        else:
            result = self.model.select_transaction_personal_id(self.actual_id,self.user_id)
            self.view.refresh_personal_transaction(result)


    def submit_delete_transaction(self,transaction_id):
        result = self.view.delete_transaction()

        self.model.delete_transaction(transaction_id)
        if result == 'main':
            self.view.new_window.destroy()
            self.view.refresh_transaction()
        else:
            result = self.model.select_transaction_personal_id(self.actual_id,self.user_id)
            self.view.refresh_personal_transaction(result)


    def submit_edit_conagent_category_subcategory(self, data, type_item):
        item_id, name = data
        transactions = self.model.check_for_transactions(item_id, type_item)

        if transactions:
            
            if type_item == "Контрагент":
                self.model.update_counteragent(name, item_id)
            elif type_item == "Категорія":
                self.model.update_category(name, item_id)  
            elif type_item == "Підкатегорія":
                self.model.update_subcategory(name, item_id)  
        else:
            if type_item == "Контрагент":
                self.model.update_counteragent(name, item_id)
            elif type_item == "Категорія":
                self.model.update_category(name, item_id)  
            elif type_item == "Підкатегорія":
                self.model.update_subcategory(name, item_id)  

        self.view.refresh_counteragents()


    def submit_delete_conagent_category_subcategory(self, data, type_item):
        item_id, name = data
        deleted = False

        if type_item == "Контрагент":
            deleted = self.model.delete_counteragent(name,item_id)
        elif type_item == "Категорія":
            deleted = self.model.delete_category(name,item_id)
        elif type_item == "Підкатегорія":
            deleted = self.model.delete_subcategory(name,item_id)
        self.view.refresh_counteragents()
        return deleted


    def submit_currency_parsing_left_panel(self,name_currency,type_currency):
        result = self.model.add_currency_parsing_left_panel(name_currency,type_currency)
        print(result)


    def update_info_delete_conagent_category_subcategory(self,item_id,type_item):
        transactions = self.model.check_for_transactions(item_id, type_item)
        return transactions


    def update_card_name_currency(self):
        result = self.model.select_name_currency_card(self.actual_id)
        return result


    def update_card_list(self):
        card_names = self.model.select_cars(self.user_id)
        return card_names


    def update_card_currency(self, selected_card):
        return self.model.select_currency_by_card(selected_card)


    def update_counterparty_list(self):
        self.counterparty = self.model.select_counterparties(self.user_id)
        return self.counterparty


    def update_category_list(self):
        self.category = self.model.select_category(self.user_id)
        return self.category


    def update_subcategory_list(self):
        self.subcategory = self.model.select_subcategory(self.user_id)
        return self.subcategory


    def update_category_for_subcategory(self):
        self.category_for_subcategory = self.model.select_category_for_subcategory(self.user_id)
        return self.category_for_subcategory


    def update_transaction(self):
        self.transaction = self.model.select_transaction(self.user_id)
        return self.transaction


    def show_card_by_name(self, card_name):
        card_data = self.model.select_card_by_name(card_name, self.user_id)
        self.view.choice_edit_delete_card(card_data)


    def is_card_name_exist(self, name):
        return self.model.is_card_name_exist(name)


    def change_main_currency(self, new_currency):

        self.model.add_db_actualy_amount(new_currency, 1)
        self.model.recalculate_left_panel(new_currency)


    def refresh_all_currencies(self, base_currency):
        return self.model.recalculate_left_panel(base_currency)


    def tool_currency_parsing(self, name_currency, base_currency):
        name_currency = name_currency.strip().upper()
        base_currency = base_currency.strip().upper()

        try:
            url = f"https://open.er-api.com/v6/latest/{name_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "rates" not in data:
                return None

            rate = data["rates"].get(base_currency)
            if rate is None:
                return None

            return name_currency, rate

        except requests.RequestException:
            
            return None