import json

# print(jsondata)

with open ('PIDXSampleInvoice.json','r') as f:
    jsondata = json.loads(f.read())


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
            return arr

    values = extract(obj, arr, key)
    return values

print(jsondata['Invoice'])

print(json_extract(jsondata, 'pidx:InvoiceSummary'))