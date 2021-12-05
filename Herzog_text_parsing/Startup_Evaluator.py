import pandas as pd
from collections import defaultdict
from datetime import datetime

startup_file = "../Herzog_web_scraping/cybersecurity_startup_companies.csv"

df = pd.read_csv(startup_file)[["Company Name", "PRODUCT STAGE", "FOUNDED", "FUNDING STAGE", "Total raised"]]


def get_prod_score(prod_stage):
    if pd.isna(prod_stage):
        return 0, 0
    val_map = {"Customer development": 1, "Released": 9, "Beta": 7, "R&D": 2, "Alpha": 5, "Clinical trials": 3}
    if prod_stage in val_map:
        return val_map[prod_stage], 0.8
    else:
        return 0, 0


def get_founded_score(founded):
    if pd.isna(founded):
        return 0, 0
    val_map = defaultdict(lambda: 2)
    to_app = ({0:1, 1:1, 2:3, 3:5, 4:5, 5:7, 5:7, 7:8, 8:8, 9:8, 10:2})
    for key in to_app:
        val_map[key] = to_app[key]
    current_year = datetime.now().strftime('%Y')
    a = founded.split("/")
    if len(a) == 1:
        year_founded = a[0]
    else:
        year_founded = a[1]
    comp_age = int(current_year) - int(year_founded)

    return val_map[comp_age], 0.7



def get_funding_score(funding):
    if pd.isna(funding):
        return 0, 0
    else:
        return 5, 0.5


def get_stage_score(stage):
    if pd.isna(stage):
        return 0, 0
    val_map = {"Bootstrapped": 1, "Pre-Seed":2, "Seed": 3, "ROUND A": 7, "ROUND B": 8, "C": 3, "ROUND C+":7,
               "Public":5,"Revenue Financed": 6, "Established": 5}
    if stage in val_map:
        return val_map[stage], 0.8
    else:
        return 0, 0



def eval_company(opdict):
    prod_score, prod_weight = get_prod_score(opdict["PRODUCT STAGE"])
    founded_score, founded_weight = get_founded_score(opdict["FOUNDED"])
    stage_score, stage_weight = get_stage_score(opdict["FUNDING STAGE"])
    funding_score, funding_weight = get_funding_score(opdict["Total raised"])

    total_weight = prod_weight + founded_weight + stage_weight + funding_weight
    normed_score = (prod_weight * prod_score + founded_weight * founded_score +
                    stage_weight * stage_score + funding_weight * funding_score) / total_weight

    return opdict["Company Name"], normed_score


temp_dict = {}
for index, row in df.iterrows():
    company, score = eval_company(row.to_dict())
    temp_dict[company] = [score]
    #print(company, score)

print(temp_dict)

dfOut = pd.DataFrame.from_dict(temp_dict).transpose()
dfOut.columns = ["SCORE"]

dfOut.to_csv('data/startup_scores.csv')






