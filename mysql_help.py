import pymysql
from DBUtils.PooledDB import PooledDB


class MySqlHelper(object):
    def __init__(self, mincached, **dbparms):
        dbparms['cursorclass'] = pymysql.cursors.DictCursor
        try:
            self.pool = PooledDB(pymysql, mincached, **dbparms)
        except Exception as ex:
            self.pool = None
            print(ex)

    def Insert(self, sql, param=()):
        id = 0
        conne = self.pool.connection()
        try:
            
            cursor = conne.cursor()
            cursor.execute(sql, param)
            id = cursor.lastrowid
            conne.commit()
            cursor.close()
            conne.close()
        except Exception as ex:
            conne.close()
            print(sql, "\n", ex)
        return id

    def Update(self,sql, param=()):
        conne = self.pool.connection()
        try:
            cursor = conne.cursor()
            cursor.execute(sql, param)
            conne.commit()
            cursor.close()
            conne.close()
        except Exception as ex:
            conne.close()
            print(sql, "\n", ex)
            return
    def Select(self, sql, param=()):
        result = None
        conne = self.pool.connection()
        try:
            
            cursor = conne.cursor()
            cursor.execute("set sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'")
            cursor.execute(sql, param)
            result = cursor.fetchone()
            cursor.close()
            conne.close()
        except Exception as ex:
            conne.close()
            print(sql, "\n", ex)
        return result

    def SelectList(self, sql, param=()):
        result = None
        conne = self.pool.connection()
        try:
            
            cursor = conne.cursor()
            cursor.execute(sql, param)
            result = cursor.fetchall()
            cursor.close()
            conne.close()
        except Exception as ex:
            conne.close()
            print(sql, "\n", ex)
        return result

    def Close(self):
        try:
            self.pool.close()
        except Exception as ex:
            print(ex)
