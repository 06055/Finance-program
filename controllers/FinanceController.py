from tkinter import filedialog, messagebox
import requests
import time
from datetime import date, timedelta

class FinanceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.user_id = None 
        self.view.window_reg()
        self.view.set_controller(self)
        self.view.submit_button_reg.config(command=self.submit_data_reg)
        self.view.submit_button_log.config(command=self.submit_data_show_log)
        self.currencies_loaded = False   
        self.rates_cache = None          
        self.rates_cache_base_currency = None
        self.last_rates_fetch_ts = None 

    def has_internet(self, check_base='USD', timeout=4):
        """
        Простая проверка интернета через API (легкая GET).
        Возвращает True если доступен API.
        """
        try:

            url = f"https://open.er-api.com/v6/latest/{check_base}"
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return True
        except requests.RequestException:
            return False


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


    def get_add_actual_currency(self, key, value):
        return self.set_main_currency(key)

    def get_select_actualy_amount(self):
        currency = self.get_main_currency()
        return (None, currency, 1)


    def get_main_currency(self, user_id=None):
        return self.model.get_main_currency(self.user_id if user_id is None else user_id)


    def set_main_currency(self, currency, user_id=None):
        result = self.model.set_main_currency(self.user_id if user_id is None else user_id, currency)
        self.currencies_loaded = False
        self.rates_cache = None
        self.rates_cache_base_currency = None
        return result


    def get_secondary_currencies(self, user_id=None):
        return self.model.get_secondary_currencies(self.user_id if user_id is None else user_id)


    def set_secondary_currencies(self, currency1, currency2, user_id=None):
        return self.model.set_secondary_currencies(self.user_id if user_id is None else user_id, currency1, currency2)


    def get_available_currencies(self, user_id=None):
        return self.model.get_available_currencies(self.user_id if user_id is None else user_id)


    def convert_currency(self, amount, from_currency, to_currency):
        try:
            amount = float(amount or 0)
        except (TypeError, ValueError):
            amount = 0

        from_currency = str(from_currency).strip().upper()
        to_currency = str(to_currency).strip().upper()
        if from_currency == to_currency:
            return amount

        if self.rates_cache:
            if self.rates_cache_base_currency == from_currency and to_currency in self.rates_cache:
                return amount * float(self.rates_cache[to_currency])
            if self.rates_cache_base_currency == to_currency and from_currency in self.rates_cache:
                rate = float(self.rates_cache[from_currency])
                if rate:
                    return amount / rate

        return self.model.convert_currency(amount, from_currency, to_currency)


    def get_total_balance_in_main_currency(self, user_id=None):
        return self.model.get_total_balance_in_main_currency(self.user_id if user_id is None else user_id)


    def format_money(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0

        formatted = f"{value:,.2f}"
        return formatted.replace(",", " ").replace(".", ",").replace(" ", ".")


    def get_total_balance_items(self):
        total, main_currency = self.get_total_balance_in_main_currency()
        balances = [(main_currency, self.format_money(total))]

        for currency in self.get_secondary_currencies():
            if currency == main_currency:
                continue
            converted_total = self.convert_currency(total, main_currency, currency)
            balances.append((currency, self.format_money(converted_total)))

        return balances[:3]


    def get_total_balance_text(self):
        balances = []
        for currency, amount in self.get_total_balance_items():
            balances.append(f"{amount} {currency}")

        return "Баланс: " + " | ".join(balances[:3])


    def get_currency_parsing_left_panel(self):
        return self.model.select_currency_parsing_left_panel(self.user_id)


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

        self.model.update_transaction_info(self.id_tr,counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, selected_before_card, self.user_id)
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


    def submit_currency_parsing_left_panel(self, name_currency, type_currency):
        return self.model.add_currency_parsing_left_panel(name_currency, type_currency, self.user_id)


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


    def fetch_rates(self, base_currency, timeout=6):
        try:
            url = f"https://open.er-api.com/v6/latest/{base_currency}"
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            rates = data.get("rates")
            if not rates:
                return None
            return {k: float(v) for k, v in rates.items()}
        except requests.RequestException:
            return None


    def ensure_currencies_loaded(self):
        if self.currencies_loaded and self.rates_cache:
            return True

        base_currency = self.get_main_currency()
        if not base_currency:
            return False

        if not self.has_internet(check_base=base_currency):
            return False

        rates = self.fetch_rates(base_currency)
        if rates is None:
            return False

        ok = self.model.update_left_panel_rates(rates, self.user_id)
        if ok:
            self.rates_cache = rates
            self.rates_cache_base_currency = base_currency
            self.last_rates_fetch_ts = time.time()
            self.currencies_loaded = True
            return True
        return False


    def change_main_currency(self, new_currency):
        self.set_main_currency(new_currency)
        self.model.recalculate_left_panel(new_currency, self.user_id)
        self.currencies_loaded = False
        self.rates_cache = None
        self.rates_cache_base_currency = None


    def refresh_all_currencies(self, base_currency):
        if not self.has_internet(check_base=base_currency):
            return False
        rates = self.fetch_rates(base_currency)
        if not rates:
            return False
        ok = self.model.update_left_panel_rates(rates, self.user_id)
        if ok:
            self.rates_cache = rates
            self.rates_cache_base_currency = base_currency
            self.currencies_loaded = True
            self.last_rates_fetch_ts = time.time()
            return True
        return False


    def tool_currency_parsing(self, name_currency, base_currency):
        name_currency = name_currency.strip().upper()
        base_currency = base_currency.strip().upper()

        if self.currencies_loaded and self.rates_cache:
            rate = None
            try:
                if self.rates_cache_base_currency == base_currency and name_currency in self.rates_cache:
                    rate = self.rates_cache[name_currency]
            except Exception:
                rate = None

            if rate is not None:
                return name_currency, float(rate)

        try:
            url = f"https://open.er-api.com/v6/latest/{base_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "rates" not in data:
                return None

            rate = data["rates"].get(name_currency)
            if rate is None:
                return None

            return name_currency, float(rate)

        except requests.RequestException:
            return None


    def change_base_currency_and_recalculate(self, new_currency):
        self.set_main_currency(new_currency)

        self.currencies_loaded = False
        self.rates_cache = None
        self.rates_cache_base_currency = None

        self.ensure_currencies_loaded()



    def fetch_currency_history(self, base_currency, target_currency, days=30):
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        url = (
            f"https://api.frankfurter.app/"
            f"{start_date}..{end_date}"
            f"?from={base_currency}&to={target_currency}"
        )

        try:
            response = requests.get(url, timeout=4)
            response.raise_for_status()
            data = response.json()

            rates = data.get("rates")
            if not rates:
                return None

            history = [
                (day, values[target_currency])
                for day, values in sorted(rates.items())
            ]

            return history

        except requests.RequestException:
            return None
