#!/usr/bin/env python
# coding: utf-8

# In[3]:


import flask
from flask import request, jsonify
import psycopg2
import json

app = flask.Flask(__name__)


def request_database(query):
    connection = None
    try:
        connection = psycopg2.connect(user = 'ornithologist',
                                      password = 'ornithologist',
                                      host = '127.0.0.1',
                                      port = '5432',
                                      database = 'birds_db')

        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()

        return (True, record)

    except (Exception, psycopg2.Error) as error :
        print ('Error while connecting to PostgreSQL', error)
        return (False, error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                
def insert_into_database(query, insert_object):
    connection = None
    try:
        connection = psycopg2.connect(user = 'ornithologist',
                                      password = 'ornithologist',
                                      host = '127.0.0.1',
                                      port = '5432',
                                      database = 'birds_db')

        cursor = connection.cursor()
        cursor.execute(query, insert_object)
        connection.commit()

        return (True, )

    except (Exception, psycopg2.Error) as error :
        print ('Error while connecting to PostgreSQL', error)
        return (False, error)
    finally:
            if(connection):
                cursor.close()
                connection.close()


@app.route('/', methods=['GET'])
def home():
    return 'Home Route'

@app.route('/version', methods=['GET'])
def version():
    return 'Birds Service. Version 0.1'


@app.errorhandler(404)
def page_not_found(error_desc = 'Invalid value', error_code = 404):
    error_string = str(error_desc)
    return error_string, error_code


@app.route('/birds', methods=['GET'])
def api_filter():
    query_parameters = request.args

    attribute = query_parameters.get('attribute')
    limit = query_parameters.get('limit')
    order = query_parameters.get('order')
    offset = query_parameters.get('offset')

    query = 'SELECT * FROM birds'
    
    if attribute:
        if check_attribute(attribute):
            query += (' ORDER BY ' + attribute)
        else:
            return page_not_found('Invalid value for attribute param')
        
        if order:
            if order.lower() == 'desc' or order.lower() == 'asc':
                query += (' ' + order)
            else:
                return page_not_found('Invalid value for order param')
    
    if limit:
        query += (' LIMIT ' + limit)
    if offset:
        query += (' OFFSET ' + offset)

    query = query + ';'
    birds = request_database(query)

    if birds[0]:
        return jsonify(birds[1])
    else:
        return page_not_found(birds[1])
    
    
@app.route('/birds', methods=['POST'])
def insert_bird():
    request_object = next(iter(request.form))
    request_object = json.loads(request_object)

    name = request_object.get('name')
    color = request_object.get('color')
    species = request_object.get('species')
    body_length = request_object.get('body_length')
    wingspan = request_object.get('wingspan')
    
    if name and color and species and wingspan and body_length:
        query = """INSERT INTO birds (name,color,species,body_length,wingspan) VALUES(%s,%s,%s,%s,%s);"""
        is_success = insert_into_database(query, (name, color, species, body_length, wingspan))

        if not is_success[0]:
            return page_not_found(is_success[1])
        return 'Inserted successfully'
    else:
        return page_not_found(is_success[1])
    
def check_attribute(attribute):
    return True if attribute.lower() in ['name', 'body_length', 'color', 'wingspan', 'species'] else False


app.run(host='localhost', port=8080)
