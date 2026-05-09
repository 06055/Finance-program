# Personal-Finance-System
Personal-Finance-System — це десктопний фінансовий додаток, створений на Python для ведення фінансового обліку, аналізу даних та роботи з декількома валютами.

Програма дозволяє додавати та зберігати фінансові операції, працювати з валютами, аналізувати статистику та відображати дані через графічний інтерфейс. Для збереження інформації використовується MySQL, а інтерфейс реалізований через Tkinter.

Personal-Finance-System is a desktop financial application built with Python for financial tracking, data analysis, and multi-currency management.

The application allows users to add and store financial operations, work with currencies, analyze statistics, and display information through a graphical interface. MySQL is used for data storage, while the interface is built with Tkinter.

---

# Можливості / Features

- Додавання доходів та витрат  
- Збереження фінансової історії  
- Робота з декількома валютами  
- Основна та вторинні валюти  
- Конвертація валют  
- Побудова графіків та статистики  
- Аналіз фінансових даних  
- Інтерфейс на Tkinter  
- Збереження даних у MySQL  
- MVC-архітектура проєкту  

- Add income and expenses  
- Store financial history  
- Multi-currency support  
- Primary and secondary currencies  
- Currency conversion  
- Charts and statistics  
- Financial data analysis  
- Tkinter graphical interface  
- MySQL database integration  
- MVC project architecture  

---

# Технології / Technologies

## Backend
- Python

## Database
- MySQL

## GUI
- Tkinter

## Libraries
- pandas
- matplotlib
- requests
- pillow
- tkcalendar
- mysql-connector-python
- beautifulsoup4

---

# Архітектура / Architecture

Проєкт побудований на MVC-архітектурі:

- Model — робота з базою даних та логікою
- View — графічний інтерфейс
- Controller — взаємодія між логікою та інтерфейсом

The project is based on MVC architecture:

- Model — database and business logic
- View — graphical user interface
- Controller — interaction between logic and interface

---

# Структура проєкту / Project Structure


```bash
project/
│
├── controllers/
│   └── FinanceController.py
│
├── models/
│   └── FinanceModel.py
│
├── views/
│   └── FinanceView.py
│
├── images/
│   ├── background_card/
│   ├── icons/
│   ├── icons_for_personal_card/
│   └── image_button/
│
├── .vscode/
│   └── settings.json
│
├── README.md
├── home_finances_db.sql
├── main.py
└── README.md
```



# Початок роботи / Getting Started

Перед запуском проєкту виконайте наступні кроки.

Before running the project, complete the following setup steps.

---

## 1. Встановлення залежностей / Install dependencies

```bash
pip install -r requirements.txt
```

Або встановіть бібліотеки вручну:

```bash
pip install pandas matplotlib requests pillow tkcalendar mysql-connector-python beautifulsoup4
```

---

## 2. Налаштування MySQL / Configure MySQL

Створіть базу даних:

```sql
CREATE DATABASE home_finances;
```

Після цього імпортуйте `.sql` файл у MySQL.

After that, import the `.sql` file into MySQL.

---

## 3. Налаштування підключення / Configure database connection

Відкрийте файл конфігурації або `main.py` та змініть параметри підключення до MySQL:

```python
'user': 'your_username',
'password': 'your_password',
'database': 'home_finances'
```

Edit the database connection settings in `main.py` or the config file to match your MySQL configuration.

---

## 4. Запуск проєкту / Run the project

```bash
python main.py
```

Після запуску відкриється графічний інтерфейс програми.

After launch, the graphical application window will open.







# Особливості проєкту / Project Highlights

- Великий Python-проєкт із модульною та структурованою архітектурою  
- Використання MVC-підходу для розділення логіки, інтерфейсу та роботи з даними  
- Інтеграція MySQL для збереження та обробки фінансової інформації  
- Підтримка основної та декількох вторинних валют  
- Побудова графіків, статистики та фінансової аналітики  
- Графічний інтерфейс, створений за допомогою Tkinter  
- Масштабована структура проєкту для подальшого розвитку та підтримки  
- Організація великого Python-коду з поділом на модулі та компоненти  

- Large-scale Python project with modular and structured architecture  
- MVC architecture implementation for separating logic, interface, and data management  
- MySQL integration for storing and processing financial information  
- Support for primary and multiple secondary currencies  
- Charts, statistics, and financial analytics system  
- Graphical user interface built with Tkinter  
- Scalable project structure for future maintenance and expansion  
- Organized large-scale Python codebase with modular components  

---

# Скріншоти / Screenshots

## Робота з валютами / Currency Management

<img width="900" alt="Currency Management" src="https://github.com/user-attachments/assets/b10e3349-5e53-45d3-a991-5b8398468d0d" />

## Аналітика балансу / Balance Analytics

<img width="900" alt="Balance Analytics" src="https://github.com/user-attachments/assets/bf3ed056-b39f-46fc-a3dc-46be756cde36" />

## Таблиця транзакцій / Transactions Table

<img width="900" alt="Transactions Table" src="https://github.com/user-attachments/assets/0e0b9408-e751-42d0-8dc1-60593cf718e8" />

## Дерево категорій та контрагентів / Categories and Counterparties Tree

<img width="900" alt="Categories and Counterparties Tree" src="https://github.com/user-attachments/assets/a61c743c-0037-4940-adc5-1334a550139f" />




# Статус / Status

Проєкт завершений та доступний для подальшого використання і вдосконалення.

The project has been completed and is available for further use and improvements.

---

# Автор / Author

**Vitaly Volokhov**  

GitHub: https://github.com/06055





