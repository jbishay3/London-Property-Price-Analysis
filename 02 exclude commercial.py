"""
Step 2: remove commercial and other non residential sales.

The Price Paid file records a property type for every sale. Four of the codes
are residential (D detached, S semi detached, T terraced, F flat) and the fifth,
O for other, covers everything else, including commercial units, land and
properties that could not be classified.

Those O records distort a residential comparison in both directions: some are
large commercial transactions worth many millions, others are nominal transfers
of land. Excluding them is the first cleaning step.

Input:  pp-2025.csv (Price Paid Data, supplied without a header row)
Output: printed table of median, mean and count by district, residential only
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

# Keep only the four residential property types by dropping code O.
non_commercial_properties=comparison[(comparison["property_type"] != "O")]

# Recalculate the same three statistics so the effect of the exclusion can be
# read directly against the baseline figures from step 1.
stats = non_commercial_properties.groupby("district")["price"].agg(["median", "mean", "count"])
print(stats)
