import pandas as pd
import pm4py

eve_df = pm4py.read_ocel("./my_data/recruiting.jsonocel")


#dataframe = pd.read_csv("./my_data/recruiting.csv")
#print(dataframe['ocel:activity'].unique())

"""
objects = ['vacancies', 'managers', 'applicants', 'applications', 'recruiters', 'offers']
for obj in objects:    
    flattend_df = pm4py.ocel_flattening(eve_df, obj)
    print(flattend_df)
    flattend_log = pm4py.convert_to_event_log(flattend_df)
    pm4py.write_xes(flattend_log, f"./my_data/recruiting/flat_{obj}.xes")
"""
    

"""
filtered_log = pm4py.filter_variants_by_coverage_percentage(flattend_log, 0.01)
print(filtered_log)
vacancies_dfg, starts, ends = pm4py.discover_dfg(filtered_log)
pm4py.view_dfg(vacancies_dfg, starts, ends, format='svg')
print("Done")
"""