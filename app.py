import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

###########################
#     HELPER FUNCTIONS    #
###########################

def add_footer():
    """
    Displays a common footer across all tabs.
    """
    st.markdown("---")
    st.write(" **ICL Management Tool | Powered by Oporot Carbon | Desgiend and Develped by Dr. Luvchik Avi**")
    st.caption("© 2025 All Rights Reserved.")

def load_data():
    """
    Loads or simulates ESG-related data for GHG, water, energy, waste, and biodiversity.
    Replace or expand these sample data frames with real data as needed.
    """

    # 1) GHG EMISSIONS DATA (2018–2023)
    df_ghg = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022, 2023],
        # In million tonnes (just sample numbers)
        'Scope 1+2 GHG': [2.94, 2.65, 2.51, 2.54, 2.41, 2.29],
        # Could also store separate Scope 1 vs. Scope 2 columns if desired
    })

    # 2) WATER USAGE DATA
    df_water = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022, 2023],
        'Freshwater_m3': [20.2, 19.8, 19.1, 20.2, 19.6, 17.4],    # millions of m³
        'NonFreshwater_m3': [48.8, 49.0, 48.2, 48.8, 49.4, 47.3], # millions of m³
    })

    # 3) ENERGY DATA
    df_energy = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022, 2023],
        'Total_Energy_GJ': [35.3, 36.5, 33.8, 34.0, 35.1, 36.4],
        # Some example breakdown:
        'Renewables_%': [3, 4, 5, 6, 8, 9],  # approximate share of total energy from renewables
    })

    # 4) WASTE DATA
    df_waste = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022, 2023],
        'Hazardous_t': [29.5, 28.2, 27.9, 34.9, 28.0, 23.9],   # thousand tonnes
        'NonHazardous_t': [5.5, 22.3, 38.5, 32.0, 10.5, 21.5],# thousand tonnes
    })

    # 5) BIODIVERSITY / RESTORATION SAMPLE
    df_biod = pd.DataFrame({
        'Year': [2019, 2020, 2021, 2022, 2023],
        'Habitat_Restored_km2': [0.5, 0.8, 1.2, 1.6, 2.0],
        'Sites_with_Projects': [3, 4, 5, 6, 7],
    })

    return df_ghg, df_water, df_energy, df_waste, df_biod

def apply_ghg_scenario(df, additional_reduction_pct):
    """
    Applies an additional percentage reduction to the GHG DataFrame to simulate
    improved performance from new policies or investments.
    """
    df_scenario = df.copy()
    df_scenario["Scope 1+2 GHG"] = df_scenario["Scope 1+2 GHG"] * (1 - additional_reduction_pct / 100.0)
    return df_scenario

