import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="India Census 2011 | Data Visualization",
    # page_icon="IN",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("india_census_2011.csv")

    # Create useful calculated metrics
    df["Internet Penetration (%)"] = (
            df["Households_with_Internet"]
            / (df["Rural_Households"] + df["Urban_Households"])* 100
    )

    return df


df = load_data()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("India Census 2011 — Interactive Data Visualization")

st.markdown(
    """
    Explore district-level demographic and household data across India
    using an interactive map.

    **Map Size** → Primary Parameter  
    **Map Color** → Secondary Parameter
    """
)

st.divider()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Dashboard Controls")

# State selection
list_of_states = sorted(df["State"].unique().tolist())
list_of_states.insert(0, "Overall India")

selected_state = st.sidebar.selectbox(
    "Select State",
    list_of_states
)

# Parameters
parameter_columns = [
    "Households_with_Internet",
    "Rural_Households",
    "Urban_Households",
    "Population",
    "Sex Ratio",
    "Literacy Rate",
    "Internet Penetration (%)"
]

primary = st.sidebar.selectbox("Primary Parameter",parameter_columns)

secondary = st.sidebar.selectbox("Secondary Parameter",parameter_columns)

plot = st.sidebar.button("Generate Visualization",use_container_width=True)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------

if selected_state == "Overall India":
    selected_df = df.copy()
else:
    selected_df = df[df["State"] == selected_state].copy()

# --------------------------------------------------
# KPI Section
# --------------------------------------------------

st.subheader("Key Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Districts",selected_df["District"].nunique())

col2.metric("Avg. Sex Ratio",f"{selected_df['Sex Ratio'].mean():.1f}")

col3.metric("Avg. Literacy Rate",
                f"{selected_df['Literacy Rate'].mean():.1f}%")

col4.metric("Population",f"{selected_df['Population'].sum():,.0f}")

st.divider()

# --------------------------------------------------
# Map
# --------------------------------------------------

if plot:

    st.subheader(f"District-Level Visualization — {selected_state}")

    st.info(f"**Size:** {primary}  |  **Color:** {secondary}")

    # Zoom based on selection
    if selected_state == "Overall India":
        zoom_level = 4
    else:
        zoom_level = 6

    fig = px.scatter_map(
        selected_df,
        lat="Latitude",
        lon="Longitude",
        size=primary,
        color=secondary,
        zoom=zoom_level,
        size_max=35,
        map_style="carto-positron",
        width=1400,
        height=850,
        hover_name="District",
        hover_data={
            "State": True,
            "Population": ":,.0f",
            "Sex Ratio": ":.1f",
            "Literacy Rate": ":.1f",
            primary: ":.1f",
            secondary: ":.1f",
            "Latitude": False,
            "Longitude": False
        }
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        " Select the parameters from the sidebar and click\n\n"
        "**Generate Visualization** to display the map."
    )

# --------------------------------------------------
# Data Preview
# --------------------------------------------------

with st.expander("View Dataset"):
    st.write(f"Showing **{len(selected_df)} districts**")

    st.dataframe(
        selected_df,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# Download Data
# --------------------------------------------------

st.subheader("Download Data")

csv = selected_df.to_csv(index=False)

st.download_button(
    label="Download Selected Data as CSV",
    data=csv,
    file_name=f"{selected_state.replace(' ', '_')}_census_2011.csv",
    mime="text/csv"
)

# --------------------------------------------------
# About Project
# --------------------------------------------------

st.divider()

with st.expander("About This Project"):
    st.markdown(
        """
        ### India Census 2011 Data Visualization

        This project demonstrates an interactive district-level
        visualization of Indian Census 2011 data using **Python,
        Pandas, Plotly and Streamlit**.

        **Features**

        - State-wise filtering
        - Interactive geographic visualization
        - Primary and secondary parameter selection
        - District-level demographic analysis
        - Key statistics
        - Dataset preview
        - CSV download

        **Technology Used**

        - Python
        - Pandas
        - Plotly
        - Streamlit

        **Project Goal**

        The goal of this project is to transform raw census data
        into an easy-to-understand interactive dashboard.
        """
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "Built with Python + Streamlit • India Census 2011 Data Visualization"
)