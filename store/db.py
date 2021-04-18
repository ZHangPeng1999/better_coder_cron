import pymysql


def InsertBoard(myType, city_uri, salary_uri, education_uri, company_uri, technology_uri):
    # 打开数据库连接
    db  = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='design',
        charset='utf8'
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = """INSERT INTO Board(type,
             city_uri, salary_uri, education_uri, company_uri, technology_uri)
             VALUES (""" + myType + ",'" + city_uri + "','" + salary_uri + "','" + education_uri + "','" + \
          company_uri + "','" + technology_uri + "'" + """)"""
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    InsertBoard("1", "2", "3", "4", "5", "6")
