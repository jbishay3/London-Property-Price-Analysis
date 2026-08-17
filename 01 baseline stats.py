"""
Step 1: baseline price statistics, before any cleaning.

Loads the HM Land Registry Price Paid file for 2025 and produces the median,
mean and transaction count for each of the three boroughs being compared.

These figures are deliberately unfiltered. They are the starting point that the
later scripts clean up, and the gap between the median and the mean here is the
first sign that the raw data contains records that do not belong in a
residential price comparison.

Input:  pp-2025.csv (Price Paid Data, supplied without a header row)
Output: printed table of median, mean and count by district
"""

import pandas as pd
import numpy as np

# Print every row rather than letting pandas truncate the middle of the output.
pd.set_option("display.max_rows", None)

# The Price Paid file ships with no header row, so the columns are read
# positionally and named afterwards, following the field order published in the
# Land Registry documentation.
df = pd.read_csv("pp-2025.csv", header=None)
df.columns = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
"old_new", "duration", "paon", "saon", "street", "locality", "town_city", "district", "county",
"ppd_category", "record_status"]

# The three west London boroughs under comparison. District names are stored in
# capitals in the source file, so they are matched in capitals here.
wanted = ["EALING", "HOUNSLOW", "RICHMOND UPON THAMES"]
comparison=df[(df["district"].isin(wanted))]

# Median is the headline figure because sale prices are heavily skewed by a
# small number of very large transactions. The mean is kept alongside it as a
# skew indicator, and the count shows how much data sits behind each borough.
stats = comparison.groupby("district")["price"].agg(["median", "mean", "count"])
print(stats)
