import mysql.connector
from datetime import datetime
from tkinter import messagebox
import re
import requests
 
class FinanceModel:
    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
    default_currency_codes = ("USD", "EUR", "UAH", "GBP", "PLN")
    default_rates_to_usd = {
        "USD": 1.0,
        "EUR": 1.08,
        "UAH": 0.025,
        "GBP": 1.27,
        "PLN": 0.25
    }
    rates_cache = {}

    @staticmethod
    def connect_db():
        return mysql.connector.connect(**FinanceModel.dbconfig)

    @staticmethod
    def get_table_columns(cursor, table_name):
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        return {row[0]: row for row in cursor.fetchall()}

    @staticmethod
    def get_currency_column(columns):
        for column in ("money_type", "currency", "name_currency", "currency_code", "name"):
            if column in columns:
                return column
        return None

    @staticmethod
    def get_secondary_pair_columns(columns):
        possible_pairs = (
            ("currency1", "currency2"),
            ("currency_1", "currency_2"),
            ("currency_a", "currency_b"),
            ("first_currency", "second_currency"),
            ("first_secondary_currency", "second_secondary_currency"),
            ("secondary_currency_1", "secondary_currency_2"),
        )
        for first_column, second_column in possible_pairs:
            if first_column in columns and second_column in columns:
                return first_column, second_column
        return None

    @staticmethod
    def get_secondary_role_column(columns):
        for column in ("role", "currency_role", "slot", "position", "number", "type"):
            if column in columns:
                return column
        return None

    @staticmethod
    def complete_secondary_currencies(user_id, secondary, save=False):
        main_currency = FinanceModel.get_main_currency(user_id)
        result = [
            currency for currency in FinanceModel.unique_currencies(secondary)
            if currency != main_currency
        ]

        if len(result) < 2:
            candidates = FinanceModel.get_left_panel_currency_codes(user_id) + list(FinanceModel.default_currency_codes)
            for currency in candidates:
                currency = FinanceModel.normalize_currency(currency)
                if currency and currency != main_currency and currency not in result:
                    result.append(currency)
                if len(result) == 2:
                    break

        result = result[:2]
        if save and len(result) == 2:
            try:
                FinanceModel.set_secondary_currencies(user_id, result[0], result[1])
            except Exception:
                pass

        return result

    @staticmethod
    def normalize_currency(currency):
        if currency is None:
            return None
        currency = str(currency).strip().upper()
        return currency or None

    @staticmethod
    def unique_currencies(currencies):
        result = []
        for currency in currencies:
            currency = FinanceModel.normalize_currency(currency)
            if currency and currency not in result:
                result.append(currency)
        return result

    @staticmethod
    def get_main_currency(user_id=None):
        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "actually_type_currency")
            currency_column = FinanceModel.get_currency_column(columns)
            if not currency_column:
                return "USD"

            params = []
            query = f"SELECT `{currency_column}` FROM actually_type_currency"
            if "user_id" in columns and user_id is not None:
                query += " WHERE user_id = %s"
                params.append(user_id)
            query += " ORDER BY id LIMIT 1"

            cursor.execute(query, tuple(params))
            result = cursor.fetchone()
            if result and result[0]:
                return FinanceModel.normalize_currency(result[0])
            return "USD"
        finally:
            cursor.close()
            dbc.close()

    @staticmethod
    def set_main_currency(user_id, currency):
        currency = FinanceModel.normalize_currency(currency)
        if not currency:
            raise ValueError("Основна валюта не вибрана")

        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "actually_type_currency")
            currency_column = FinanceModel.get_currency_column(columns)
            if not currency_column:
                raise ValueError("У таблиці actually_type_currency не знайдено колонку валюти")

            params = []
            select_query = "SELECT id FROM actually_type_currency"
            if "user_id" in columns and user_id is not None:
                select_query += " WHERE user_id = %s"
                params.append(user_id)
            select_query += " ORDER BY id LIMIT 1"
            cursor.execute(select_query, tuple(params))
            result = cursor.fetchone()

            if result:
                set_parts = [f"`{currency_column}` = %s"]
                update_params = [currency]
                if "money" in columns:
                    set_parts.append("money = %s")
                    update_params.append(1)
                if "name" in columns and currency_column != "name":
                    set_parts.append("name = %s")
                    update_params.append("Основна")

                update_query = f"UPDATE actually_type_currency SET {', '.join(set_parts)} WHERE id = %s"
                update_params.append(result[0])
                cursor.execute(update_query, tuple(update_params))
            else:
                insert_columns = []
                insert_values = []

                if "user_id" in columns and user_id is not None:
                    insert_columns.append("user_id")
                    insert_values.append(user_id)
                if "name" in columns and currency_column != "name":
                    insert_columns.append("name")
                    insert_values.append("Основна")
                insert_columns.append(currency_column)
                insert_values.append(currency)
                if "money" in columns:
                    insert_columns.append("money")
                    insert_values.append(1)

                placeholders = ", ".join(["%s"] * len(insert_columns))
                fields = ", ".join(f"`{column}`" for column in insert_columns)
                cursor.execute(
                    f"INSERT INTO actually_type_currency ({fields}) VALUES ({placeholders})",
                    tuple(insert_values)
                )

            dbc.commit()
            return "SUCCESS"
        finally:
            cursor.close()
            dbc.close()

    @staticmethod
    def get_secondary_currencies(user_id=None):
        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "secondary_currencies")
            pair_columns = FinanceModel.get_secondary_pair_columns(columns)

            params = []
            where = ""
            if "user_id" in columns and user_id is not None:
                where = " WHERE user_id = %s"
                params.append(user_id)

            if pair_columns:
                first_column, second_column = pair_columns
                cursor.execute(
                    f"SELECT `{first_column}`, `{second_column}` FROM secondary_currencies{where} ORDER BY id LIMIT 1",
                    tuple(params)
                )
                result = cursor.fetchone()
                if result:
                    return FinanceModel.complete_secondary_currencies(user_id, result, save=True)
                return FinanceModel.complete_secondary_currencies(user_id, [], save=True)

            currency_column = FinanceModel.get_currency_column(columns)
            if not currency_column:
                return []

            role_column = FinanceModel.get_secondary_role_column(columns)
            order_by = f"`{role_column}`" if role_column else "id"
            cursor.execute(
                f"SELECT `{currency_column}` FROM secondary_currencies{where} ORDER BY {order_by}, id LIMIT 2",
                tuple(params)
            )
            currencies = FinanceModel.unique_currencies(row[0] for row in cursor.fetchall())
            return FinanceModel.complete_secondary_currencies(user_id, currencies, save=True)
        except mysql.connector.Error:
            return FinanceModel.complete_secondary_currencies(user_id, [], save=False)
        finally:
            cursor.close()
            dbc.close()

    @staticmethod
    def get_required_insert_value(column, index, currency, role, user_id):
        if column == "user_id":
            return user_id
        if column in ("role", "currency_role", "slot", "position", "number", "type"):
            return index
        if column == "money":
            return 1
        if column == "name":
            return role
        if "currency" in column:
            return currency
        return ""

    @staticmethod
    def set_secondary_currencies(user_id, currency1, currency2):
        currency1 = FinanceModel.normalize_currency(currency1)
        currency2 = FinanceModel.normalize_currency(currency2)
        main_currency = FinanceModel.get_main_currency(user_id)

        if not currency1 or not currency2:
            raise ValueError("Потрібно вибрати дві вторинні валюти")
        if currency1 == currency2:
            raise ValueError("Вторинні валюти не можуть бути однаковими")
        if main_currency in (currency1, currency2):
            raise ValueError("Основна валюта не може бути вторинною")

        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "secondary_currencies")
            pair_columns = FinanceModel.get_secondary_pair_columns(columns)

            params = []
            select_query = "SELECT id FROM secondary_currencies"
            if "user_id" in columns and user_id is not None:
                select_query += " WHERE user_id = %s"
                params.append(user_id)
            select_query += " ORDER BY id LIMIT 1"

            if pair_columns:
                first_column, second_column = pair_columns
                cursor.execute(select_query, tuple(params))
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        f"UPDATE secondary_currencies SET `{first_column}` = %s, `{second_column}` = %s WHERE id = %s",
                        (currency1, currency2, result[0])
                    )
                else:
                    insert_columns = []
                    insert_values = []
                    if "user_id" in columns and user_id is not None:
                        insert_columns.append("user_id")
                        insert_values.append(user_id)
                    insert_columns.extend([first_column, second_column])
                    insert_values.extend([currency1, currency2])

                    fields = ", ".join(f"`{column}`" for column in insert_columns)
                    placeholders = ", ".join(["%s"] * len(insert_columns))
                    cursor.execute(
                        f"INSERT INTO secondary_currencies ({fields}) VALUES ({placeholders})",
                        tuple(insert_values)
                    )
            else:
                currency_column = FinanceModel.get_currency_column(columns)
                if not currency_column:
                    raise ValueError("У таблиці secondary_currencies не знайдено колонку валюти")

                if "user_id" in columns and user_id is not None:
                    cursor.execute("DELETE FROM secondary_currencies WHERE user_id = %s", (user_id,))
                else:
                    cursor.execute("DELETE FROM secondary_currencies")

                role_column = FinanceModel.get_secondary_role_column(columns)
                for index, (role, currency) in enumerate((("2A", currency1), ("2B", currency2)), start=1):
                    insert_columns = []
                    insert_values = []

                    if "user_id" in columns and user_id is not None:
                        insert_columns.append("user_id")
                        insert_values.append(user_id)
                    if role_column:
                        insert_columns.append(role_column)
                        column_type = str(columns[role_column][1]).lower()
                        insert_values.append(index if "int" in column_type else role)

                    insert_columns.append(currency_column)
                    insert_values.append(currency)

                    for column, info in columns.items():
                        extra = str(info[5]).lower() if len(info) > 5 else ""
                        is_required = info[2] == "NO" and info[4] is None
                        if column in insert_columns or "auto_increment" in extra or not is_required:
                            continue
                        insert_columns.append(column)
                        insert_values.append(
                            FinanceModel.get_required_insert_value(column, index, currency, role, user_id)
                        )

                    fields = ", ".join(f"`{column}`" for column in insert_columns)
                    placeholders = ", ".join(["%s"] * len(insert_columns))
                    cursor.execute(
                        f"INSERT INTO secondary_currencies ({fields}) VALUES ({placeholders})",
                        tuple(insert_values)
                    )

            dbc.commit()
            return "SUCCESS"
        finally:
            cursor.close()
            dbc.close()

    @staticmethod
    def get_left_panel_currency_codes(user_id=None):
        try:
            currencies = FinanceModel.select_currency_parsing_left_panel(user_id)
            return list(currencies.keys())
        except Exception:
            return []

    @staticmethod
    def get_available_currencies(user_id=None):
        main_currency = FinanceModel.get_main_currency(user_id)
        secondary = FinanceModel.get_secondary_currencies(user_id)
        currencies = FinanceModel.unique_currencies([main_currency] + secondary)

        if len(currencies) < 3:
            candidates = FinanceModel.get_left_panel_currency_codes(user_id) + list(FinanceModel.default_currency_codes)
            for currency in candidates:
                currency = FinanceModel.normalize_currency(currency)
                if currency and currency != main_currency and currency not in currencies:
                    currencies.append(currency)
                if len(currencies) == 3:
                    break

        if len(currencies) >= 3:
            secondary = [currency for currency in currencies[1:3] if currency != main_currency]
            if len(secondary) == 2:
                try:
                    FinanceModel.set_secondary_currencies(user_id, secondary[0], secondary[1])
                except Exception:
                    pass

        return currencies[:3]

    @staticmethod
    def fetch_conversion_rate(from_currency, to_currency):
        from_currency = FinanceModel.normalize_currency(from_currency)
        to_currency = FinanceModel.normalize_currency(to_currency)
        if not from_currency or not to_currency:
            return None
        if from_currency == to_currency:
            return 1.0

        cache_key = (from_currency, to_currency)
        if cache_key in FinanceModel.rates_cache:
            return FinanceModel.rates_cache[cache_key]

        try:
            url = f"https://open.er-api.com/v6/latest/{from_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data.get("rates", {}).get(to_currency)
            if rate is None:
                return None
            rate = float(rate)
            FinanceModel.rates_cache[cache_key] = rate
            return rate
        except requests.RequestException:
            return None

    @staticmethod
    def get_default_conversion_rate(from_currency, to_currency):
        from_currency = FinanceModel.normalize_currency(from_currency)
        to_currency = FinanceModel.normalize_currency(to_currency)
        from_rate = FinanceModel.default_rates_to_usd.get(from_currency)
        to_rate = FinanceModel.default_rates_to_usd.get(to_currency)
        if not from_rate or not to_rate:
            return None
        return from_rate / to_rate

    @staticmethod
    def convert_currency(amount, from_currency, to_currency):
        try:
            amount = float(amount or 0)
        except (TypeError, ValueError):
            amount = 0

        from_currency = FinanceModel.normalize_currency(from_currency)
        to_currency = FinanceModel.normalize_currency(to_currency)
        if not from_currency or not to_currency or from_currency == to_currency:
            return amount

        rate = FinanceModel.fetch_conversion_rate(from_currency, to_currency)
        if rate is None:
            rate = FinanceModel.get_default_conversion_rate(from_currency, to_currency)
        if rate is None:
            return amount
        return amount * rate

    @staticmethod
    def select_card_balances_with_currency(user_id):
        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            cursor.execute(
                "SELECT count_money, type_currency FROM pocket WHERE user_id = %s",
                (user_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            dbc.close()

    @staticmethod
    def get_total_balance_in_main_currency(user_id):
        main_currency = FinanceModel.get_main_currency(user_id)
        cards = FinanceModel.select_card_balances_with_currency(user_id)
        total = 0

        for balance, currency in cards:
            total += FinanceModel.convert_currency(balance, currency, main_currency)

        return total, main_currency

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
        dbconfig = FinanceModel.dbconfig
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT name, count_money, type_currency FROM pocket WHERE user_id = %s"""
        cursor.execute(_SQL, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        dbc.close()

        main_currency = FinanceModel.get_main_currency(user_id)
        cards = []
        for name, balance, currency in result:
            balance = FinanceModel.convert_currency(balance, currency, main_currency)
            cards.append((name, float(balance)))
        return cards



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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO counterparties (name,user_id) VALUES (%s,%s)"""
        cursor.execute(_SQL, (name,user_id,))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_counterparties(user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO categories (name, parent_id, user_id) VALUES (%s, %s, %s)"""
        cursor.execute(_SQL, (name, parent_id, user_id,))
        dbc.commit()

        cursor.close()
        dbc.close()


    
    @staticmethod
    def select_category(user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO subcategory (name, parent_id, user_id) VALUES (%s, %s, %s)"""
        cursor.execute(_SQL, (name, parent_id, user_id))
        dbc.commit()

        cursor.close()
        dbc.close()


    @staticmethod
    def select_subcategory(user_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id, counteragent, categoria, subcategoria, type_transaction, count, currency, card, data FROM transactions WHERE user_id = %s"""
        cursor.execute(_SQL,(user_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()
        return result

    def is_card_name_exist(self, name):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT * FROM transactions WHERE id = %s"""
        
        cursor.execute(_SQL,(id_tr,))
        result = cursor.fetchall()

        
        cursor.close()
        dbc.close()
        return result[0]
    

    @staticmethod
    def select_card_currency_for_balance(cursor, card_name, user_id=None):
        if user_id is None:
            cursor.execute(
                "SELECT type_currency FROM pocket WHERE name = %s LIMIT 1",
                (card_name,)
            )
        else:
            cursor.execute(
                "SELECT type_currency FROM pocket WHERE name = %s AND user_id = %s LIMIT 1",
                (card_name, user_id)
            )

        result = cursor.fetchone()
        if result:
            return result[0]
        return None


    @staticmethod
    def update_card_balance_delta(cursor, card_name, amount, amount_currency, user_id=None):
        card_currency = FinanceModel.select_card_currency_for_balance(cursor, card_name, user_id)
        if not card_currency:
            return

        converted_amount = FinanceModel.convert_currency(amount, amount_currency, card_currency)

        if user_id is None:
            cursor.execute(
                "UPDATE pocket SET count_money = count_money + %s WHERE name = %s",
                (converted_amount, card_name)
            )
        else:
            cursor.execute(
                "UPDATE pocket SET count_money = count_money + %s WHERE name = %s AND user_id = %s",
                (converted_amount, card_name, user_id)
            )


    @staticmethod
    def update_transaction_info(id_tr, counteragent, category, subcategory, type_transaction, amount, currency, choisecard_menu, date, selected_before_card, user_id=None):
        dbconfig = FinanceModel.dbconfig
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        amount = float(amount)

        cursor.execute("SELECT count, currency, card, user_id FROM transactions WHERE id = %s", (id_tr,))
        previous_transaction = cursor.fetchone()
        if not previous_transaction:
            cursor.close()
            dbc.close()
            return

        previous_amount = float(previous_transaction[0])
        previous_currency = previous_transaction[1]
        previous_card = previous_transaction[2] or selected_before_card
        transaction_user_id = previous_transaction[3]
        if user_id is None:
            user_id = transaction_user_id
        
        if type_transaction.lower() == "витрата":
            amount = -abs(amount)
        else:
            amount = abs(amount)

        FinanceModel.update_card_balance_delta(
            cursor,
            previous_card,
            -previous_amount,
            previous_currency,
            user_id
        )

        FinanceModel.update_card_balance_delta(
            cursor,
            choisecard_menu,
            amount,
            currency,
            user_id
        )

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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """SELECT id, name FROM categories WHERE parent_id = %s"""
        cursor.execute(_SQL, (counterpart_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()

        return result


    def select_subcategories_by_category(self,category_id):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        
        _SQL = """SELECT id, name FROM subcategory WHERE parent_id = %s"""
        cursor.execute(_SQL, (category_id,))
        result = cursor.fetchall()

        cursor.close()
        dbc.close()

        return result


    def delete_transaction(self,transaction_id):
        dbconfig = FinanceModel.dbconfig
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        cursor.execute("SELECT count, currency, card, user_id FROM transactions WHERE id = %s", (transaction_id,))
        result = cursor.fetchone()

        if result:
            amount, currency, card_name, user_id = result
            amount = float(amount)

            FinanceModel.update_card_balance_delta(
                cursor,
                card_name,
                -amount,
                currency,
                user_id
            )

            _SQL = """DELETE FROM transactions WHERE id = %s"""
            cursor.execute(_SQL, (transaction_id,))
            dbc.commit()

        cursor.close()
        dbc.close()



    def check_for_transactions(self,item_id, type_item):
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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

        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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

        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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

        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'home_finances'}
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
        return FinanceModel.set_main_currency(None, money_type)


    def select_actualy_amount(self):
        currency = FinanceModel.get_main_currency()
        return (None, currency, 1)


    def add_currency_parsing_left_panel(self,name_currency,type_currency,user_id=None):
        name_currency = FinanceModel.normalize_currency(name_currency)
        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "left_panel_dollar")
            currency_column = "name_currency" if "name_currency" in columns else FinanceModel.get_currency_column(columns)
            rate_column = "type_currency" if "type_currency" in columns else ("rate" if "rate" in columns else None)
            if not currency_column or not rate_column:
                return "NO_COLUMNS"

            params = [name_currency]
            select_query = f"SELECT id FROM left_panel_dollar WHERE `{currency_column}` = %s"
            if "user_id" in columns and user_id is not None:
                select_query += " AND user_id = %s"
                params.append(user_id)
            select_query += " LIMIT 1"
            cursor.execute(select_query, tuple(params))
            result = cursor.fetchone()

            if result:
                cursor.execute(
                    f"UPDATE left_panel_dollar SET `{rate_column}` = %s WHERE id = %s",
                    (type_currency, result[0])
                )
            else:
                insert_columns = []
                insert_values = []
                if "user_id" in columns and user_id is not None:
                    insert_columns.append("user_id")
                    insert_values.append(user_id)
                insert_columns.extend([currency_column, rate_column])
                insert_values.extend([name_currency, type_currency])

                fields = ", ".join(f"`{column}`" for column in insert_columns)
                placeholders = ", ".join(["%s"] * len(insert_columns))
                cursor.execute(
                    f"INSERT INTO left_panel_dollar ({fields}) VALUES ({placeholders})",
                    tuple(insert_values)
                )

            dbc.commit()
            return "SUCCESS"
        except mysql.connector.Error:
            return "NO_TABLE"
        finally:
            cursor.close()
            dbc.close()


    def select_currency_parsing_left_panel(self,user_id=None):
        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "left_panel_dollar")
            currency_column = "name_currency" if "name_currency" in columns else FinanceModel.get_currency_column(columns)
            rate_column = "type_currency" if "type_currency" in columns else ("rate" if "rate" in columns else None)
            if not currency_column or not rate_column:
                return {}

            params = []
            query = f"SELECT `{currency_column}`, `{rate_column}` FROM left_panel_dollar"
            if "user_id" in columns and user_id is not None:
                query += " WHERE user_id = %s"
                params.append(user_id)

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            result = {}
            for name, rate in rows:
                name = FinanceModel.normalize_currency(name)
                if not name:
                    continue
                try:
                    result[name] = float(rate)
                except (TypeError, ValueError):
                    pass
            return result
        except mysql.connector.Error:
            return {}
        finally:
            cursor.close()
            dbc.close()


    def recalculate_left_panel(self,new_base_currency,user_id=None):
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

        return FinanceModel.update_left_panel_rates(rates, user_id)


    def update_left_panel_rates(self,rates: dict,user_id=None):
        dbc = FinanceModel.connect_db()
        cursor = dbc.cursor()
        try:
            columns = FinanceModel.get_table_columns(cursor, "left_panel_dollar")
            currency_column = "name_currency" if "name_currency" in columns else FinanceModel.get_currency_column(columns)
            rate_column = "type_currency" if "type_currency" in columns else ("rate" if "rate" in columns else None)
            if not currency_column or not rate_column:
                return False

            params = []
            query = f"SELECT id, `{currency_column}` FROM left_panel_dollar"
            if "user_id" in columns and user_id is not None:
                query += " WHERE user_id = %s"
                params.append(user_id)
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

            for row_id, currency in rows:
                currency = FinanceModel.normalize_currency(currency)
                rate = rates.get(currency)
                if rate is None:
                    continue
                cursor.execute(
                    f"UPDATE left_panel_dollar SET `{rate_column}` = %s WHERE id = %s",
                    (rate, row_id)
                )
            dbc.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            dbc.close()


    def update_main_currency(self,base_currency):
        return FinanceModel.set_main_currency(None, base_currency)
