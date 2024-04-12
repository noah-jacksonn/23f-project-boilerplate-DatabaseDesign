from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select id, company, last_name,\
        first_name, job_title, business_phone from customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a PUT /customers route that will update the customers information given their ID
# number.  You can base this off the examples in the Products Blueprint.
# You only need to include attributes that are returned from the GET /customers route.  
@customers.route('/customers/<int:id>', methods=['PUT'])
def put_customers(id):
    cursor = db.get_db().cursor()
    data = request.get_json()
    query = '''
        UPDATE customers 
        SET company = %s, 
            last_name = %s, 
            first_name = %s, 
            job_title = %s,
            business_phone = %s 
        WHERE id = %s
    '''
    cursor.execute(query, (data['company'], data['last_name'], data['first_name'], data['job_title'], data['business_phone'], id))
    db.get_db().commit()
    return jsonify({"message": "Customer updated successfully"}), 200
                   
# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response