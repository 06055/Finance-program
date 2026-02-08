import mysql.connector
from datetime import datetime
from tkinter import messagebox
import re
import requests

class FinanceModel:

    @staticmethod
    def model_registration(name, gmail, password, password_repeat):
        if not all([name, gmail, password, password_repeat]):
            return "Заповніть всі поля"

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(email_pattern, gmail):
            return "Некоректна електронна пошта"
        if password != password_repeat:
            return "Пароль не збігається"

        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = "SELECT gmail FROM user WHERE gmail = %s"

        cursor.execute(_SQL, (gmail,))
        gmail_sql = cursor.fetchone()

        if gmail_sql is not None:
            return "Пошта зайнята"
        
        _SQL = "INSERT INTO user(name, gmail, password) VALUES(%s, %s, Sha1(%s))"
        cursor.execute(_SQL, (name, gmail, password))
        dbc.commit()

        return "Успішна реєстрація"


    @staticmethod
    def model_logining(gmail, password):
        if gmail != None and gmail != '':
            
            if password != None and gmail != '':
                dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
                dbc = mysql.connector.connect(**dbconfig)
                cursor = dbc.cursor()
                _SQL = """SELECT id FROM user WHERE gmail = %s and password = Sha1(%s)"""
                cursor.execute(_SQL,(gmail,password))
                result = cursor.fetchone()

                cursor.close()
                dbc.close()
                if result is not None:
                    user_id = result[0]
                    return 'Yes', user_id  
                else:
                    return 'Пошта або пароль були введені неправильно'
        return 'Пошта або пароль були введені неправильно'


    @staticmethod
    def add_new_card(name_card,type_card,balance_card,selected_currency,selected_file_or_color,full_date,status,user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        if '/' in selected_file_or_color or ':' in selected_file_or_color:
            _SQL = """INSERT INTO pocket(name, type_pocket, type_currency, data_made, count_money, bg_picture, status, user_id)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        else:
            _SQL = """INSERT INTO pocket(name, type_pocket, type_currency, data_made, count_money, bg_color, status, user_id)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""


        cursor.execute(_SQL,(name_card,type_card,selected_currency,full_date,balance_card,selected_file_or_color,status, user_id))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def can_delete_card(card_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute("SELECT name, count_money, data_made FROM pocket WHERE id = %s", (card_id,))
        result = cursor.fetchone()

        if not result:
            return 

        name, count_money, data_made = result
        now = datetime.now()
        expired = now.date() > data_made.date()

        if expired == 1 and count_money == 0 :
            return True,name

        cursor.close()
        dbc.close()


    @staticmethod
    def delete_card(card_id,card_name):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """DELETE FROM pocket WHERE id = %s"""
        cursor.execute(_SQL,(card_id,))
        dbc.commit()
        _SQL = """DELETE FROM transactions WHERE card = %s"""
        cursor.execute(_SQL,(card_name,))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_cars_all(user_id):
        list_cards = []
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'newusername',
            'password': 'newpassword',
            'db': 'home_finances'
        }
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute("""
            UPDATE pocket
            SET status = NULL
            WHERE data_made IS NOT NULL AND data_made < NOW()
        """)

        cursor.execute("""
            UPDATE pocket
            SET status = 1
            WHERE data_change IS NOT NULL AND (status IS NULL OR status != 1) AND data_made > NOW()
        """)

        dbc.commit()

        cursor.execute("""
            SELECT id, name, type_pocket, type_currency, data_made, data_change, count_money, bg_color, bg_picture, status
            FROM pocket
            WHERE user_id = %s
        """, (user_id,))
        
        result = cursor.fetchall()
        for row in result:
            list_cards.append(row)

        cursor.close()
        dbc.close()
        return list_cards



    @staticmethod
    def select_card_by_name(card_name, user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id, name, type_pocket, type_currency, data_made, data_change, count_money, bg_color, bg_picture, status FROM pocket WHERE user_id = %s"""

        _SQL = """
            SELECT id, name, type_pocket, type_currency, data_made, data_change,
            count_money, bg_color, bg_picture, status
            FROM pocket
            WHERE name = %s AND user_id = %s
            LIMIT 1
        """
        cursor.execute(_SQL, (card_name, user_id))
        result = cursor.fetchone()

        cursor.close()
        dbc.close()

        return result

    @staticmethod
    def get_user_card_names(user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = "SELECT name FROM pocket WHERE user_id = %s"
        cursor.execute(_SQL, (user_id,))
        result = cursor.fetchall()

        dbc.close()
        cursor.close()
        return [row[0] for row in result]


    @staticmethod
    def edit_card(card_id, name, type_pocket, type_currency, count_money, formatted):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        try:
            cursor.execute("SELECT name FROM pocket WHERE id = %s", (card_id,))
            result = cursor.fetchone()
            if not result:
                raise Exception("Карта не найдена")
            old_name = result[0]

            _SQL = """
                UPDATE pocket 
                SET name=%s, type_pocket=%s, type_currency=%s, count_money=%s, data_made = %s, data_change=NOW()
                WHERE id=%s
            """
            cursor.execute(_SQL, (name, type_pocket, type_currency, count_money, formatted, card_id))

            if old_name != name:
                update_transactions_sql = """
                    UPDATE transactions SET card=%s WHERE card=%s
                """
                cursor.execute(update_transactions_sql, (name, old_name))

            dbc.commit()
        except Exception as e:
            dbc.rollback()
            raise e
        finally:
            cursor.close()
            dbc.close()


    @staticmethod
    def select_cars(user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT name FROM pocket WHERE user_id = %s"""  
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()
        cursor.close()
        dbc.close()
        return [row[0] for row in result]  

    @staticmethod
    def select_cards_with_balance(user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT name, count_money FROM pocket WHERE user_id = %s"""
        cursor.execute(_SQL, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        dbc.close()
        return [(row[0], float(row[1])) for row in result]



    @staticmethod
    def select_currency_by_card(card_name):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor(buffered=True)
        _SQL = """SELECT type_currency FROM pocket WHERE name = %s"""
        cursor.execute(_SQL, (card_name,))
        result = cursor.fetchone()
        cursor.close()
        dbc.close()
        if result:
            return result[0]
        return None



    @staticmethod
    def add_counterparty(name,user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO counterparties (name,user_id) VALUES (%s,%s)"""
        cursor.execute(_SQL, (name,user_id,))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_counterparties(user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id,name FROM counterparties WHERE user_id = %s"""
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def add_category(name, parent_id,user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO categories (name, parent_id, user_id) VALUES (%s, %s, %s)"""
        cursor.execute(_SQL, (name, parent_id, user_id,))
        dbc.commit()

        cursor.close()
        dbc.close()


    
    @staticmethod
    def select_category(user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT id, name, parent_id FROM categories WHERE user_id = %s"""
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()

        return result
    

    @staticmethod
    def select_category_for_subcategory(user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id,name FROM categories WHERE user_id = %s"""
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def add_subcategory(name,parent_id,user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO subcategory (name, parent_id, user_id) VALUES (%s, %s, %s)"""
        cursor.execute(_SQL, (name, parent_id, user_id))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_subcategory(user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id,name,parent_id FROM subcategory WHERE user_id = %s"""
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def add_transaction(counteragent, category, subcategory, type_transaction, amount, currency, card, date, user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        try:
            amount = float(amount)
            if type_transaction.lower() == "витрата":
                amount = -abs(amount)
            else:
                amount = abs(amount)
            _SQL = """
            INSERT INTO transactions 
            (counteragent, categoria, subcategoria, type_transaction, count, currency, card, data, user_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(_SQL, (counteragent, category, subcategory, type_transaction, amount, currency, card, date, user_id))

            _SQL_UPDATE_BALANCE = """UPDATE pocket SET count_money = count_money + %s WHERE name = %s AND user_id = %s"""
            cursor.execute(_SQL_UPDATE_BALANCE, (amount, card, user_id))

            dbc.commit()

        except ValueError:

            messagebox.showerror("Помилка: «сума» має бути числом.")
            messagebox.showerror("")
        except mysql.connector.Error as err:
            print(f"Помилка: {err}")
        finally:
            cursor.close()
            dbc.close()


    @staticmethod
    def select_transaction(user_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id, counteragent, categoria, subcategoria, type_transaction, count, currency, card, data FROM transactions WHERE user_id = %s"""
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result

    def is_card_name_exist(self, name):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = "SELECT COUNT(*) FROM pocket WHERE name = %s"
        cursor.execute(_SQL, (name,))
        count = cursor.fetchone()[0]
        cursor.close()
        dbc.close()
        return count > 0

    @staticmethod
    def select_transaction_personal_id(card_id,user_id):
        
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT name FROM pocket WHERE id = %s"""
        
        cursor.execute(_SQL,(card_id,))
        name_card = cursor.fetchone()

        _SQL = """SELECT * FROM transactions WHERE card = %s AND user_id = %s"""
        cursor.execute(_SQL,(name_card[0],user_id,))
        result = cursor.fetchall()
        
        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def select_name_currency_card(card_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT name,type_currency FROM pocket WHERE id = %s"""
        
        cursor.execute(_SQL,(card_id,))
        result = cursor.fetchall()

        
        cursor.close()
        dbc.close()
        return result
    

    @staticmethod
    def select_info_from_id_transaction(id_tr):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM transactions WHERE id = %s"""
        
        cursor.execute(_SQL,(id_tr,))
        result = cursor.fetchall()

        
        cursor.close()
        dbc.close()
        return result[0]
    

    @staticmethod
    def update_transaction_info(id_tr, counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, selected_before_card):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        amount = float(amount)

        cursor.execute("SELECT count FROM transactions WHERE id = %s", (id_tr,))
        previous_amount = cursor.fetchone()[0]
        
        if type_transaction.lower() == "витрата":
            amount = -abs(amount)
        else:
            amount = abs(amount)

        if selected_before_card != choisecard_menu:
            _SQL = """UPDATE pocket SET count_money = count_money - %s WHERE name = %s"""
            cursor.execute(_SQL, (previous_amount, selected_before_card))
            dbc.commit()

            _SQL = """UPDATE pocket SET count_money = count_money + %s WHERE name = %s"""
            cursor.execute(_SQL, (amount, choisecard_menu))
            dbc.commit()
        else:
            _SQL = """UPDATE pocket SET count_money = count_money - %s + %s WHERE name = %s"""
            cursor.execute(_SQL, (previous_amount, amount, choisecard_menu))
            dbc.commit()

        _SQL = """UPDATE transactions 
                SET counteragent = %s,
                categoria = %s, 
                subcategoria = %s, 
                type_transaction = %s, 
                count = %s,
                currency = %s, 
                card = %s, 
                data = %s 
                WHERE id = %s"""
        cursor.execute(_SQL, (counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, id_tr))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_counterpart_info(counterpart_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id, name FROM categories WHERE parent_id = %s"""
        cursor.execute(_SQL, (counterpart_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()

        return result


    def select_subcategories_by_category(self,category_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        
        _SQL = """SELECT id, name FROM subcategory WHERE parent_id = %s"""
        cursor.execute(_SQL, (category_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()

        return result


    def delete_transaction(self,transaction_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute("SELECT count, card FROM transactions WHERE id = %s", (transaction_id,))
        result = cursor.fetchone()

        if result:
            amount, card_name = result
            amount = float(amount)
            
            if amount < 0:  
                _SQL = """UPDATE pocket SET count_money = count_money + %s WHERE name = %s"""
            else:  
                _SQL = """UPDATE pocket SET count_money = count_money - %s WHERE name = %s"""
            
            cursor.execute(_SQL, (abs(amount), card_name))
            dbc.commit()

            _SQL = """DELETE FROM transactions WHERE id = %s"""
            cursor.execute(_SQL, (transaction_id,))
            dbc.commit()

        cursor.close()
        dbc.close()



    def check_for_transactions(self,item_id, type_item):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        if type_item == "Контрагент":
            _SQL = """SELECT name FROM counterparties WHERE id = %s"""
            cursor.execute(_SQL,(item_id,))
            transactions = cursor.fetchone()
            _SQL = """SELECT * FROM transactions WHERE counteragent = %s"""
            cursor.execute(_SQL,(transactions[0],))

        elif type_item == "Категорія":
            _SQL = """SELECT name FROM categories WHERE id = %s"""
            cursor.execute(_SQL,(item_id,))
            transactions = cursor.fetchone()
            _SQL = """SELECT * FROM transactions WHERE categoria = %s"""
            cursor.execute(_SQL,(transactions[0],))

        elif type_item == "Підкатегорія":
            _SQL = """SELECT name FROM subcategory WHERE id = %s"""
            cursor.execute(_SQL,(item_id,))
            transactions = cursor.fetchone()
            _SQL = """SELECT * FROM transactions WHERE subcategoria = %s"""
            cursor.execute(_SQL,(transactions[0],))
        
        transactions = cursor.fetchall()

        cursor.close()
        dbc.close()
        
        return transactions


    def update_counteragent(self, name, item_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()


        _SQL = """SELECT name FROM counterparties WHERE id = %s"""
        cursor.execute(_SQL,(item_id,))
        counteragent_name = cursor.fetchone()

        _SQL = """UPDATE counterparties SET name = %s WHERE id = %s"""
        cursor.execute(_SQL, (name, item_id,))

        _SQL_transactions = """UPDATE transactions SET counteragent = %s WHERE counteragent = %s"""
        cursor.execute(_SQL_transactions, (name, counteragent_name[0],))

        dbc.commit()
        cursor.close()
        dbc.close()


    def update_category(self, name, item_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT name FROM categories WHERE id = %s"""
        cursor.execute(_SQL,(item_id,))
        category_name = cursor.fetchone()

        _SQL = """UPDATE categories SET name = %s WHERE id = %s"""
        cursor.execute(_SQL, (name, item_id,))

        _SQL_transactions = """UPDATE transactions SET categoria = %s WHERE categoria = %s"""
        cursor.execute(_SQL_transactions, (name, category_name[0],))

        dbc.commit()
        cursor.close()
        dbc.close()


    def update_subcategory(self, name, item_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT name FROM subcategory WHERE id = %s"""
        cursor.execute(_SQL,(item_id,))
        subcategory_name = cursor.fetchone()

        _SQL = """UPDATE subcategory SET name = %s WHERE id = %s"""
        cursor.execute(_SQL, (name, item_id))

        _SQL_transactions = """UPDATE transactions SET subcategoria = %s WHERE subcategoria = %s"""
        cursor.execute(_SQL_transactions, (name, subcategory_name[0],))

        dbc.commit()
        cursor.close()
        dbc.close()


    def delete_counteragent(self, name,item_id):
        name = name.strip()

        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM transactions WHERE counteragent = %s"""
        cursor.execute(_SQL, (name,))
        transactions = cursor.fetchall()

        if transactions:
            cursor.close()
            dbc.close()
            return False

        _SQL = """SELECT * FROM categories WHERE parent_id = %s"""
        cursor.execute(_SQL, (item_id,))
        categories = cursor.fetchall()
        if categories:
            cursor.close()
            dbc.close()
            return False

        _SQL = """DELETE FROM counterparties WHERE id = %s"""
        cursor.execute(_SQL, (item_id,))
        dbc.commit()

        cursor.close()
        dbc.close()
        return True


    def delete_category(self, name, item_id):
        name = name.strip()

        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM subcategory WHERE parent_id IN (SELECT id FROM categories WHERE name = %s)"""
        cursor.execute(_SQL, (name,))
        subcategories = cursor.fetchall()

        if subcategories:
            cursor.close()
            dbc.close()
            return False

        _SQL = """SELECT * FROM transactions WHERE categoria = %s"""
        cursor.execute(_SQL, (name,))
        transactions = cursor.fetchall()

        if transactions:
            cursor.close()
            dbc.close()
            return False

        _SQL = """DELETE FROM categories WHERE id = %s"""
        cursor.execute(_SQL, (item_id,))
        dbc.commit()

        cursor.close()
        dbc.close()
        return True


    def delete_subcategory(self, name,item_id):
        name = name.strip()

        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()


        _SQL = """SELECT * FROM transactions WHERE subcategoria = %s"""
        cursor.execute(_SQL, (name,))
        transactions = cursor.fetchall()

        if transactions:
            cursor.close()
            dbc.close()
            return False


        _SQL = """DELETE FROM subcategory WHERE id = %s"""

        cursor.execute(_SQL,(item_id,))
        dbc.commit()

        cursor.close()
        dbc.close()
        return True


    def add_db_actualy_amount(self, money_type, money):
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'newusername',
            'password': 'newpassword',
            'db': 'home_finances'
        }

        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute("SELECT id FROM actually_type_currency LIMIT 1")
        result = cursor.fetchone()

        if result:

            _SQL = """
                UPDATE actually_type_currency
                SET money_type = %s, money = %s
                WHERE id = %s
            """
            cursor.execute(_SQL, (money_type, money, result[0]))
        else:

            _SQL = """
                INSERT INTO actually_type_currency (money_type, money)
                VALUES (%s, %s)
            """
            cursor.execute(_SQL, (money_type, money))

        dbc.commit()
        cursor.close()
        dbc.close()

        return "SUCCESS"


    def select_actualy_amount(self):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM actually_type_currency"""
        cursor.execute(_SQL)

        result = cursor.fetchone()

        return result


    def add_currency_parsing_left_panel(self,name_currency,type_currency):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO left_panel_dollar(name_currency,type_currency) VALUES(%s,%s)"""
        cursor.execute(_SQL,(name_currency,type_currency,))
        dbc.commit()
        cursor.close()
        dbc.close()
        return "SUCCESS"


    def select_currency_parsing_left_panel(self):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = "SELECT name_currency, type_currency FROM left_panel_dollar"
        cursor.execute(_SQL)

        rows = cursor.fetchall()

        cursor.close()
        dbc.close()

        result = {name: float(rate) for name, rate in rows}

        return result


    def recalculate_left_panel(self, new_base_currency):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        try:
            url = f"https://open.er-api.com/v6/latest/{new_base_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            rates = data.get("rates")
            if not rates:
                return False

        except requests.RequestException:
            return False

        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute("SELECT id, name_currency FROM left_panel_dollar")
        rows = cursor.fetchall()

        for row_id, currency in rows:
            rate = rates.get(currency)
            if rate is None:
                continue

            cursor.execute(
                "UPDATE left_panel_dollar SET type_currency = %s WHERE id = %s",
                (rate, row_id)
            )
        dbc.commit()
        cursor.close()
        dbc.close()

        return True


    def update_main_currency(self, base_currency):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute(
            "UPDATE actually_type_currency SET money = %s WHERE money_type = %s",
            (1, base_currency)
        )

        dbc.commit()
        cursor.close()
        dbc.close()
