import sqlite3


class Database:
	def __init__(self, path):
		self.connection = sqlite3.connect(path)
		self.cursor = self.conn.cursor()
		self.__create_table("main", ["image", "throttling", "angle", "time"], ["blob", "double", "double", "datetime"])

	def __create_table(self, table_name, column_names, column_types):
		if len(column_names) != len(column_types):
			raise()

		sql_query = "DROP TABLE IF EXISTS " + table_name + "; CREATE TABLE " + table_name + " ("
		for i in range(0, len(column_names)):
			sql_query += column_names[i] + " " + column_types[i] + ","

		sql_query[:-1] = ")"

		try:
			self.cursor.execute(sql_query)
			self.connection.commit()
		finally:
			self.close()

	def save_record(self, image, throttling, turn_angle):
		sql_query = "INSERT INTO main VALUES(?, ?, ?, datetime('now');"
		self.cursor.execute(sql_query, [sqlite3.Binary(image), throttling, turn_angle])
		self.connection.commit()

	def close(self):
		self.connection.close()

