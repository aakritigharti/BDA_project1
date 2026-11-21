                                                    ||"Book Analytics Project"||

#Project Overview
The "Book Analytics Project" is an end-to-end data analytics project that explores book-related information using the Open Library API.
The project focuses on extracting, cleaning, transforming, analyzing, and visualizing book data to discover meaningful insights about books, authors, publication years, editions, subjects, and cover availability.

The analysis uses Python, SQL, PostgreSQL, and Power BI to demonstrate a complete data analytics workflow.

#Project Objectives
- Extract book information using the Open Library API.
- Clean and preprocess raw book datasets using Python.
- Analyze book data using SQL and Python.
- Explore book publication trends, authors, subjects, and editions.
- Identify books with multiple authors.
- Analyze book cover availability.
- Build an interactive Power BI dashboard to present insights.

#Technologies Used
-Programming Language: Python
-Data Extraction: Open Library API, Requests
-Data Cleaning: Pandas, NumPy
-Data Visualization: Matplotlib, Seaborn
-Database: PostgreSQL
-SQL Environment: DBeaver
-Data Analysis: SQL, Python 
-Dashboard: Microsoft Power BI
-Development Environment: Jupyter Notebook, VS Code
-Version Control: Git and GitHub

#Project Structure
BDA_project1/
│
├── data/
│   ├── raw/
│   │   └── open_library_raw.csv
│   └── cleaned/
│       └── open_library_cleaned.csv
│
├── notebook/
│   └── book_analytics.ipynb
│
├── powerbi/
│   └── Power BI dashboard
│
├── scripts/
│
├── sql/
│    
├── .gitignore
├── requirements.txt
└── README.md


#Project Workflow
1. Data Extraction
- Retrieved book information from the Open Library API.
- Collected details such as book titles, authors, publication years, subjects, ISBNs, languages, publishers, and editions.

2. Data Cleaning and Preprocessing
- Handled missing and inconsistent values.
- Removed duplicate records where appropriate.
- Standardized date formats.
- Cleaned author and subject information.
- Created additional analytical columns such as author count and subject count.
- Prepared the cleaned dataset for analysis.

3. Database Management
- Imported the cleaned CSV dataset into PostgreSQL.
- Connected PostgreSQL with DBeaver.
- Performed data exploration and analytical queries using SQL.

4. Data Analysis
Analyzed different aspects of the book dataset, including:
- Top 10 books.
- Books with multiple authors.
- Publication trends.
- Edition distribution.
- Cover availability.
- Author and subject distribution.

5. Data Visualization
Developed an interactive Power BI dashboard featuring:
- KPI cards.
- Top 10 books visualization.
- Pie charts.
- Bar charts.
- Book cover status analysis.
- Edition and author-related analysis.

#Power BI Dashboard
The dashboard provides an interactive overview of the book dataset, helping users explore book characteristics and identify patterns in the collected data.

#How to Run the Project
Step 1: Clone the Repository
git clone https://github.com/aakritigharti/BDA_project1.git

Step 2: Navigate to the Project
cd BDA_project1

Step 3: Create a Virtual Environment
python -m venv penv

Activate it on Windows:
penv\Scripts\activate

Step 4: Install Dependencies
pip install -r requirements.txt

Step 5: Open the Jupyter Notebook
jupyter notebook

Open `notebook/book_analytics.ipynb` to explore the Python analysis.

#Key Learning Outcomes
- Working with real-world API data.
- Data extraction and preprocessing using Python.
- Handling missing values and inconsistent data.
- Writing SQL queries for analytical purposes.
- Working with PostgreSQL databases.
- Developing interactive dashboards using Power BI.
- Understanding an end-to-end data analytics workflow.
- Managing projects using Git and GitHub.

Author
Aakriti Gharti
Computer Engineering Graduate

GitHub: [aakritigharti](https://github.com/aakritigharti)

This project was developed as part of my practical learning journey in Data Analytics.
