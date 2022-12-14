# Packages
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector as connection

# Settings
st.set_option('deprecation.showPyplotGlobalUse', False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# Page Setup
st.set_page_config(
    page_title="DS7330 Final Project",
    layout="wide",
)

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return connection.connect(**st.secrets["mysql"])

mydb = init_connection()

# Refresh every 1000 minutes or when query changes.
# @st.experimental_memo(ttl=60000)
def load_data(query):
    df = pd.read_sql(query,mydb)
    return df

student_df = load_data("""
        select
            *
        from StudentDemographics

        left join BodySpecifics
        on BodySpecifics.StudentDemographics_StudentID = StudentDemographics.StudentID

        left join HomeLife
        on HomeLife.StudentDemographics_StudentID = StudentDemographics.StudentID

        left join MiscPreferences
        on MiscPreferences.StudentDemographics_StudentID = StudentDemographics.StudentID

        left join SocialActivity
        on SocialActivity.StudentDemographics_StudentID = StudentDemographics.StudentID

        left join WorldIssues
        on WorldIssues.StudentDemographics_StudentID = StudentDemographics.StudentID;
    """)

# Show variables and data types
# df.dtypes

# plotly charts
# https://plotly.com/python/plotly-express/


# Filter Variables
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
age_order = pd.unique(student_df['AgeSurveyed'])
age_order.sort()

student_df2 = student_df

# Dashboard Layout
# Title
st.title("Student Census Data")

# Sidebar
with st.sidebar:
    st.write("Filters")
    month_filter = st.multiselect("Birth Month", month_order, default=month_order)
    student_df2 = student_df2[student_df2["BirthMonth"].isin(month_filter)]

    age_filter = st.select_slider("Age Range",options=age_order, value=(min(student_df2['AgeSurveyed']),max(student_df2['AgeSurveyed'])))
    student_df2 = student_df2[student_df2["AgeSurveyed"].between(min(age_filter), max(age_filter))]

# Body
co11, col2 = st.columns(2)
col3, col4  = st.columns(2)
col5, col6= st.columns(2)

# Histogram of Height
with co11:
    fig = px.histogram(student_df2, x="Height", color="Gender", marginal="rug")
    st.markdown("Histogram - Height by Gender")
    st.plotly_chart(fig, use_container_width=True)
# Scatter plot Time w/ Family vs. Time Gaming
with col2:
    fig2 = px.scatter(student_df2, x="HrsSpentWithFamily", y="HrsGames", color="Gender")
    st.markdown("Scatter plot - Hours with Family vs Hours Gaming")
    st.plotly_chart(fig2, use_container_width=True)

# Parallel Categories - Gender and Birth Month
with col3:
    fig3 = px.parallel_categories(student_df2, dimensions=['Gender','BirthMonth'],color="AgeSurveyed", color_continuous_scale=px.colors.sequential.Inferno)
    st.markdown("Parallel Categories - Gender, Birth Month")
    st.plotly_chart(fig3, use_container_width=True)
# Bubble Plot - Armspan vs. Chore Hours by Year
with col4:
    fig4 = px.scatter(student_df2, x="YearSurveyed", y="Armspan", size="HrsChores", log_x=True, size_max=60)
    st.markdown("Bubble Plot - Armspan vs Chores by YearSurveyed")
    st.plotly_chart(fig4, use_container_width=True)

# Bar Plot - Social Media Hours by Gender
with col5:
    fig5 = px.bar(student_df2, x="YearSurveyed", y="HrsSocialMedia",color="Gender",barmode ="group")
    st.markdown("Social Media hrs by Gender")
    st.plotly_chart(fig5,use_container_width=True)

# Bar Plot - Memory Game Score vs. Academic Pressure by Gender
with col6:
    fig6 = px.bar(student_df2, x="MemoryGameScore", y="AcademicPressure",color="Gender",barmode ="group")
    st.markdown("Academic Pressure and MemoryGameScore")
    st.plotly_chart(fig6,use_container_width=True)
