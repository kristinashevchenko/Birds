#!/usr/bin/env python
# coding: utf-8

# In[3]:


import psycopg2

def count_birds_color(cursor):
    cursor.execute("INSERT INTO bird_colors_info (color, count) SELECT color, count(name) as count from birds GROUP BY color;")
    
    
def count_birds_stat(cursor):
    cursor.execute("SELECT AVG(body_length) as body_length_mean, AVG(wingspan) as wingspan_length_mean from birds;")
    
    record = cursor.fetchone()
    body_length_mean = record[0]
    wingspan_mean = record[1]
    
    cursor.execute('SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY body_length) FROM birds;')
    record = cursor.fetchone()
    body_length_median = record[0]
    
    cursor.execute('SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY wingspan) FROM birds;')
    record = cursor.fetchone()
    wingspan_median = record[0]
    
    cursor.execute("""SELECT n1.body_length from (select body_length, count(name) as counted from birds group by body_length) n1
    WHERE n1.counted = (select max(n2.counted2) from (SELECT (count(name)) as counted2 FROM birds GROUP BY body_length) n2);""")
    record = cursor.fetchall()
    body_length_mode = []
    for row in record:
        body_length_mode.append(row[0])
        
    cursor.execute("""SELECT n1.wingspan from (select wingspan, count(name) as counted from birds group by wingspan) n1  
    WHERE n1.counted = (select max(n2.counted2) from (SELECT (count(name)) as counted2 FROM birds GROUP BY wingspan) n2);""")
    record = cursor.fetchall()
    wingspan_mode = []
    for row in record:
        wingspan_mode.append(row[0])
    
    cursor.execute("""INSERT INTO birds_stat 
    (body_length_mean,body_length_median,body_length_mode,wingspan_mean,wingspan_median,wingspan_mode) 
    VALUES(%s,%s,%s,%s,%s,%s);""", (body_length_mean,
                                    body_length_median,
                                    body_length_mode,
                                    wingspan_mean,
                                    wingspan_median,
                                    wingspan_mode))

 
def mainFunc():
    connection = None
    try:
        connection = psycopg2.connect(user = "ornithologist",
                                      password = "ornithologist",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "birds_db")

        cursor = connection.cursor()

        # clear databases
        cursor.execute("DELETE from bird_colors_info;")
        cursor.execute("DELETE from birds_stat;")

        # 1 задание
        count_birds_color(cursor)
        connection.commit()
        print('Successfully inserted in birds_info')

        # 2 задание
        count_birds_stat(cursor)
        connection.commit()
        print('Successfully inserted in birds_stat')

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
                
mainFunc()


# In[ ]:




