import flask
from flask import request, jsonify
from flask_cors import CORS
from flask import render_template
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# -----If no URL route is found, return 404 not found error-----
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>PIDX API Server - 404</h1><p> </p><p>The resource could not be found.</p>", 404

# -----A Route to return all of the Ticket Handling data-----
# Sample Call http://api.pidx.org:8080/api/v1/json/receive_tickets
@app.route('/api/v1/json/recieve_tickets', methods=['GET'])
def api_json_ticket_data():

    conn = sqlite3.connect('TicketTest.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    all_json_ticket_data = cur.execute('SELECT supplier, buyer, fieldticketnumber, date, job_location, po_number, line_number, quantity, UOM, lineitem, lineitem_total, amount_total FROM allTicketFields;').fetchall()
    conn.close()
    return jsonify({'result': [dict(row) for row in all_json_ticket_data]})

# -----A route to store ticket records in the ticketData table-----
# Sample Call http://api.pidx.org:8080/api/v1/json/submit_ticket/myuniquemessageID
@app.route('/api/v1/json/submit_ticket/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    print('----PIDX Received POST Request---------------')

    content = request.json

    print('----Received POST Request---------------')
    print(content['allTicketFields'])
    print('-------------------')

# open SQLite3 database
    conn = sqlite3.connect('TicketTest.db')
    cur = conn.cursor()
# write new ticket record to the DB
    cur.execute('INSERT INTO allTicketFields (supplier, buyer, fieldticketnumber, date, job_location, po_number, line_number, quantity, UOM, lineitem, lineitem_total, amount_total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      (content.get('allTicketFields').get('supplier'), content.get('allTicketFields').get('buyer'), content.get('allTicketFields').get('fieldticketnumber'), content.get('allTicketFields').get('date'), content.get('allTicketFields').get('job_location'), content.get('allTicketFields').get('po_number'), content.get('allTicketFields').get('line_number'),
       content.get('allTicketFields').get('quantity'), content.get('allTicketFields').get('UOM'), content.get('allTicketFields').get('lineitem'), content.get('allTicketFields').get('lineitem_total'),
       content.get('allTicketFields').get('amount_total') ) )

# # -----A Route to return all of the Ticket Handling data-----
# # Sample Call http://api.pidx.org:8080/api/v1/json/receive_tickets
# @app.route('/api/v1/json/recieve_tickets', methods=['GET'])
# def api_json_ticket_data():

#     conn = sqlite3.connect('TicketTest.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()

# #   all_json_ticket_data = cur.execute('SELECT * FROM ticketData;').fetchall()
#     all_json_ticket_data = cur.execute('ticketID, buyerParty, supplierParty, ticketCost FROM ticketData;').fetchall()
#     conn.close()
#     return jsonify({'result': [dict(row) for row in all_json_ticket_data]})

# # -----A route to store ticket records in the ticketData table-----
# # Sample Call http://api.pidx.org:8080/api/v1/json/submit_ticket/myuniquemessageID
# @app.route('/api/v1/json/submit_ticket/<uuid>', methods=['GET', 'POST'])
# def add_message(uuid):
#     print('----PIDX Received POST Request---------------')

#     content = request.json

#     print('----Received POST Request---------------')
#     print(content['ticketData'])
#     print('-------------------')

# # open SQLite3 database
#     conn = sqlite3.connect('TicketTest.db')
#     cur = conn.cursor()
# # write new ticket record to the DB
#     cur.execute('INSERT INTO ticketData (ticketID, buyerParty, supplierParty, ticketCost) VALUES (?, ?, ?, ?)',
#       (content.get('ticketData').get('ticketID'), content.get('ticketData').get('buyerParty'), content.get('ticketData').get('supplierParty'),
#        content.get('ticketData').get('ticketCost') ) )

# commit and close DB
    conn.commit()
    conn.close()

# return unique UUID sent from request
    return jsonify({"uuid":uuid})

# -----------------------------
# Start the server on LOCALHOST port 8080
# -----------------------------
if __name__ == '__main__':
      app.run(host='127.0.0.1', port=8080, debug=True)