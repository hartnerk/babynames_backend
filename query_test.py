import sqlite3

# Change filepath to db.sqlite3 in line 7 to your current directory. 


def user_preference_query(gender=None, usage=None):

    if usage is not None:
        usage = usage.capitalize()
        
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    sql = "select * from users_babynames"

    if gender is not None and usage is not None:
        sql += ' where gender = ? and usage = ?'
        curs.execute(sql,[gender, usage])

    elif gender is not None and usage is None:
        sql += " where gender = ?"
        curs.execute(sql,[gender])

    elif usage is not None and gender is None:
        sql += " where usage = ?"
        curs.execute(sql,[usage])

    
    r = curs.fetchall()
    conn.commit()
    curs.close()

    return list(r)

q1 = user_preference_query('m',None)
print(q1)