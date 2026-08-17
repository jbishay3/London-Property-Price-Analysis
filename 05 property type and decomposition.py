"""
Step 5: housing mix analysis and decomposition of the price gap.

The earlier steps show that Richmond upon Thames is more expensive than Ealing
and Hounslow, but not why. Two explanations are possible and they are very
different: either Richmond has more of the expensive property types, or the same
type of property simply costs more there.

This script separates the two. It builds counts, medians and means for every
combination of property type and borough, then each borough's housing mix as
percentage shares, and a mean to median ratio as a skew check by segment.

The decomposition that produces the headline split, roughly 20 per cent from
differences in housing mix and 80 per cent from underlying price levels, is held
at the bottom of the file. It reweights every borough onto a common housing mix
and compares that with its actual mix.

Input:  pp-2025.csv (Price Paid Data, supplied without a header row)
Output: mean_median_ratios.csv, plus the tables built in memory above it
"""

import pandas as pd
import numpy as np

# Wider output and thousands separators with no decimal places, so that price
# tables are readable in the terminal.
pd.set_option("display.width", 200)
pd.set_option("display.float_format", "{:,.0f}".format)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Read the headerless file positionally, then apply the documented column names.
df = pd.read_csv("pp-2025.csv", header=None)
df.columns = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
"old_new", "duration", "paon", "saon", "street", "locality", "town_city", "district", "county",
"ppd_category", "record_status"]

# Narrow the national file down to the three boroughs, then keep residential
# property types only, as established in step 2. A copy is taken because the
# labels below are rewritten in place.
wanted = ["HOUNSLOW", "EALING", "RICHMOND UPON THAMES"]
comparison=df[(df["district"].isin(wanted))]
clean=comparison[(comparison["property_type"] != "O")].copy()

# Replace the single letter codes and the capitalised district names with
# readable labels, so the output tables can be read without a key.
labels1 = {"D": "Detached", "S": "Semi detached", "T": "Terraced", "F": "Flat"}
labels2={"HOUNSLOW": "Hounslow", "RICHMOND UPON THAMES": "Richmond", "EALING": "Ealing"}
clean["property_type"] = clean["property_type"].replace(labels1)
clean["district"] = clean["district"].replace(labels2)

# Fix the row order from cheapest type to most expensive so every table reads
# the same way, rather than falling back to alphabetical order.
order = ["Flat", "Terraced", "Semi detached", "Detached"]

# Three views of the same grid, property type down the side and borough across
# the top: how many sales, the typical price, and the average price.
counts = clean.groupby(["property_type", "district"])["price"].count().unstack().reindex(order)
medians = clean.groupby(["property_type", "district"])["price"].median().unstack().reindex(order)
means = clean.groupby(["property_type", "district"])["price"].mean().unstack().reindex(order)

# Each borough's housing mix as percentages of its own sales. This is the
# composition side of the question.
shares=(counts / counts.sum())*100

# Mean divided by median for each segment. A ratio well above 1 shows that a few
# very large sales are pulling the average up, which is why medians are used
# throughout the comparison.
ratios=(means/medians).round(2)
ratios.to_csv("mean_median_ratios.csv")


medians.to_csv("medians.csv")
#Each borough's own housing mix, as proportions
own_weights = counts / counts.sum()

# A common mix: each type's share across all three boroughs combined
type_totals = counts.sum(axis=1)
common_weights = type_totals / type_totals.sum()

# Weighted average price using each borough's actual mix
actual = (medians * own_weights).sum()

# The same, but forcing every borough onto the common mix
standardised = medians.mul(common_weights, axis=0).sum()

decomposition = pd.DataFrame({
    "Actual mix": actual,
    "Common mix": standardised,
    "Composition effect": actual - standardised,
}).round(0)

print(decomposition)
decomposition.to_csv("composition_decomposition.csv")
