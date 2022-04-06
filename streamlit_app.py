import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

# Move this code into `load_data` function {{
cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)

pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)

df = pd.merge(left=cancer_df, right=pop_df, how="left")
df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
df.dropna(inplace=True)

df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

# }}

@st.cache
def load_data():
    ## {{ CODE HERE }} ##
    df = ... # remove this line
    return df

# Uncomment the next line when finished
# df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates")


### P2.1 ###
year = 2018 # replace with st.slider
subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
sex = "M" # replace with st.radio
subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
# filter for only the countries which contain data for the selected year
countries = ["Sweden", "Thailand"] # replace with st.multiselect
subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
cancer = "Leukaemia"
subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Rate", title="Mortality rate per 100,000"),
    color="Country",
    tooltip=["Rate"],
).properties(
    title=f"{cancer} mortality rates for {'males' if sex is 'M' else 'females'} in {year}",
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)
