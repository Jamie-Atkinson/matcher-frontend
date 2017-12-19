# matcher-frontend

Visiting the root (`/`) of this app will make a POST request to registermatcher, and display the results.

Next steps:

* Parse a csv file loaded from the `/upload/` page, and extract a column of interest (probably using pandas, e.g. `import pandas as pd; data = pd.read_csv('file')`)
* Make multiple POST requests using the data uploaded from the upload page - you might start by running a for loop on the column of interest, e.g. `column = data['column']; for row in column: make_post_request(row)`.
* Handle all the responses in a sensible way. You will have multiple response jsons, one each for every row in column. Could be combined together into a dataframe in pandas.
