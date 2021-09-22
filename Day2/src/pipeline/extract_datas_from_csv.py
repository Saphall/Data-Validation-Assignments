from database_connection import *

def extract_datas_from_csv(tableName, filePath):
    try:
        con = databaseConnect('data_validation')
        cur = con.cursor()

        # empty table before extraction
        cur.execute('TRUNCATE TABLE %s RESTART IDENTITY;' %tableName)
        with open(filePath,'r') as file:
             # skip header row
            next(file)
            cur.copy_from(file,tableName,sep=',')
        con.commit() 
        print(f'[+] Extraction of {tableName} Successful!')

        databaseDisconnect(con,cur)
    except Exception as e:
        print('[-] Exception Occured:',e)



if __name__ == '__main__':
    extract_datas_from_csv('customer','../../data/customer.csv')
    extract_datas_from_csv('product','../../data/product.csv')
    extract_datas_from_csv('sales','../../data/sales.csv')
    extract_datas_from_csv('employee_raw','../../data/employee_raw.csv')
    extract_datas_from_csv('employee','../../data/employee.csv')
    extract_datas_from_csv('timesheet_raw','../../data/timesheet_raw.csv')
    extract_datas_from_csv('timesheet','../../data/timesheet.csv')