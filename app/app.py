import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations



#------------------------------
#Page Config
#------------------------------
st.set_page_config(
    page_title = "Data Scientist Skill Demand",
    layout = "wide"
)

st.title("Data Scientist Skills Demand Dashboard")
st.markdown("Analysis of **Data Scientist job posting** based on LinkedIN data")

# ---------------------
# Load Data
# ---------------------

@st.cache_data
def load_data():
    return pd.read_csv("D:/Project/Data Scientist/LinkedIn Data Scientist/data/processed/berlin_data_scientist_jobs_clean.csv")

df =load_data()

st.metric("Total Job Ads", len(df))


###------------------------------------
### Side bar Filters
#--------------------------------------

st.sidebar.header("🔎 Filters")

# Normalize column names ONCE
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# --- Job title filter ---
titles = sorted(df["job_title"].dropna().unique())

selected_titles = st.sidebar.multiselect(
    "Job Title",
    options=titles,
    default=titles
)

# Apply filter
filtered_df = df[df["job_title"].isin(selected_titles)].copy()

st.write("Rows after filters:", len(filtered_df))

# ------------------------------------
# Skill Extraction
# ------------------------------------

import re

SKILL_PATTERNS = {
    "python": r"\bpython\b",
    "sql": r"\bsql\b",
    "r": r"(?<!\w)r(?!\w)",
    "machine learning": r"\bmachine learning\b|\bml\b",
    "statistics": r"\bstatistic(s|al)?\b",
    "spark": r"\bspark\b|\bpyspark\b",
    "aws": r"\baws\b|\bamazon web services\b",
    "gcp": r"\bgcp\b|\bgoogle cloud\b",
    "deep learning": r"\bdeep learning\b|\bdl\b",
    "nlp": r"\bnlp\b|\bnatural language processing\b",
    "scikit-learn": r"\bscikit\-learn\b|\bsklearn\b",
    "tensorflow": r"\btensorflow\b",
    "pytorch": r"\bpytorch\b",
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b"
}

def extract_skills(text):
    found = []
    for skill, pat in SKILL_PATTERNS.items():
        if re.search(pat, text):
            found.append(skill)
    return found

filtered_df["skills"] = filtered_df["job_desc_clean"].apply(extract_skills)


# -----------------------
# Skill demand
# -----------------------
skill_counter = Counter(
    [s for skills in filtered_df["skills"] for s in skills]
)

skill_df = (
    pd.DataFrame(skill_counter.items(), columns=["Skill", "Count"])
    .sort_values("Count", ascending=False)
    .head(20)
)

st.subheader("🔥 Top Skills in Demand")

tab1, tab2, tab3 = st.tabs(["📊 Skill Demand", "🧩 Co-occurrence", "🔎 Job Explorer"])

with tab1:
    st.subheader("🔥 Top Skills in Demand")

    skill_counter = Counter([s for skills in filtered_df["skills"] for s in skills])
    skill_df = (
        pd.DataFrame(skill_counter.items(), columns=["Skill", "Count"])
        .sort_values("Count", ascending=False)
        .head(25)
    )
    skill_df["Percent of Jobs"] = (skill_df["Count"] / len(filtered_df) * 100).round(1)

    # Plot
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.barh(skill_df["Skill"][::-1], skill_df["Count"][::-1])
    ax.set_xlabel("Number of Job Ads")
    ax.set_ylabel("Skill")
    st.pyplot(fig)

    st.dataframe(skill_df, use_container_width=True)

with tab2:
    st.subheader("🧩 Skill Co-occurrence Heatmap")

    # Choose skills to include in heatmap
    all_skills = sorted({s for skills in filtered_df["skills"] for s in skills})
    default_skills = [s for s in ["python", "machine learning", "sql", "statistics", "aws", "gcp", "spark", "deep learning", "nlp"] if s in all_skills]

    selected_skills = st.multiselect(
        "Select skills for the heatmap",
        options=all_skills,
        default=default_skills if len(default_skills) > 0 else all_skills[:10]
    )

    if len(selected_skills) < 2:
        st.info("Select at least 2 skills to see co-occurrence.")
    else:
        # Count pairs
        pair_counter = Counter()
        for skills in filtered_df["skills"]:
            skills_set = sorted(set(skills))
            # only keep selected skills
            skills_set = [s for s in skills_set if s in selected_skills]
            for a, b in combinations(skills_set, 2):
                pair_counter[(a, b)] += 1

        # Build matrix
        m = pd.DataFrame(0, index=selected_skills, columns=selected_skills)
        for (a, b), c in pair_counter.items():
            m.loc[a, b] = c
            m.loc[b, a] = c

        # Plot heatmap without seaborn (pure matplotlib)
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(9, 7))
        im = ax.imshow(m.values)

        ax.set_xticks(range(len(selected_skills)))
        ax.set_yticks(range(len(selected_skills)))
        ax.set_xticklabels(selected_skills, rotation=45, ha="right")
        ax.set_yticklabels(selected_skills)

        # annotate counts
        for i in range(len(selected_skills)):
            for j in range(len(selected_skills)):
                val = m.values[i, j]
                if val > 0 and i != j:
                    ax.text(j, i, str(val), ha="center", va="center")

        ax.set_title("Co-occurrence counts (how often two skills appear in the same ad)")
        fig.tight_layout()
        st.pyplot(fig)


with tab3:
    st.subheader("🔎 Browse Jobs & Skills")

    # Filter jobs by skill
    all_skills = sorted({s for skills in filtered_df["skills"] for s in skills})
    pick_skill = st.selectbox("Filter jobs that mention a skill", options=["(no filter)"] + all_skills)

    view_df = filtered_df.copy()
    if pick_skill != "(no filter)":
        view_df = view_df[view_df["skills"].apply(lambda xs: pick_skill in xs)].copy()

    st.write("Matching jobs:", len(view_df))

    # Show a small table
    cols_to_show = [c for c in ["job_title", "company_name", "job_level", "job_remote", "job_type", "link"] if c in view_df.columns]
    st.dataframe(view_df[cols_to_show].head(50), use_container_width=True)

    # Click a job to view details
    idx = st.number_input("Pick a row index to inspect (from the table above)", min_value=0, max_value=max(0, len(view_df)-1), value=0)
    if len(view_df) > 0:
        row = view_df.iloc[int(idx)]
        st.markdown(f"### {row.get('job_title','')}")
        st.write("Company:", row.get("company_name",""))
        st.write("Level:", row.get("job_level",""))
        st.write("Remote:", row.get("job_remote",""))
        st.write("Type:", row.get("job_type",""))
        if "link" in row and pd.notna(row["link"]):
            st.write("Link:", row["link"])
        st.write("Skills:", ", ".join(row.get("skills", [])))
        st.markdown("**Description (cleaned)**")
        st.write(row.get("job_desc_clean","")[:2500] + ("..." if len(row.get("job_desc_clean","")) > 2500 else ""))
