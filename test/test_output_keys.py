import pytest
from output_keys import output_keys
from example_json import example_json


jsons = [i for i in example_json if i]

unwanted = ['row.names','phase','index-entry-number','entry-number','entry-timestamp','key']
wanted = ['register', 'local-authority-eng', 'local-authority-type', 'name', 'official-name', 'start-date', 'end-date']

def test_output_keys():
    """
    Test that DataFrameConverter returns an np.array
    """
    subset_json = output_keys(jsons[0], unwanted)
    print(subset_json)
    subset_json_keys = list(subset_json.keys())

    assert subset_json_keys == wanted
