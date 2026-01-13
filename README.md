# Data Scientist Skill Demand Analysis

## Project Overview
This project analyzes **Data Scientist job postings** to identify:
- Most in-demand technical skills
- Skill combinations employers look for
- How skills co-occur in real job ads

The goal is to provide **data-driven insights** for job seekers and recruiters.

---

## Data
- [Source: LinkedIn job postings (2024)]{https://www.kaggle.com/datasets/wilomentena/linkedin-data-scientistanalyst-jobs-berlin-2024/data}
- Focus: **Data Scientist roles only**
- Total job ads analyzed: **60**

Job descriptions were cleaned and analyzed using NLP and regex-based skill extraction.

---

## Key Insights
- **Python** appears in over **90%** of Data Scientist roles
- **Machine Learning** is required in **85%** of postings
- **SQL and R** are equally demanded (~52%)
- Cloud & big data skills (AWS, Spark, GCP) are common in senior roles
- Skills like NLP, Deep Learning, and Recommendation Systems indicate specialization

---

## Dashboard Features
Built with **Streamlit**:
- Interactive skill demand charts
- Skill co-occurrence heatmap
- Job explorer with skill-based filtering

---

## Tech Stack
- Python
- pandas, numpy
- matplotlib
- regex, NLP
- Streamlit

---

## How to Run
```bash
pip install -r requirements.txt
python -m streamlit run app/app.py
```

---

## Project Structure
```text

berlin-ds-skill-demand/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/                # (OPTIONAL – usually NOT uploaded)
│   └── processed/
│       └── berlin_data_scientist_jobs_clean.csv
│
├── notebooks/
│   └── 01_load_and_filter.ipynb
│
├── src/                    # optional (if used)
│
├── requirements.txt
├── README.md
└── .gitignore

```

## UI Screenshot
### Dashboard Screenshot:

![dashboard_page-0001](https://github.com/user-attachments/assets/9d1423cc-1a5a-469c-ba96-d9e910cb0477)
![dashboard_page-0002](https://github.com/user-attachments/assets/008333f2-934b-4deb-9f00-722afe67853e)


### Co-occurance
![Co_occureance_page-0001](https://github.com/user-attachments/assets/68887f5f-8229-4951-8f35-4a5ab2228a94)
![Co_occureance_page-0002](https://github.com/user-attachments/assets/ddef4d7e-406e-4e7d-a069-ace7a82c6a52)

### Job Explorer
![Job_explore_page-0001](https://github.com/user-attachments/assets/1cd3f2f6-cc90-42bd-bbce-6b63c02992d2)
![Job_explore_page-0002](https://github.com/user-attachments/assets/cc523999-e276-4a1c-bb3b-981a7d47f091)





___Thank You___
