import requests
import datetime

ts = datetime.datetime.now().timestamp()

res = requests.post(f"http://127.0.0.1:8080/api/v1/json/submit_ticket/{ts}", json={   
   "ticketData": {
      "ticketID": ts,
      "buyerParty": "Cereal Eater",
      "supplierParty": "Kellogs",
      "ticketCost": "140" }
})
if res.ok:
    print(res.json())
