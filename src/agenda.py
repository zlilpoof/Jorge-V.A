import mysql.connector

def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="jorge"
        )
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS compromissos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            dia INT,
            mes INT,
            hora INT,
            descricao VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {str(e)}")

def registrar_compromisso(dia, mes, hora, compromisso):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        query = "INSERT INTO compromissos (dia, mes, hora, descricao) VALUES (%s, %s, %s, %s)"
        values = (dia, mes, hora, compromisso)
        cursor.execute(query, values)
        
        conn.commit()
        cursor.close()
        conn.close()
        return "Compromisso registrado com sucesso "
    except Exception as e:
        return f"Erro ao registrar compromisso {str(e)}"

def listar_compromissos_por_dia_mes(dia_especifico, mes_especifico):
    compromissos_do_dia_mes = []
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = "SELECT id, dia, mes, hora, descricao FROM compromissos WHERE dia = %s AND mes = %s"
        cursor.execute(query, (dia_especifico, mes_especifico))

        for id_compromisso, dia, mes, hora, descricao in cursor.fetchall():
            compromissos_do_dia_mes.append(f"{id_compromisso}: Dia {dia} do Mês {mes}, às {hora} horas: {descricao}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao listar compromissos do dia {dia_especifico} do mês {mes_especifico}: {str(e)}")

    return compromissos_do_dia_mes

def listar_compromissos():
    compromissos = []
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = "SELECT id, dia, mes, hora, descricao FROM compromissos"
        cursor.execute(query)

        for id_compromisso, dia, mes, hora, descricao in cursor.fetchall():
            compromissos.append(f"{id_compromisso}: Dia {dia} do Mês {mes}, as {hora} horas: {descricao}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao listar compromissos: {str(e)}")

    return compromissos

def deletar_compromisso_por_id(id_compromisso):
    compromissos_modificados = False
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = "DELETE FROM compromissos WHERE id = %s"
        values = (id_compromisso,)
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            compromissos_modificados = True
            conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao deletar compromissos: {str(e)}")

    return compromissos_modificados

def deletar_compromisso_por_dia(dia_compromisso):
    compromissos_modificados = False
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = "DELETE FROM compromissos WHERE dia = %s"
        values = (dia_compromisso,)
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            compromissos_modificados = True
            conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao deletar compromissos: {str(e)}")

    return compromissos_modificados