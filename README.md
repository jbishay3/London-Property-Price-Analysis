# West London house prices: what actually explains the gap between three neighbouring boroughs

An analysis of every residential property sale recorded in Ealing, Hounslow and Richmond upon Thames during 2025, using HM Land Registry Price Paid Data.

dataset available at: https://price-paid-data.publicdata.landregistry.gov.uk/pp-2025.csv

## The question

Richmond is well known to be more expensive than its neighbours. What is less obvious is why. Two explanations are possible and they are very different:

1. **Composition.** Richmond has grander housing, more detached houses and fewer flats, so its average is dragged up by what it contains rather than what things cost.
2. **Price level.** Every kind of property simply costs more there.

I picked these three boroughs because they sit next to each other in west London, share the same transport links and labour market, and yet differ enormously in price. That makes them a reasonable natural comparison.

## The data

HM Land Registry Price Paid Data, yearly file for 2025, released under the Open Government Licence. Roughly a million sales nationally, of which 9,364 fall in the three boroughs.

The file arrives with no column headers, so the sixteen column names are supplied manually in the script.

**One thing worth flagging for anyone reusing this dataset.** I began with the monthly update file and only later noticed that the dates inside it spanned 2022 to 2026. The monthly file contains everything the Land Registry *processed* that month, including corrections to older records, not everything that *sold* that month. Every figure calculated from it was therefore meaningless. The yearly files are cut by date of transfer and are the correct choice. This cost me a couple of hours and is not obvious from the file name.

## Cleaning

**Property type O was excluded.** This code covers everything non residential and it turned out to be doing more work than expected. At the top of the range it captures office and retail blocks along the Golden Mile in Brentford, including one at £30m. At the bottom it captures garages, sheds, parking spaces and, in one case, a strip of subsoil in Teddington sold for £2,000. Excluding it therefore cleans both tails of the distribution in a single defensible step.

Commercial sales are a small share of transactions but a large share of money:

| | Share of sales | Share of money |
|---|---|---|
| Ealing | 4.8% | 14.0% |
| Hounslow | 4.1% | 16.2% |
| Richmond | 4.9% | 4.2% |

Richmond is the exception. Its commercial sales are cheap relative to its residential market, so removing them actually *raised* its mean.

**No minimum price threshold was applied.** After excluding type O, the cheapest sales were inspected directly. There was one at £8,000 and then nothing until £56,063, with no cluster of nominal £1 transfers of the kind that usually appears in this dataset. A price floor would have been arbitrary, so none was used.

After cleaning: 3,607 sales in Ealing, 2,474 in Hounslow and 2,849 in Richmond.

## Findings

### 1. Richmond's premium is price, not property mix

Richmond is more expensive in every single property type.

| Median, 2025 | Hounslow | Ealing | Richmond |
|---|---|---|---|
| Flat | £346,500 | £385,000 | £460,000 |
| Terraced | £525,000 | £605,000 | £890,000 |
| Semi detached | £560,000 | £700,000 | £1,075,000 |
| Detached | £775,000 | £1,300,000 | £1,650,000 |

A terraced house in Richmond has a higher median than a detached house in Hounslow.

To separate the two explanations I standardised each borough onto a common housing mix, using each property type's share across all three boroughs combined, and compared that against each borough's actual mix.

| | Actual mix | Common mix | Composition effect |
|---|---|---|---|
| Hounslow | £462,597 | £459,859 | +£2,738 |
| Ealing | £530,130 | £550,915 | −£20,785 |
| Richmond | £794,472 | £758,895 | +£35,576 |

Of the £264,342 gap between Richmond and Ealing, about £56,361 comes from Richmond having a dearer mix of property types and £207,981 from every type costing more. Composition explains roughly a fifth; price level explains four fifths.

Richmond's composition effect came out higher than I expected before running it, but nowhere near large enough to be the main story.

*A weighted average of medians is not itself a median, so this is an approximation rather than an exact decomposition. The result also depends on which reference mix is chosen.*

### 2. Hounslow's housing mix is distinctive but its effect cancels out

Hounslow has noticeably more semi detached housing than Ealing, 24.1% of sales against 15.6%, and fewer flats. Despite that, its composition effect is close to zero. More semis pushes it up, a cheaper spread elsewhere pulls it back, and the two roughly offset. A borough can have unusual housing stock and still sit on the average once everything is weighed together.

### 3. Hounslow is the cheapest borough and also the most stretched

Measuring how far each mean sits above its median:

| Mean above median | Hounslow | Ealing | Richmond |
|---|---|---|---|
| Flat | 12% | 7% | 13% |
| Terraced | 28% | 20% | 10% |
| Semi detached | 33% | 22% | 18% |
| Detached | 75% | 23% | 27% |

Flats are level across all three boroughs, but Hounslow's spread widens sharply moving up the property ladder, reaching 75% for detached houses against roughly a quarter elsewhere.

This reflects the borough containing two quite different markets. Chiswick sits inside Hounslow alongside Feltham and Hanworth, so its detached stock ranges from ordinary suburban housing to riverside houses selling above £10m.

The practical implication is that "Hounslow is cheaper" is a misleading summary of the borough.

*Hounslow's detached figure rests on 80 sales, so it should be treated as indicative.*

## Limitations

**Shared ownership sales are recorded at the price paid for a share, not the value of the property.** I found this by sorting the cheap end and noticing repeated odd prices in consecutive rows: nine flats at Onyx House on Horn Lane, Ealing, all sold on 27 June 2025 between £56,063 and £79,399, in a postcode where the median sale is £507,000. The file does not record the share percentage, so no correction is possible.

The `ppd_category` field does not reliably identify these. Most were flagged as category B, but at least one comparable record at Verbena House in Southall was flagged A.

Cheap leasehold sales appear in Ealing and Hounslow but not Richmond, and arise from two different causes. Ealing has 29 new build records of the shared ownership kind. Hounslow has 46 established ones, more likely short leases or ex social housing stock.

**Sensitivity test.** Removing all leasehold flats under £150,000 moves the medians by £5,000 in Ealing and £5,000 in Hounslow, around 1%, and leaves Richmond unchanged. The borough ranking does not change. The bias is real and documented but immaterial to the comparison.

Other limitations: the tenure field is known to be unreliable on older records, and leases of seven years or less are never registered. Only one year of data is used, so nothing here says anything about trends.

## What I would do next

Add the 2015 and 2020 yearly files and compare across a decade, noting that prices are not comparable across years without acknowledging general inflation. Split Hounslow by town or postcode district to test the two markets hypothesis directly, rather than inferring it from the mean to median ratio.

## Running it

```
pip install pandas
python property_type_analysis.py
```

Download `pp-2025.csv` from the HM Land Registry price paid data downloads page and place it in the project folder. Note the file is around 100MB and is not included in this repository.

## Attribution

Contains HM Land Registry data © Crown copyright and database right 2025. This data is licensed under the Open Government Licence v3.0.

