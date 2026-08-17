"""
Step 4: sensitivity test on the cleaning rules.

Step 3 used a 5,000 pound floor to remove nominal transfers. A fair question is
whether the borough ranking depends on where that line is drawn.

This script applies a far more aggressive rule instead. It removes every
leasehold flat sold for under 150,000 pounds, which is a much larger cut and
takes out a whole band of genuine low value sales as well as the nominal ones.
Leasehold flats are targeted because that is where shared ownership shares,
lease extensions and part transfers cluster.

If the ranking of the three boroughs survives a rule this severe, it is not an
artefact of the cleaning choices.

Input:  pp-2025.csv (Price Paid Data, supplied without a header row)
Output: printed table of median, mean and count by district under the stricter rule
"""

import pandas as pd
import numpy as np

# Print the full table rather than a truncated view.
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Read the headerless file positionally, then apply the documented column names.
df = pd.read_csv("pp-2025.csv", header=None)
df.columns = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
"old_new", "duration", "paon", "saon", "street", "locality", "town_city", "district", "county",
"ppd_category", "record_status"]

# Narrow the national file down to the three boroughs being compared.
wanted = ["EALING", "HOUNSLOW", "RICHMOND UPON THAMES"]
comparison=df[(df["district"].isin(wanted))]

# Start from the residential only set, as in step 2.
clean=comparison[(comparison["property_type"] != "O")]

# Flag the records to be tested against: flats (F) held on a lease (L) that sold
# for under 150,000 pounds.
misc=(clean["property_type"] == "F") & (clean["price"]<150000) & (clean["duration"] == "L")

# The tilde inverts the flag, so the statistics are calculated on everything
# except those records. Compare the ordering against step 3 rather than the
# absolute values, which will naturally be higher here.
stats = clean[~misc].groupby("district")["price"].agg(["median", "mean", "count"])
print(stats)
