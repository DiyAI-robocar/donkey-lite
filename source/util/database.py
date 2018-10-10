import sqlite3


class Database:
    def __init__(self, path: str, col_names: list, col_data_types: list) -> None:
        """
        Constructor
        :param path: Path to the SQLite database
        :param col_names: Names of the columns
        :param col_data_types: Data types of the columns
        :return: Void function
        """
        self.connection = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.__create_table("main", col_names + ["timestamp"], col_data_types + ["datetime"])

    def __create_table(self, table_name: str, column_names: list, column_types: list) -> None:
        """
        Create the table in the SQLite database
        :param table_name: name of the table
        :param column_names: columns names
        :param column_types: data types of the columns
        :return:
        """
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

    def save_record(self, image: object, throttling: float, turn_angle: float) -> None:
        """
        Save the image and the values from the controller
        :param image: Image
        :param throttling: The value of the throttling
        :param turn_angle: The value of the turn angle
        :return: Void function
        """
        sql_query = "INSERT INTO main VALUES(?, ?, ?, datetime('now');"
        self.cursor.execute(sql_query, [sqlite3.Binary(image), throttling, turn_angle])
        self.connection.commit()

    def close(self) -> None:
        """
        Close the connection to the database
        :return: Void function
        """
        self.connection.close()
