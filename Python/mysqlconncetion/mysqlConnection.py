import mysql.connector
import contextlib
from jupyter_server.auth import passwd

@contextlib.contextmanager
def get_db(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    if connection.is_connected():
        print("DB Connected :", connection.is_connected())

    else:
        print(connection.is_connected())
        print("Unable to connect to MySQL database")
    coursor = connection.cursor()
    yield coursor
    if commit:
        connection.commit()
    coursor.close()
    connection.close()

def fetch_data():
    with get_db() as coursor:
        coursor.execute("select * from expenses")
        for row in coursor.fetchall():
            print(row)


def expenses_for_date(dt):
    with get_db() as coursor:
        coursor.execute("select * from expenses where expense_date=%s", (dt,))
        for row in coursor.fetchall():
            print(row)

def add_expense(expense):
    with get_db(commit=True) as coursor:
        try:
            coursor.execute("insert into expenses (expense_date,amount,category,notes) values (%s, %s, %s, %s)", (expense[0], expense[1], expense[2], expense[3]))
        except mysql.connector.Error as err:
            print(err)
        except Exception as err:
            print(err)

if __name__ == "__main__":
    #fetch_data()
    #expenses_for_date("2024-09-30")
    add_expense(["2024-09-29","73","Other","Test2"])


