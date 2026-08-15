# SpaceX Falcon 9 First-Stage Landing Prediction, Data Science Capstone

Predicting whether a Falcon 9 first-stage booster will land successfully, using data collected from the SpaceX API and Wikipedia, explored with SQL and visualization, mapped interactively with Folium, presented in a Plotly Dash dashboard, and modeled with four classifiers (Logistic Regression, SVM, Decision Tree, KNN).

## Contents

| Folder / File | Description |
|---|---|
| `notebooks/01_data_collection_api.ipynb` | Collects launch records from the public SpaceX v4 REST API and flattens rocket/payload/launchpad/core references into one table. |
| `notebooks/02_data_collection_webscraping.ipynb` | Scrapes the Wikipedia "List of Falcon 9 and Falcon Heavy launches" page with BeautifulSoup to cross-check and enrich the API data. |
| `notebooks/03_data_wrangling.ipynb` | Cleans the combined dataset and derives the binary `Class` landing-outcome label. **Executed** — all outputs are real, generated from `data/dataset_part_1.csv`. |
| `notebooks/04_eda_sql.ipynb` | Loads the dataset into SQLite and answers standard EDA questions (launch site totals, payload stats, outcome counts, orbit breakdown) via SQL queries. **Executed.** |
| `notebooks/05_eda_visualization.ipynb` | Matplotlib/Seaborn charts relating flight number, payload mass, orbit, launch site and outcome; also produces the one-hot-encoded feature set used for modeling. **Executed** — 6 real chart outputs embedded. |
| `notebooks/06_folium_map.ipynb` | Interactive Folium map: launch site markers, a MarkerCluster of every individual launch color-coded by outcome, and a distance line from a pad to the nearest coastline. **Executed** — produces `interactive_map/spacex_launch_sites_map.html`. |
| `notebooks/07_predictive_analysis_classification.ipynb` | Standardizes features, splits data (72 train / 18 test), tunes 4 classifiers with `GridSearchCV`, and compares test accuracy. **Executed** — real results: all 4 models score 83.33% test accuracy; SVM's best kernel is `sigmoid`. |
| `dashboard/spacex_dash_app.py` | Plotly Dash app: launch-site dropdown, payload-mass range slider, a pie chart of success rate and a scatter chart of payload vs. outcome, both updating live from the two filters. |
| `interactive_map/spacex_launch_sites_map.html` | Standalone interactive Folium map (open directly in a browser). |
| `data/dataset_part_1.csv` | Wrangled base dataset (90 Falcon 9 launches, 2010–2020). |
| `data/dataset_part_2.csv` | `dataset_part_1.csv` plus the binary `Class` landing-outcome label. |
| `data/dataset_part_3.csv` | One-hot-encoded feature set (80 columns) used for model training. |
| `presentation/SpaceX_Capstone_Presentation.pdf` | Final capstone presentation (submitted to Coursera). |

## Key results

- 90 launches analyzed (2010–2020); overall landing success rate 66.7%.
- Launch sites: CCAFS SLC-40 (55 launches, 60.0% success), KSC LC-39A (22, 77.3%), VAFB SLC-4E (13, 76.9%).
- Most common target orbit: GTO (27 launches).
- Best model: SVM with a sigmoid kernel, 84.8% cross-validated training accuracy; all four models (Logistic Regression, SVM, Decision Tree, KNN) tie at 83.33% test accuracy on the 18-sample held-out set.

## Running locally

```bash
pip install pandas numpy matplotlib seaborn scikit-learn folium plotly dash beautifulsoup4 requests jupyter

# Notebooks
jupyter notebook notebooks/

# Dashboard (from the dashboard/ folder, so it finds dataset_part_1.csv)
cd dashboard && python spacex_dash_app.py
```

## Author

Jessica Beale
