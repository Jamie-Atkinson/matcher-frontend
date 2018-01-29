from output_keys import output_keys
from example_json import example_json

unwanted = ['row.names','phase','index-entry-number','entry-number','entry-timestamp','key']

jsons = [i for i in example_json if i]
foo = output_keys(jsons[0], unwanted)
print(foo)
