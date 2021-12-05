import pandas as pd

startup_file = "data/startup_scores.csv"
compatibility_file = "data/mult_startup_scores.csv"

startup_scores = pd.read_csv(startup_file, sep=r',')
compatibility_scores = pd.read_csv(compatibility_file, sep=r',', index_col=0)

def find_matches(company_name, is_mult, n=10):
    if not is_mult:
        '''
        find top 10 most compatible multinationals
        '''
        my_score = startup_scores[company_name]

        corrs = compatibility_scores.loc[company_name]
        return corrs.sort_values(0).tail(n)

    else:
        '''
        awesome score = compatible score + start up score 
        find top 10 most awesome startups 
        '''
        corrs = compatibility_scores.transpose().loc[[company_name, "SCORE"]].transpose()


        return corrs.assign(f=corrs[company_name] + corrs['SCORE'] * 5).sort_values('f').drop('f',axis=1).tail(n)


a = find_matches("Axiado", True, 2)
print(a)
#find_matches("CyberArk", False, 2)
