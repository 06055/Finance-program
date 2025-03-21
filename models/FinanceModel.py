import mysql.connector
import re



class FinanceModel:
    @staticmethod
    def model_registration(name, gmail, password, password_repeat):
        if name != '' and name != None:
            if gmail != '' and gmail != None:
                if password != '' and password != None and password_repeat != '' and password_repeat != None:
                    if password == password_repeat:

                        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
                        dbc = mysql.connector.connect(**dbconfig)
                        cursor = dbc.cursor()
                        _SQL = f"""SELECT gmail FROM user WHERE gmail = '{gmail}' """
                        cursor.execute(_SQL)
                        gmail_sql = cursor.fetchone()

                        if gmail_sql == None:
                            _SQL = """INSERT INTO user(name,gmail,password) VALUES(%s,%s,Sha1(%s))"""
                            cursor.execute(_SQL,(name,gmail,password,))
                            dbc.commit()
                            return "Успешная реестрация"
                        else:return 'Почта занята'
                    else:return "Пароль не совпадает"
        else:return "Ошибка"


    @staticmethod
    def model_logining(gmail, password):
        if gmail != None and gmail != '':
            
            if password != None and gmail != '':
                dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
                dbc = mysql.connector.connect(**dbconfig)
                cursor = dbc.cursor()
                _SQL = """SELECT name FROM user WHERE gmail = %s and password = Sha1(%s)"""
                cursor.execute(_SQL,(gmail,password))
                result = cursor.fetchone()

                cursor.close()
                dbc.close()
                if result != None:
                    return 'Yes'

                else:
                    return 'Почта или пароль были введены не правильно'


    @staticmethod
    def add_new_card(name_card,type_card,balance_card,selected_currency,selected_file_or_color,full_date):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        if '/' in selected_file_or_color  or ':' in selected_file_or_color:
            _SQL = """INSERT INTO pocket(name,type_pocket,type_currency,data_made,count_money,bg_picture) VALUES(%s,%s,%s,%s,%s,%s)"""
        else:
            _SQL = """INSERT INTO pocket(name,type_pocket,type_currency,data_made,count_money,bg_color) VALUES(%s,%s,%s,%s,%s,%s)"""

        cursor.execute(_SQL,(name_card,type_card,selected_currency,full_date,balance_card,selected_file_or_color))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_cars_all():
        list_cards = list()
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT * FROM pocket"""
        cursor.execute(_SQL)

        result = cursor.fetchall()
        for i in result:
            list_cards.append(i)
        return list_cards


    @staticmethod
    def select_cars():
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT name FROM pocket"""  
        cursor.execute(_SQL)
        result = cursor.fetchall()
        cursor.close()
        dbc.close()
        return [row[0] for row in result]  


    @staticmethod
    def select_currency_by_card(card_name):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT type_currency FROM pocket WHERE name = %s"""
        cursor.execute(_SQL, (card_name,))
        result = cursor.fetchone()
        cursor.close()
        dbc.close()
        if result:
            return result[0]
        return None
    

    @staticmethod
    def add_counterparty(name):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO counterparties (name) VALUES (%s)"""
        cursor.execute(_SQL, (name,))
        dbc.commit()

        cursor.close()
        dbc.close()

    @staticmethod
    def select_counterparties():
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM counterparties"""
        cursor.execute(_SQL)
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def add_category(name, parent_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO categories (name, parent_id) VALUES (%s, %s)"""
        cursor.execute(_SQL, (name, parent_id))
        dbc.commit()

        cursor.close()
        dbc.close()


    
    @staticmethod
    def select_category():
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM categories"""
        cursor.execute(_SQL)
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result
    

    @staticmethod
    def select_category_for_subcategory():
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id,name FROM categories"""
        cursor.execute(_SQL)
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def add_subcategory(name,parent_id):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO subcategory (name, parent_id) VALUES (%s, %s)"""
        cursor.execute(_SQL, (name, parent_id))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_subcategory():
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM subcategory"""
        cursor.execute(_SQL)
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def add_transaction(counteragent, category, subcategory, type_transaction, amount, currency, card, date):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        try:
            amount = float(amount)
            if type_transaction.lower() == "расход":
                amount = -abs(amount)
            else:
                amount = abs(amount)
            _SQL = """
            INSERT INTO transactions 
            (counteragent, categoria, subcategoria, type_transaction, count, currency, card, data) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(_SQL, (counteragent, category, subcategory, type_transaction, amount, currency, card, date))

            _SQL_UPDATE_BALANCE = "UPDATE pocket SET count_money = count_money + %s WHERE name = %s"
            cursor.execute(_SQL_UPDATE_BALANCE, (amount, card))

            dbc.commit()

        except ValueError:
            print("Ошибка: 'amount' должно быть числом.")
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")
        finally:
            cursor.close()
            dbc.close()


    @staticmethod
    def select_transaction():
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM transactions"""
        cursor.execute(_SQL)
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result


    @staticmethod
    def select_transaction_personal_id(card_id):
        
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT name FROM pocket WHERE id = %s"""
        
        cursor.execute(_SQL,(card_id,))
        name_card = cursor.fetchone()

        _SQL = """SELECT * FROM transactions WHERE card = %s"""
        cursor.execute(_SQL,(name_card[0],))
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
    def update_transaction_info(id_tr,counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, selected_before_card):
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'db': 'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        amount = float(amount)
        if type_transaction.lower() == "расход":
            amount = -abs(amount)
            if selected_before_card != choisecard_menu:
                onlyamount = abs(amount)
                _SQL = """UPDATE pocket SET count_money = count_money + %s WHERE name = %s"""
                cursor.execute(_SQL, (onlyamount, selected_before_card))
                dbc.commit()
        else:
            amount = abs(amount)
            if selected_before_card != choisecard_menu:
                _SQL = """UPDATE pocket SET count_money = count_money - %s WHERE name = %s"""
                cursor.execute(_SQL, (amount, selected_before_card))
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

        


        _SQL = """UPDATE pocket SET count_money = count_money + %s WHERE name = %s"""
        cursor.execute(_SQL, (amount, choisecard_menu))
        dbc.commit()

        cursor.close()
        dbc.close()
    