import itertools
import math
import pandas as pd
from scipy import stats

from catan.settings import DB_CONFIG

def load_data():
    df_exp = pd.read_sql_table('experiment', DB_CONFIG['path'])
    df_exp.rename(columns={'id': 'experiment_id'}, inplace=True)

    df_trial = pd.read_sql_table('trial', DB_CONFIG['path'])
    df_trial.rename(columns={'id': 'trial_id'}, inplace=True)
    
    df_trial_roll = pd.read_sql_table('trial_roll', DB_CONFIG['path'])
    
    df_trial_roll_join = df_trial.join(df_trial_roll.set_index('trial_id'), on='trial_id')
    df_full = df_exp.join(df_trial_roll_join.set_index('experiment_id'), on='experiment_id')
  
    return df_full


def describe_settlement_pattern(df_full):
    return df_full.groupby(by=['settlement_pattern'])['resource_count'].describe()


def test_settlement_pattern_difference(df_full):
    # Is it okay to assume the variance is the same? 
    # What evidence supports the claim?
    # What evidence opposes the claim?
    settlement_patterns = df_full['settlement_pattern'].unique()
    combinations = itertools.combinations(settlement_patterns, 2)

    ttest_results_list = []
    for c in combinations:
        df_pattern_0 = df_full[df_full['settlement_pattern'] == c[0]]
        df_pattern_1 = df_full[df_full['settlement_pattern'] == c[1]]
        p_test_value = 0.01
        ttest_result = stats.ttest_ind(df_pattern_1['resource_count'], df_pattern_0['resource_count'], equal_var=False)
        ttest_results_list.append(
                {
                'pattern_a': c[0],
                'pattern_b': c[1],
                'statistic': ttest_result.statistic,
                'pvalue': ttest_result.pvalue,
                f'significant_at_{p_test_value}': p_test_value > ttest_result.pvalue
            }
        )
    return pd.DataFrame.from_records(ttest_results_list)
    