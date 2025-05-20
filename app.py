import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns  # Added seaborn import
import re

# Load default dataset
st.title("📊 LinkedIn Data Job Market Analysis")

# Load dataset from file if exists, else wait for upload
default_data_path = "jobs.csv"
try:
    df = pd.read_csv(default_data_path)
    df.columns = df.columns.str.strip().str.lower()
    st.markdown("Analyze data-related roles scraped from LinkedIn to uncover trends, skill demands, and work type distributions.")
    
    # Fill missing descriptions with empty string for safety
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    else:
        st.warning("Column 'description' is missing in the default dataset.")

    # View raw data
    with st.expander("📂 View Raw Dataset"):
        st.write(df.head())

    # -----------------------
    # Skill Extraction
    # -----------------------
    st.header("💡 Top In-Demand Skills")
    # Define a simple keyword skill list
    skills = ["Python", "SQL", "R", "Excel", "Power BI", "Tableau", "AWS", "Azure", "Spark", "TensorFlow", "scikit-learn"]

    def extract_skills(text):
        text = str(text).lower()
        return [skill for skill in skills if skill.lower() in text]

    if 'description' in df.columns:
        df['Skills'] = df['description'].apply(extract_skills)

        # Count skill frequency
        flat_skills = [skill for sublist in df['Skills'] for skill in sublist]
        skill_freq = pd.Series(flat_skills).value_counts()

        st.bar_chart(skill_freq.head(10))
    else:
        st.warning("Column 'description' not found for skill extraction.")

    # -----------------------
    # Top Job Titles
    # -----------------------
    st.header("🎯 Most Common Job Titles")
    if 'title' in df.columns:
        st.bar_chart(df['title'].value_counts().head(10))
    else:
        st.warning("Column 'title' not found.")

    # -----------------------
    # Optional: "About Me" Generator
    # -----------------------
    st.header("📝 Auto Generate 'About Me' From a Job Description")
    sample_desc = st.text_area("Paste a job description below:", height=200)

    if st.button("Generate Summary"):
        if sample_desc.strip():
            matched_skills = extract_skills(sample_desc)
            st.success("Here's your personalized 'About Me' 👇")
            st.write(f"""
I am a data professional with strong experience in tools and technologies such as {", ".join(matched_skills)}.
I’m passionate about applying data science to solve real-world problems, and I strive to bring business value using analytical insights.
            """)
        else:
            st.error("Please paste a job description first.")

except FileNotFoundError:
    st.warning(f"Default dataset '{default_data_path}' not found. Please upload your dataset below.")

st.title("🔍 LinkedIn Data Science Job Market Explorer ")

# Upload dataset
uploaded_file = st.file_uploader("Upload LinkedIn Job Dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    st.success("Dataset loaded successfully!")

    # Fill missing description column if exists
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    else:
        st.warning("Column 'description' is missing in the uploaded dataset.")

    # Preview data
    with st.expander("📄 Preview Dataset"):
        st.dataframe(df.head())

    # --- Skill Extraction ---
    skills = ["python", "sql", "excel", "power bi", "tableau", "r", "aws", "machine learning", "deep learning", "pandas", "numpy"]

    def extract_skills(text):
        text = str(text).lower()
        return [skill for skill in skills if skill in text]

    if 'description' in df.columns:
        df['skills'] = df['description'].apply(extract_skills)
        all_skills = sum(df['skills'], [])
        skill_counts = Counter(all_skills)
        top_skills = pd.DataFrame(skill_counts.most_common(), columns=['Skill', 'Frequency'])

        st.subheader("📊 Most In-Demand Skills")
        fig1, ax1 = plt.subplots()
        sns.barplot(data=top_skills, x='Frequency', y='Skill', ax=ax1)
        ax1.set_title("Top In-Demand Skills in Job Descriptions")
        st.pyplot(fig1)
    else:
        st.warning("Column 'description' missing for skill extraction.")

    # --- Job Titles ---
    if 'title' in df.columns:
        top_titles = df['title'].value_counts().nlargest(10).reset_index()
        top_titles.columns = ['Job Title', 'Count']

        st.subheader("📌 Most Common Job Titles")
        fig2, ax2 = plt.subplots()
        sns.barplot(data=top_titles, y='Job Title', x='Count', ax=ax2)
        ax2.set_title("Top 10 Job Titles")
        st.pyplot(fig2)
    else:
        st.warning("Column 'title' not found for job title analysis.")

    # --- Seniority Level ---
    def get_seniority(title):
        title = str(title).lower()
        if "intern" in title:
            return "Intern"
        elif "junior" in title:
            return "Junior"
        elif "senior" in title:
            return "Senior"
        elif "lead" in title or "principal" in title:
            return "Lead"
        else:
            return "Mid"

    if 'title' in df.columns:
        df['seniority'] = df['title'].apply(get_seniority)
        seniority_counts = df['seniority'].value_counts().reset_index()
        seniority_counts.columns = ['Seniority', 'Count']

        st.subheader("🧱 Job Seniority Levels")
        fig3, ax3 = plt.subplots()
        sns.barplot(data=seniority_counts, x='Seniority', y='Count', ax=ax3)
        ax3.set_title("Seniority Distribution")
        st.pyplot(fig3)
    else:
        st.warning("Column 'title' missing for seniority level extraction.")

    # --- Work Type & Employment Type ---
    if 'work_type' in df.columns:
        st.subheader("🌐 Work Type Distribution")
        work_type_counts = df['work_type'].value_counts().reset_index()
        work_type_counts.columns = ['Work Type', 'Count']
        fig4, ax4 = plt.subplots()
        sns.barplot(data=work_type_counts, x='Work Type', y='Count', ax=ax4)
        ax4.set_title("Work Type Distribution")
        st.pyplot(fig4)
    else:
        st.warning("Column 'work_type' not found in dataset.")

    if 'employment_type' in df.columns:
        st.subheader("📁 Employment Type Distribution")
        employment_counts = df['employment_type'].value_counts().reset_index()
        employment_counts.columns = ['Employment Type', 'Count']
        fig5, ax5 = plt.subplots()
        sns.barplot(data=employment_counts, x='Employment Type', y='Count', ax=ax5)
        ax5.set_title("Employment Type Distribution")
        st.pyplot(fig5)
    else:
        st.warning("Column 'employment_type' not found in dataset.")

else:
    st.info("Please upload a dataset to begin the analysis.")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Built by Nanier · Dataset: LinkedIn Job Posts · App powered by Streamlit")
