from Herzog_text_parsing.Text_Comparer import Comparer
import pandas as pd

startup_file = "../Herzog_web_scraping/cybersecurity_startup_companies.csv"

df = pd.read_csv(startup_file, nrows=5)[["Company Name", "TAGS"]]
print(df)

comp = Comparer(df["Company Name"].tolist(), df["TAGS"].tolist())
comp.compare_all_data()