def apply_water_scenario(df, investment_m):
    """
    Example: For every 10M invested, reduce Freshwater usage by 1% in this simplistic scenario.
    """
    df_scenario = df.copy()
    reduction_pct = (investment_m // 10) * 1  # integer math for simplicity
    df_scenario["Freshwater_m3"] = df_scenario["Freshwater_m3"] * (1 - reduction_pct / 100.0)
    return df_scenario, reduction_pct

def apply_energy_scenario(df, solar_mw_add):
    """
    Example: For every +10 MW of solar, the renewables_% might increase by 1 percentage point (illustrative).
    """
    df_scenario = df.copy()
    step = solar_mw_add // 10
    df_scenario["Renewables_%"] = df_scenario["Renewables_%"] + step
    # Keep it capped at 100 (just in case)
    df_scenario["Renewables_%"] = df_scenario["Renewables_%"].clip(upper=100)
    return df_scenario

def apply_waste_scenario(df, new_reuse_k):
    """
    For each thousand tonnes (k) of potential re-use, reduce the hazardous & non-hazardous disposal by some fraction.
    This is a simplified example.
    """
    df_scenario = df.copy()
    # Let's say each 1k re-use can reduce total hazardous waste by 0.5% and non-hazardous by 0.3%
    haz_reduction = df_scenario["Hazardous_t"] * 0.005 * new_reuse_k
    nonhaz_reduction = df_scenario["NonHazardous_t"] * 0.003 * new_reuse_k
    df_scenario["Hazardous_t"] = (df_scenario["Hazardous_t"] - haz_reduction).clip(lower=0)
    df_scenario["NonHazardous_t"] = (df_scenario["NonHazardous_t"] - nonhaz_reduction).clip(lower=0)
    return df_scenario

def combined_esg_scenario(ghg_red, water_inv, solar_mw, waste_reuse):
    """
    A placeholder function that integrates multiple scenario inputs in a
    simplistic way to show a final "score" or "index."
    Could combine weighted metrics of GHG, water usage, waste, etc.
    """
    # Basic scoring approach: (the bigger the better for scenario)
    # We'll just sum or average these inputs in a toy formula for demonstration:
    # Score range: 0-100
    # Example: each dimension contributes up to 25 points if you max it out
    # e.g. GHG: 30% => full 25 points
    # water: 50M => full 25
    # solar: 50 MW => full 25
    # waste reuse: 10k => full 25
    # This is purely illustrative:
    ghg_score = min(ghg_red / 30, 1) * 25
    water_score = min(water_inv / 50, 1) * 25
    solar_score = min(solar_mw / 50, 1) * 25
    waste_score = min(waste_reuse / 10, 1) * 25
    total_score = ghg_score + water_score + solar_score + waste_score
    return round(total_score, 2)

###########################
#       MAIN APP          #
###########################

def main():
    # Streamlit Layout & Title
    st.set_page_config(layout="wide", page_title="ICL ESG Decision Tool")
    
    col1, col2 = st.columns([0.7, 0.3])  # adjust column widths
    with col1:
        st.title("ICL ESG Decision-Making Tool")
    with col2:
        st.image("/Users/aviluvchik/app/ICL/icl_logo.jpeg", width=120)
    #st.markdown(
    #    "Welcome to the ICL ESG Decision-Making Tool! Use this app to explore and analyze key ESG metrics, "
    #    "run reduction scenarios, and evaluate the impact of various sustainability initiatives."
    #)

    # Load Data
    df_ghg, df_water, df_energy, df_waste, df_biod = load_data()

    # TABS
    tabs = st.tabs([
        "Home / Executive Summary",
        "Climate & GHG",
        "Water & Wastewater",
        "Energy & Efficiency",
        "Circular & Waste",
        "Biodiversity & Overall"
    ])

    ###############################################################################
    # TAB 0: HOME / EXECUTIVE SUMMARY
    ###############################################################################
    with tabs[0]:
        st.subheader("Executive Summary")
        st.write("A quick snapshot of key ESG metrics and progress (sample data).")

        # Display some Key KPIs side by side
        col1, col2, col3 = st.columns(3)
        # GHG KPI
        ghg_2023 = df_ghg.loc[df_ghg["Year"] == 2023, "Scope 1+2 GHG"].values[0]
        col1.metric("GHG (Scope 1 & 2, 2023)", f"{ghg_2023:.2f} Mt CO2e", "-4.94% vs 2022")

        # Water KPI
        water_2023 = df_water.loc[df_water["Year"] == 2023, "Freshwater_m3"].values[0]
        col2.metric("Freshwater (2023)", f"{water_2023:.1f}M m³", "-11% vs 2022")

        # Waste KPI
        waste_2023 = df_waste.loc[df_waste["Year"] == 2023, "Hazardous_t"].values[0]
        col3.metric("Hazardous Waste (2023)", f"{waste_2023:.1f}k tonnes", "-17% vs 2022")

        st.markdown("### GHG Emissions Trend (2018–2023)")
        fig_ghg_trend = px.line(
            df_ghg,
            x="Year",
            y="Scope 1+2 GHG",
            markers=True,
            title="Historical GHG Emissions (Mt CO2e)"
        )
        st.plotly_chart(fig_ghg_trend, use_container_width=True)

        st.markdown("### Water Withdrawal (Fresh vs. Non-Fresh)")
        df_water_melted = df_water.melt(id_vars=["Year"], value_vars=["Freshwater_m3","NonFreshwater_m3"],
                                        var_name="Type", value_name="Volume_m3")
        fig_water_bar = px.bar(
            df_water_melted,
            x="Year",
            y="Volume_m3",
            color="Type",
            barmode="group",
            title="Water Withdrawal (million m³)"
        )
        st.plotly_chart(fig_water_bar, use_container_width=True)

        add_footer()

    ###############################################################################
    # TAB 1: CLIMATE & GHG
    ###############################################################################
    with tabs[1]:
        st.subheader("Climate & GHG Emissions")
        st.write("Dive deeper into emissions data and test reduction scenarios.")

        # Show table or chart of GHG
        fig_ghg_scatter = px.scatter(
            df_ghg,
            x="Year",
            y="Scope 1+2 GHG",
            size="Scope 1+2 GHG",
            title="Scope 1 & 2 Emissions by Year",
            labels={"Scope 1+2 GHG": "GHG (Mt CO2e)"}
        )
        st.plotly_chart(fig_ghg_scatter, use_container_width=True)

        st.markdown("#### Additional Reduction Scenario")
        addl_reduction = st.slider("Additional % reduction in GHG by 2030 vs baseline", 0, 30, 10)
        
        df_ghg_scenario = apply_ghg_scenario(df_ghg, addl_reduction)
        fig_ghg_scenario = px.line(
            df_ghg_scenario,
            x="Year",
            y="Scope 1+2 GHG",
            markers=True,
            title=f"Emissions with Additional {addl_reduction}% Reduction (Illustrative)"
        )
        st.plotly_chart(fig_ghg_scenario, use_container_width=True)

        st.write("**Scenario Table:**")
        st.dataframe(df_ghg_scenario.style.highlight_min(color="lightgreen", subset=["Scope 1+2 GHG"]))

        add_footer()

    ###############################################################################
    # TAB 2: WATER & WASTEWATER
    ###############################################################################
    with tabs[2]:
        st.subheader("Water & Wastewater Management")
        st.write("Analyze water usage, discharge, recycling, and scenario planning.")

        # Basic chart
        fig_water_base = px.bar(
            df_water,
            x="Year",
            y=["Freshwater_m3","NonFreshwater_m3"],
            barmode="group",
            title="Water Withdrawal (million m³)"
        )
        st.plotly_chart(fig_water_base, use_container_width=True)

        st.markdown("#### Investment in Water Recycling Scenario")
        inv_slider = st.slider("Investment in Water Recycling (Million USD)", 0, 50, 10)
        df_water_scenario, r_pct = apply_water_scenario(df_water, inv_slider)

        st.write(f"Estimated reduction in freshwater usage: **{r_pct}%** (from baseline)")

        fig_water_scenario = px.bar(
            df_water_scenario,
            x="Year",
            y=["Freshwater_m3","NonFreshwater_m3"],
            barmode="group",
            title=f"Water With Investment = ${inv_slider}M"
        )
        st.plotly_chart(fig_water_scenario, use_container_width=True)

        st.write("**Scenario Table:**")
        st.dataframe(df_water_scenario.style.highlight_min(
            color="lightblue", 
            subset=["Freshwater_m3","NonFreshwater_m3"]
        ))

        add_footer()

    ###############################################################################
    # TAB 3: ENERGY & EFFICIENCY
    ###############################################################################
    with tabs[3]:
        st.subheader("Energy & Efficiency")
        st.write("View total energy consumption, renewables share, and efficiency scenarios.")

        # Current Data
        fig_energy = px.line(
            df_energy,
            x="Year",
            y="Total_Energy_GJ",
            markers=True,
            title="Total Energy Consumption (million GJ)"
        )
        st.plotly_chart(fig_energy, use_container_width=True)

        st.markdown("### Renewables Share Over Time")
        fig_renewables = px.bar(
            df_energy, 
            x="Year", 
            y="Renewables_%",
            title="Share of Renewables (%)"
        )
        st.plotly_chart(fig_renewables, use_container_width=True)

        st.markdown("#### Solar Capacity Scenario")
        solar_mw = st.slider("Additional Solar Capacity (MW)", 0, 100, 20)
        df_energy_scenario = apply_energy_scenario(df_energy, solar_mw)

        fig_energy_scenario = px.bar(
            df_energy_scenario, 
            x="Year", 
            y="Renewables_%",
            title=f"Renewables % with +{solar_mw} MW of Solar"
        )
        st.plotly_chart(fig_energy_scenario, use_container_width=True)

        st.write("**Scenario Table:**")
        st.dataframe(df_energy_scenario.style.highlight_max(
            color="lightgreen",
            subset=["Renewables_%"]
        ))

        add_footer()

    ###############################################################################
    # TAB 4: CIRCULAR & WASTE
    ###############################################################################
    with tabs[4]:
        st.subheader("Circular Economy & Waste Management")
        st.write("Hazardous vs non-hazardous waste, disposal methods, re-use scenario, etc.")

        
        st.markdown("#### Byproduct Reuse Scenario")
        reuse_slider = st.slider("Potential Additional Byproduct Reuse (k tonnes)", 0, 20, 5)
        df_waste_scenario = apply_waste_scenario(df_waste, reuse_slider)

        fig_waste_scenario = px.bar(
            df_waste_scenario,
            x="Year",
            y=["Hazardous_t", "NonHazardous_t"],
            barmode="group",
            title=f"Waste Levels with {reuse_slider}k Reuse"
        )
        st.plotly_chart(fig_waste_scenario, use_container_width=True)

        st.write("**Scenario Table:**")
        st.dataframe(df_waste_scenario.style.highlight_min(
            color="lightyellow",
            subset=["Hazardous_t","NonHazardous_t"]
        ))

        add_footer()

    ###############################################################################
    # TAB 5: BIODIVERSITY & OVERALL
    ###############################################################################
    with tabs[5]:
        st.subheader("Biodiversity & Integrated ESG Scenario")
        st.write("Track biodiversity initiatives and run an overall multi-parameter scenario.")

        # Show sample biodiversity data
        fig_biod = px.line(
            df_biod,
            x="Year",
            y="Habitat_Restored_km2",
            markers=True,
            title="Habitat Restored Over Time (km²)"
        )
        st.plotly_chart(fig_biod, use_container_width=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.metric("Sites w/ Projects (2023)", df_biod["Sites_with_Projects"].iloc[-1])

        with col_b2:
            st.metric("Habitat Restored (2023)", f"{df_biod['Habitat_Restored_km2'].iloc[-1]} km²")

        st.markdown("### Combine All Scenario Inputs")

        st.info("Below is a simplified example of how we might combine multiple scenario levers into a single ESG 'score' or index. Adjust weights and formula as you see fit.")

        # We re-ask user for scenario levers for demonstration:
        addl_ghg_red_input = st.slider("GHG Additional Reduction (%)", 0, 30, 10, key="biod_ghg")
        water_invest_input = st.slider("Water Investment ($M)", 0, 50, 10, key="biod_water")
        solar_mw_input = st.slider("Solar Capacity (MW)", 0, 50, 20, key="biod_solar")
        waste_reuse_input = st.slider("Waste Reuse (k tonnes)", 0, 10, 5, key="biod_waste")

        final_score = combined_esg_scenario(
            addl_ghg_red_input,
            water_invest_input,
            solar_mw_input,
            waste_reuse_input
        )

        st.success(f"**Overall ESG Scenario Score:** {final_score} / 100 (Higher is better)")

        add_footer()

######################
#     RUN THE APP    #
######################

if __name__ == "__main__":
    main()
