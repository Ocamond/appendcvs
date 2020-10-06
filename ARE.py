import pandas as pd
import pyodbc

server = "siemens.cls48i48uap0.us-east-2.rds.amazonaws.com"
database = "test"
username = "admin"
password = "Ocamond200568!"
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username +
                      ';PWD='+password)
cursor = cnxn.cursor()

ARE_list = pd.read_sql_query('SELECT ARE,"Ländercode ISO2 / Country code ISO2" FROM ARE_INFO', cnxn)
ARE_list.columns = ["ARE", "Country Code"]
