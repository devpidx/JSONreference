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

#    all_json_ticket_data = cur.execute('SELECT * FROM ticketData;').fetchall()
    all_json_ticket_data = cur.execute('SELECT supplier, buyer, fieldticketnumber, date, job_location, po_number, line_number, quantity, UOM, lineitem, lineitem_total, amount_total FROM allTicketFields;').fetchall()
    conn.close()
    return jsonify({"ticket data": all_json_ticket_data})

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
    data = cur.execute('INSERT INTO allTicketFields (supplier, buyer, fieldticketnumber, date, job_location, po_number, line_number, quantity, UOM, lineitem, lineitem_total, amount_total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      (content.get('allTicketFields').get('supplier'), content.get('allTicketFields').get('buyer'), content.get('allTicketFields').get('fieldticketnumber'), content.get('allTicketFields').get('date'), content.get('allTicketFields').get('job_location'), content.get('allTicketFields').get('po_number'), content.get('allTicketFields').get('line_number'),
       content.get('allTicketFields').get('quantity'), content.get('allTicketFields').get('UOM'), content.get('allTicketFields').get('lineitem'), content.get('allTicketFields').get('lineitem_total'),
       content.get('allTicketFields').get('amount_total') ) )

# commit and close DB
    conn.commit()
    conn.close()

    with open("./tickets/" + uuid + ".json", "w") as text_file:
        text_file.write(json.dumps(content))

# return unique UUID sent from request
    return jsonify({"uuid":uuid})

# -----A route to allow searching of the product codes database by passing three parameters to the search URL-----
# Sample Call http://api.pidx.org:8080/api/v1/json/recieve_tickets/query?ticketID=221?buyerParty=OFSPortal
@app.route('/api/v1/json/recieve_tickets/query', methods=['GET'])
def api_filter():
    query_parameters = request.args

    supplier = query_parameters.get('supplier')
    buyer = query_parameters.get('buyer')
    fieldticketnumber = query_parameters.get('fieldticketnumber')
    date = query_parameters.get('date')
    job_location = query_parameters.get('job_location')
    po_number = query_parameters.get('po_number')
    line_number = query_parameters.get('line_number')
    quantity = query_parameters.get('quantity')
    UOM = query_parameters.get('UOM')
    lineitem = query_parameters.get('lineitem')
    lineitem_total = query_parameters.get('lineitem_total')
    amount_total = query_parameters.get('amount_total')

    query = "SELECT * FROM allTicketFields WHERE"
    to_filter = []

    if supplier:
        query += ' supplier like ? AND'
        supplier = "%" + supplier + "%"
        to_filter.append(supplier)
    if buyer:
        query += ' buyer like ? AND'
        buyer = "%" + buyer + "%"
        to_filter.append(buyer)
    if fieldticketnumber:
        query += ' fieldticketnumber like ? AND'
        fieldticketnumber = "%" + fieldticketnumber + "%"
        to_filter.append(fieldticketnumber)
    if date:
        query += ' date like ? AND'
        date = "%" + date + "%"
        to_filter.append(date)
    if job_location:
        query += ' job_location like ? AND'
        job_location = "%" + job_location + "%"
        to_filter.append(job_location)
    if po_number:
        query += ' po_number like ? AND'
        po_number = "%" + po_number + "%"
        to_filter.append(po_number)
    if line_number:
        query += ' line_number like ? AND'
        line_number = "%" + line_number + "%"
        to_filter.append(line_number)
    if quantity:
        query += ' quantity like ? AND'
        quantity = "%" + quantity + "%"
        to_filter.append(quantity)
    if UOM:
        query += ' UOM like ? AND'
        UOM = "%" + UOM + "%"
        to_filter.append(UOM)
    if lineitem:
        query += ' lineitem like ? AND'
        lineitem = "%" + lineitem + "%"
        to_filter.append(lineitem)
    if lineitem_total:
        query += ' lineitem_total like ? AND'
        lineitem_total = "%" + lineitem_total + "%"
        to_filter.append(lineitem_total)
    if amount_total:
        query += ' amount_total like ? AND'
        amount_total = "%" + amount_total + "%"
        to_filter.append(amount_total)
    if not (supplier or buyer or fieldticketnumber or date or job_location or po_number or line_number or quantity or UOM or lineitem or lineitem_total or amount_total):
        return page_not_found(404)

    query = query[:-4] + ';'
    print("Here is your query: " + query)
    print("Here is your filter function: " , to_filter)
    conn = sqlite3.connect('TicketTest.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    # query = "SELECT * FROM ticketData WHERE ticketID LIKE ?; "
    # to_filter = ['221']
    # print(query)
    # print(to_filter)
    results = cur.execute(query, to_filter).fetchall()
    # results = cur.execute(query).fetchall()
    
    print(results)

    return jsonify({'result': [dict(row) for row in results]})

# -----------------------------
# Start the server on LOCALHOST port 8080
# -----------------------------
if __name__ == '__main__':
      app.run(host='127.0.0.1', port=8080, debug=True)