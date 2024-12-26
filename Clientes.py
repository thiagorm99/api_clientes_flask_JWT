import sqlite3

class Clientes:
    def __init__(self, db_path='db.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários

    def get_all(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM clientes')
            clientes = cursor.fetchall()
            return [dict(row) for row in clientes]
        except Exception as e:
            return f"Erro ao executar a consulta: {e}"


    def add_client(self, nome, telefone):
        if not nome or not telefone:
            return {"error": "Nome e telefone são obrigatórios"}
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
            self.conn.commit()
            return {"message": "Cliente adicionado com sucesso"}
        except Exception as e:
            return {"error": str(e)}
        

    def edit_client(self, cod, nome, telefone):
        if not nome or not telefone:
            return {"error": "Nome e telefone são obrigatórios"}
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE clientes SET nome = ?, telefone = ? WHERE id = ?", (nome, telefone, cod))
            self.conn.commit()
            if cursor.rowcount == 0:
                return {"error": "Cliente não encontrado"}
            return {"message": "Cliente editado com sucesso"}
        except Exception as e:
            return {"error": str(e)}
        
    def delete_client(self, cod):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cod,))
            self.conn.commit()
            if cursor.rowcount == 0:
                return {"error": "Cliente não encontrado"}
            return {"message": "Cliente deletado com sucesso"}
        except Exception as e:
            return {"error": str(e)}


    def __del__(self):
        if self.conn:
            self.conn.close()
