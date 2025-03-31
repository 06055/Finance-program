class FinanceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.window_reg()
        self.view.set_controller(self)
        self.view.submit_button_reg.config(command=self.submit_data_reg)
        self.view.submit_button_log.config(command=self.submit_data_show_log)


    def submit_data_reg(self):
        name, gmail, password, password_repeat = self.view.get_user_input_reg()
        result = self.model.model_registration(name, gmail, password, password_repeat)
        if result == "Успешная реестрация":
            self.view.clear_widgets()
            self.view.window_log()
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
        if result == 'Yes':
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
            self.view.window_cards(self.model.select_cars_all())
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
            self.view.load_icons('window_ucounterparties', self.title_icons)


    def get_select_card_all(self):
        return self.model.select_cars_all()


    def get_subcategories_by_category(self, category_id):
        return self.model.select_subcategories_by_category(category_id)


    def get_counterpart_info(self, counterpart_id):
        return self.model.select_counterpart_info(counterpart_id)


    def add_new_card(self):
        name_card,type_card,balance_card,selected_currency,selected_file_or_color,full_date = self.view.get_add_card_information()
        self.model.add_new_card(name_card,type_card,balance_card,selected_currency,selected_file_or_color,full_date)
        self.view.new_window.destroy()
        self.view.refresh_cards()


    def add_transaction(self):
        counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date = self.view.get_transaction_information()
        self.model.add_transaction(counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date)
        self.view.new_window.destroy()
        self.view.refresh_transaction()


    def add_transaction_personal(self):
        counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date = self.view.get_transaction_information()
        self.model.add_transaction(counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date)
        result = self.model.select_transaction_personal_id(self.actual_id)
        self.view.refresh_personal_transaction(result)


    def close_transaction_personal(self):
        self.view.refresh_cards()


    def submit_data_add_counterparty(self):
        name = self.view.get_counterparty_input()  
        self.model.add_counterparty(name)
        self.view.new_window.destroy()


    def submit_data_add_category(self):
        name, parent_id = self.view.get_category_input()
        self.model.add_category(name, parent_id)
        self.view.new_window.destroy()


    def submit_data_add_subcategory(self):
        name, parent_id = self.view.get_subcategory_input()
        self.model.add_subcategory(name,parent_id)
        self.view.new_window.destroy() 


    def submit_update_personal_card_transaction(self, card_id):
        self.actual_id = card_id
        result = self.model.select_transaction_personal_id(card_id)
        self.view.personal_transaction_card(result)


    def submit_update_id_transaction(self,id_tr):
        self.id_tr = id_tr
        result = self.model.select_info_from_id_transaction(id_tr)
        return result


    def submit_edit_transaction(self):
        result = self.view.edit_transaction()
        
        result = list(result)
        if result[3] == 'Доход':
            result[4] = abs(float(result[4]))
        else:
            result[4] = -abs(float(result[4]))
        counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, which_window_transaction, selected_before_card = result

        self.model.update_transaction_info(self.id_tr,counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, selected_before_card)
        if which_window_transaction == 'main':
            self.view.new_window.destroy()
            self.view.refresh_transaction()
        else:
            result = self.model.select_transaction_personal_id(self.actual_id)
            self.view.refresh_personal_transaction(result)


    def update_card_name_currency(self):
        result = self.model.select_name_currency_card(self.actual_id)
        return result


    def update_card_list(self):
        card_names = self.model.select_cars()
        return card_names


    def update_card_currency(self, selected_card):
        return self.model.select_currency_by_card(selected_card)


    def update_counterparty_list(self):
        self.counterparty = self.model.select_counterparties()
        return self.counterparty


    def update_category_list(self):
        self.category = self.model.select_category()
        return self.category


    def update_subcategory_list(self):
        self.subcategory = self.model.select_subcategory()
        return self.subcategory


    def update_category_for_subcategory(self):
        self.category_for_subcategory = self.model.select_category_for_subcategory()
        return self.category_for_subcategory


    def update_transaction(self):
        self.transaction = self.model.select_transaction()
        return self.transaction



