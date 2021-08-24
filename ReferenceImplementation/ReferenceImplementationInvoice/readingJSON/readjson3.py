import json

with open ('PIDXSampleInvoice.json','r') as f:
    jsondata = json.loads(f.read())

# define a json extract function that finds all keys within a nested json object
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

# create a sample json string called mylist
# mylist= { }

# Convert string mylist to json string, this just checks the string is in the rght format
mylistjson=json.dumps(jsondata)

# Now convert it to a JSON Object so we can search on keys
mynewjson=json.loads(mylistjson)

# Find every instance of the `text` key in the json object.
textkeys = json_extract(mynewjson, 'pidx:ContactName')

# Print these to the screen
print(textkeys)
