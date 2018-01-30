import pytest
from output_keys import output_keys
from example_json import example_json

# Find the not None entries
jsons = [i for i in example_json if i]

unwanted = ['row.names','phase','index-entry-number','entry-number','entry-timestamp','key']
wanted = ['register', 'local-authority-eng', 'local-authority-type', 'name', 'official-name', 'start-date', 'end-date']

def test_output_keys():
    """
    Test that DataFrameConverter returns an np.array
    """
    # Try on the first not None entry
    subset_json = output_keys(jsons[0], unwanted)

    # Extract the keys from the subset
    subset_json_keys = list(subset_json.keys())

    assert subset_json_keys == wanted

