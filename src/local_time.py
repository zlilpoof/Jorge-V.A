import datetime
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR')

def current_date_formatted():
    return f"{datetime.datetime.now().strftime('%A').capitalize()} {datetime.datetime.now().strftime('%d/%m/%Y')}"

def day_string(day_of_month):
    return datetime.datetime.now().replace(day=day_of_month).strftime('%A').capitalize()

def current_day():
    return datetime.datetime.now().day

def current_month():
    return datetime.datetime.now().month

def current_year():
    return datetime.datetime.now().year

def complete_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def current_hour():
    return datetime.datetime.now().strftime("%H")
