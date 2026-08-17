"""
Step 3: remove nominal and placeholder transactions.

Alongside genuine sales, the Price Paid file contains records with prices far
below anything a property in west London could sell for. These are typically
transfers between related parties, corrections and other non market entries.
They pull the median down without saying anything about market prices.

A floor of 5,000 pounds is used. It is high enough to remove the clearly
nominal records and low enough that no plausible open market sale is caught by
it, which is checked in step 4 by testing a much stricter alternative.

This script applies both cleaning rules together and produces the figures the
main comparison is based on.

Input:  pp-2025.csv (Price Paid Data, supplied without a header row)
Output: printed table of median, mean and count by district, cleaned
"""

import pandas as pd
import numpy as np

# Print the full table rather than a truncated view.
pd.set_option("display.max_rows", None)

# Read the headerless file positionally, then apply the documented column names.
df = pd.read_csv("pp-2025.csv", header=None)
df.columns = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
"old_new", "duration", "paon", "saon", "street", "locality", "town_city", "district", "county",
"ppd_category", "record_status"]

# Narrow the national file down to the three boroughs being compared.
wanted = ["EALING", "HOUNSLOW", "RICHMOND UPON THAMES"]
comparison=df[(df["district"].isin(wanted))]

# Apply both cleaning rules at once: residential property types only, and a
# price floor to drop nominal transfers.
non_commercial_and_non_dummy_transactions=comparison[(comparison["property_type"] != "O") & (comparison["price"]>5000)]

# The resulting medians are the ones quoted in the writeup.
stats =non_commercial_and_non_dummy_transactions.groupby("district")["price"].agg(["median", "mean", "count"])
print(stats)
