from Herzog_text_parsing.Text_Comparer import Comparer
import pandas as pd

startup_file = "../Herzog_web_scraping/cybersecurity_startup_companies.csv"
multinational_file = "../Herzog_web_scraping/export_multinational_companies.csv"

startup_score_file = "data/startup_scores.csv"

startup_table = pd.read_csv(startup_file, sep=r',')[["Company Name", "TAGS"]]
#print(df0)
startup_names = startup_table["Company Name"].tolist()
startup_tags = startup_table["TAGS"].tolist()

multnt_table = pd.read_csv(multinational_file, sep=r',')[["Name of Company", "Company Tags"]]
#print(df1)
mult_names = multnt_table["Name of Company"].tolist()
mult_tags = multnt_table["Company Tags"].tolist()

comp = Comparer(startup_names, startup_tags, mult_names, mult_tags)
compat_scores_table = comp.compare_all_data()


startup_scores = pd.read_csv(startup_score_file, sep=r',', index_col=0)

dfOut = compat_scores_table.join(startup_scores, how="inner")



dfOut.to_csv('data/mult_startup_scores.csv')
