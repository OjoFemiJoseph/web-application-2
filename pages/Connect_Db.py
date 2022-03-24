import pymysql
    
def connectdb():
    
    conn =pymysql.connect(
        user = 'root',
        password = '',
        db = 'upwork',
        host = 'localhost',


    )

   
   
    print("success in connecting", conn)
    return conn