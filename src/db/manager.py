import pymysql

from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USERNAME


class DBManager:
    def __init__(self):
        self.conn = pymysql.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
        )
        self.cursor = self.conn.cursor()
        self.__initiate_table()

    def __initiate_table(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users (ID INT AUTO_INCREMENT PRIMARY KEY, "
                                "username VARCHAR(255), password VARCHAR(255))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS invoice_status (ID INT AUTO_INCREMENT PRIMARY KEY, "
                                "Invoice_Name VARCHAR(255), Status VARCHAR(255), Barcode VARCHAR(255), "
                                "Lieferschein_Nr VARCHAR(255), DTS_Date VARCHAR(255), DTS_Time VARCHAR(255), "
                                "Gewicht VARCHAR(255), Volume VARCHAR(255), Fuhre VARCHAR(255))")

            self.conn.commit()
            self.cursor.execute('SELECT username, password FROM users')
            user_info = self.cursor.fetchall()
            if user_info == ():
                self.cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', ("root", "password123"))
                self.conn.commit()
        except Exception as e:
            self.conn.ping()
            print(e)
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users (ID INT AUTO_INCREMENT PRIMARY KEY, "
                                "username VARCHAR(255), password VARCHAR(255))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS invoice_status (ID INT AUTO_INCREMENT PRIMARY KEY, "
                                "Invoice_Name VARCHAR(255), Status VARCHAR(255), Barcode VARCHAR(255), "
                                "Lieferschein_Nr VARCHAR(255), DTS_Date VARCHAR(255), DTS_Time VARCHAR(255), "
                                "Gewicht VARCHAR(255), Volume VARCHAR(255), Fuhre VARCHAR(255))")

            self.conn.commit()
            self.cursor.execute('SELECT username, password FROM users')
            user_info = self.cursor.fetchall()
            if user_info == ():
                self.cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', ("root", "password123"))
                self.conn.commit()

    @staticmethod
    def convert_tuple_to_list(tuple_value, field_idx):
        c_list = []
        for t_value in tuple_value:
            c_list.append(t_value[field_idx])

        return c_list

    def get_user_info(self, username):
        try:
            self.cursor.execute('SELECT password FROM users WHERE username = %s', username)
        except Exception as e:
            self.conn.ping()
            self.cursor.execute('SELECT password FROM users WHERE username = %s', username)
            print(e)
        info = self.cursor.fetchone()
        if info is not None:
            password = info[0]
        else:
            password = None

        return password

    def get_invoice_status_overview(self):
        try:
            self.cursor.execute('SELECT ID FROM invoice_status')
        except Exception as e:
            self.conn.ping()
            print(e)
            self.cursor.execute('SELECT ID FROM invoice_status')
        processed_info = self.cursor.fetchall()
        try:
            self.cursor.execute('SELECT ID FROM invoice_status WHERE Status = %s', "1")
        except Exception as e:
            self.conn.ping()
            self.cursor.execute('SELECT ID FROM invoice_status WHERE Status = %s', "1")
            print(e)
        validated_info = self.cursor.fetchall()

        return processed_info, validated_info

    def get_validated_status_invoices_name(self, status):
        try:
            self.cursor.execute('SELECT Invoice_Name FROM invoice_status WHERE Status = %s', status)
        except Exception as e:
            self.conn.ping()
            self.cursor.execute('SELECT Invoice_Name FROM invoice_status WHERE Status = %s', status)
            print(e)
        file_info = self.cursor.fetchall()
        file_list = self.convert_tuple_to_list(tuple_value=file_info, field_idx=0)

        return file_list

    def get_processed_invoices_name(self):
        try:
            self.cursor.execute('SELECT Invoice_Name, Status FROM invoice_status')
        except Exception as e:
            self.conn.ping()
            self.cursor.execute('SELECT Invoice_Name, Status FROM invoice_status')
            print(e)
        file_info = self.cursor.fetchall()

        file_list = self.convert_tuple_to_list(tuple_value=file_info, field_idx=0)
        status_list = self.convert_tuple_to_list(tuple_value=file_info, field_idx=1)

        return file_list, status_list

    def get_invoice_info(self, file_name):
        try:
            self.cursor.execute('SELECT Barcode, Lieferschein_Nr, DTS_Date, DTS_Time, Gewicht, Volume, Fuhre '
                                'FROM invoice_status WHERE Invoice_Name = %s', (file_name,))
        except Exception as e:
            self.conn.ping()
            self.cursor.execute('SELECT Barcode, Lieferschein_Nr, DTS_Date, DTS_Time, Gewicht, Volume, Fuhre '
                                'FROM invoice_status WHERE Invoice_Name = %s', (file_name,))
            print(e)
        file_info = self.cursor.fetchone()
        if file_info is not None:
            file_info_list = list(file_info)
        else:
            file_info_list = []

        return file_info_list

    def insert_unprocessed_invoice_result(self, invoice_results):
        for invoice_key in invoice_results.keys():
            saved_invoice_info = self.get_invoice_info(file_name=invoice_key)
            i_result = invoice_results[invoice_key]
            if saved_invoice_info:
                if saved_invoice_info[0] == i_result["Barcode"]:
                    continue
            try:
                self.cursor.execute('INSERT INTO invoice_status (Invoice_Name, Status, Barcode, Lieferschein_Nr, '
                                    'DTS_Date, DTS_Time, Gewicht, Volume, Fuhre) VALUES (%s, %s, %s, %s, %s, %s, %s, '
                                    '%s, %s)', (invoice_key, "0", i_result["Barcode"], i_result["Lieferschein_Nr"],
                                                i_result["DTS_Date"], i_result["DTS_Time"], i_result["Gewicht"],
                                                i_result["Volume"],
                                                i_result["Fuhre"]))
            except Exception as e:
                self.conn.ping()
                self.cursor.execute('INSERT INTO invoice_status (Invoice_Name, Status, Barcode, Lieferschein_Nr, '
                                    'DTS_Date, DTS_Time, Gewicht, Volume, Fuhre) VALUES (%s, %s, %s, %s, %s, %s, %s, '
                                    '%s, %s)', (invoice_key, "0", i_result["Barcode"], i_result["Lieferschein_Nr"],
                                                i_result["DTS_Date"], i_result["DTS_Time"], i_result["Gewicht"],
                                                i_result["Volume"],
                                                i_result["Fuhre"]))
                print(e)
            self.conn.commit()

        return

    def update_status_directly(self, invoice_names):
        for i_name in invoice_names:
            try:
                self.cursor.execute('update invoice_status set Status = %s where Invoice_Name = %s ', ("1", i_name))
            except Exception as e:
                self.conn.ping()
                self.cursor.execute('update invoice_status set Status = %s where Invoice_Name = %s ', ("1", i_name))
                print(e)
            self.conn.commit()

        return

    def update_status_with_info(self, barcode, lieferschein_nr, dts_date, dts_time, gewicht, volume, fuhre,
                                invoice_name):
        try:
            self.cursor.execute('update invoice_status set Status = %s, Barcode = %s, Lieferschein_Nr = %s, DTS_Date '
                                '= %s, DTS_Time = %s, Gewicht = %s, Volume = %s, Fuhre = %s where Invoice_Name = %s ',
                                ("1", barcode, lieferschein_nr, dts_date, dts_time, gewicht, volume, fuhre,
                                 invoice_name))
        except Exception as e:
            self.conn.ping()
            self.cursor.execute('update invoice_status set Status = %s, Barcode = %s, Lieferschein_Nr = %s, DTS_Date '
                                '= %s, DTS_Time = %s, Gewicht = %s, Volume = %s, Fuhre = %s where Invoice_Name = %s ',
                                ("1", barcode, lieferschein_nr, dts_date, dts_time, gewicht, volume, fuhre,
                                 invoice_name))
            print(e)
        self.conn.commit()

        return


if __name__ == '__main__':
    DBManager().get_invoice_info(file_name="Fremdschein (1).pdf")
