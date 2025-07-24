import pandas
import matplotlib.pyplot as plt
#LOADING THE DATA 
df=pandas.read_csv(r"https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv")
print(df)

#FIRST FIVE ROWS
print("\nFIRST FIVE ROWS")
print(df.head())

#CHECK FOR MISSING VALUES IN EACH COLUMN 
print("\nMISSINGVALUES IN EACH COLUMN")
print(df.isnull().sum())

#UNIQUE COUNTRIES 
print("\nUNIQUE COUNTRIES IN DATASET")
print(df["country"].unique())

#DATE RANGE
print("\nDATE RANGE ")
#df=['date']=pandas.to_datetime(df["date"])
print("EARLIEST DATE:",df["date"].min())
print("LATEST DATE:",df["date"].max())

#DESCRIPTIVE STATISTICS
#TOTAL CASES
print("\nTOTAL CONFIRMED CASES WORLDWIDE :")
print(df["total_cases"].sum())

#AVERAGE NUMBER OF DEATHS PER DAY IN INDIA 
print("\nAVERAGE NUMBER OF DEATHS PER DAY IN INDIA :")
data=df[df["country"]=="India"]
average_deaths=print(data["new_deaths"].mean())

#DATA AGGREGATION AND GROUPING
grp_by_country=df.groupby("country")[["total_cases","total_deaths"]].max()
print(grp_by_country.head(10))

#GROUP BY DATE AND PLOT GLOBAL DAILY CONFIRMED CASES
print("\nLINE CHART OF GLOBAL DAILY CONFIRMED CASES:")
daily_global = df.groupby("date")["new_cases"].sum()

plt.figure(figsize=(12, 6))
plt.plot(daily_global.index, daily_global.values, color='blue')
plt.title("Global Daily Confirmed COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.grid(True)
plt.tight_layout()
plt.show()

#BAR CHART OF TOP 10 COUNTRIES BY TOTAL CONFIRMED CASES
"""top10=grp_by_country.sort_values("total_cases",ascending=False).head(10)
plt.bar(top10["country"],top10["total_cases"])
plt.show() """

#DATE HAS HIGHEST NUMBER OF CONFIRMED CASES GLOBALLY
print("\nDATE WITH HIGHEST NEW CONFIRMED CASES GLOBALLY:")
max_date = daily_global.idxmax()
max_cases = daily_global.max()
print(f"{max_date}: {max_cases} cases")

# Create Death_Rate column and find country with highest value
latest = df.sort_values("date").groupby("country").tail(1).copy()
latest = latest[latest["total_cases"] > 0]
latest["Death_Rate"] = latest["total_deaths"] / latest["total_cases"]
worst = latest.loc[latest["Death_Rate"].idxmax()]
print(f"\nCountry with highest DEATH RATE: {worst['country']} ({worst['Death_Rate']:.2%})")

# 1️4  Compare confirmed-case trends for India, USA, Brazil
countries = ["India", "United States", "Brazil"]      # names exactly as in the dataset
mask      = df["country"].isin(countries)
trend_df  = df[mask][["date", "country", "total_cases"]]

plt.figure(figsize=(12,6))
for c in countries:
    subset = trend_df[trend_df["country"] == c]
    plt.plot(subset["date"], subset["total_cases"], label=c)

plt.title("Total Confirmed Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.tight_layout()
plt.show()

# 1️5  Pie chart of ACTIVE vs RECOVERED vs DEATHS (latest global snapshot)
global_latest = df[df["date"] == df["date"].max()].groupby("date").agg(
    total_cases   = ("total_cases",   "sum"),
    total_deaths  = ("total_deaths",  "sum"),
    total_recov   = ("total_recoveries", "sum") if "total_recoveries" in df.columns else ("total_cases", "sum")  # fallback
).iloc[0]



# 1️6  7-day rolling average of NEW cases for a chosen country (India)
country = "India"
one_cty = df[df["country"] == country].set_index("date").sort_index()
one_cty["7d_avg"] = one_cty["new_cases"].rolling(window=7).mean()

plt.figure(figsize=(12,6))
plt.plot(one_cty.index, one_cty["7d_avg"])
plt.title(f"7-Day Rolling Avg of New COVID-19 Cases – {country}")
plt.xlabel("Date")
plt.ylabel("New Cases (7-day avg)")
plt.tight_layout()
plt.show()

#print("\nTOP 5 DAYS WITH HIGHEST NEW CASES GLOBALLY:")
print("\nTOP 5 DAYS WITH HIGHEST NEW CASES GLOBALLY:")
print(daily_global.sort_values(ascending=False).head())

#Export cleaned/aggregated data to .csv
# Cleaned dataset (latest per country, with death rate)
latest.to_csv("latest_covid_summary.csv", index=False)
# Global daily totals
daily_global.to_csv("daily_global_cases.csv")

### Summary Report

"""- **Global confirmed cases:** [X] (from Q5)
- **India average daily deaths:** [Y] (from Q6)
- **Country with most cases:** [Z]
- **Highest death rate:** [W] – [W%] """

#### Top Insights:
"""- The **USA, India, and Brazil** are the most affected in terms of confirmed cases.
- [W] has the highest death-to-confirmed ratio, possibly due to [reason: e.g., healthcare limitations, underreporting].
- There is a significant **spike** on [date] with [cases] new cases globally (Q12).
- The 7-day average in India shows [rising/falling/plateauing] trend in recent weeks."""
