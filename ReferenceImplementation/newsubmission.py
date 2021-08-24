import requests
import datetime

ts = datetime.datetime.now().timestamp()

res = requests.post(f"http://127.0.0.1:8080/api/v1/json/submit_ticket/{ts}", json={   
   "allTicketFields": {
      "supplier": "OFS",
      "buyer": "Chris",
      "fieldticketnumber": ts,
      "date": "210803",
      "job_location": "UK",
      "po_number": "123457",
      "line_number": "6",
      "quantity": "2",
      "UOM": "each",
      "lineitem": "man hours",
      "lineitem_total": "400",
      "amount_total": "11000" }
})
if res.ok:
    print(res.json())