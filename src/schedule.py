import mysql.connector
import config

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database=f"{config.assistant_name}"
        )
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            day INT,
            month INT,
            hour INT,
            appointment VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {str(e)}")

def register_appointment(day, month, hour, appointment):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO appointments (day, month, hour, appointment) VALUES (%s, %s, %s, %s)"
        values = (day, month, hour, appointment)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "Compromisso registrado com sucesso "
    except Exception as e:
        return f"Erro ao registrar compromisso {str(e)}"

def list_appointments_with_day_and_month(day, month):
    appointment_of_day_and_month = []
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT id, day, month, hour, appointment FROM appointments WHERE day = %s AND month = %s"
        cursor.execute(query, (day, month))

        for id, day, month, hour, appointment in cursor.fetchall():
            appointment_of_day_and_month.append(f"{id}: Dia {day} do Mês {month}, às {hour} horas: {appointment}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao listar compromissos do dia {day} do mês {month}: {str(e)}")
    return appointment_of_day_and_month

def list_appointments():
    appointments = []
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT id, day, month, hour, appointment FROM appointments"
        cursor.execute(query)

        for id, day, month, hour, appointment in cursor.fetchall():
            appointments.append(f"{id}: Dia {day} do Mês {month}, as {hour} horas: {appointment}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao listar compromissos: {str(e)}")
    return appointments

def delete_appointment_by_id(id):
    modified_appointments = False
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "DELETE FROM appointments WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        if cursor.rowcount > 0:
            modified_appointments = True
            conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao deletar compromissos: {str(e)}")
    return modified_appointments

def delete_appointment_by_day(day):
    modified_appointments = False
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "DELETE FROM appointments WHERE day = %s"
        values = (day,)
        cursor.execute(query, values)
        if cursor.rowcount > 0:
            modified_appointments = True
            conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao deletar compromissos: {str(e)}")
    return modified_appointments