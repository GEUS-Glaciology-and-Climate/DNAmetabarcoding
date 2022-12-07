#!/usr/bin/env python
"""
Splice and dice some files for Heike Zimmerman
Patrick Wright, GEUS
Dec, 2022

This assumes we have 'input' directory created with three required files.
The output directory and file will be created.

NOTE: this can go a lot faster if needed! (currently takes ~9 min)
Using numpy arrays instead of pandas, and potentially using numba on the for loop
"""
import pandas as pd
import numpy as np
import os
from progress.bar import Bar
# from IPython import embed # for debugging

# ============================================================
# Define input filepaths
test_shortnames_input = 'input/test_shortnames.tab'
statistics_swarm_input = 'input/statistics_swarm_fastidious_shortnames.txt'
listofclusters_input = 'input/listofclusters_AMD18S_swarm_fastidious_shortnames.txt'

# Define output filepath
if not os.path.exists('output'):
	os.makedirs('output')
output_file = 'output/final_contengency.txt'
# ============================================================

print('reading input files')
og_contingency = pd.read_csv(test_shortnames_input, sep='\t')
stats_file = pd.read_csv(statistics_swarm_input, header=None, sep='\t')

print('creating dataframe for final_contingency table')
# rename first three columns in stats_file
stats_file.rename(
	columns={stats_file.columns[0]: "unique_ID_count",
			 stats_file.columns[1]: "cluster_total_counts",
			 stats_file.columns[2]: "seed_ID",
	},
	inplace = True
	)

# Create an empty dataframe that will be our final output file
# Use the columns from og_contingency dataframe
final_contingency = pd.DataFrame(columns=og_contingency.columns)

# Assign additional columns to final_contingency dataframe
final_contingency['sequences_in_swarm'] = np.nan
final_contingency['id'] = stats_file['seed_ID']
final_contingency['count'] = stats_file['cluster_total_counts']
final_contingency['sequences_in_swarm'] = stats_file['unique_ID_count']
final_contingency['seq_rank'] = og_contingency['seq_rank']
final_contingency['sequence'] = og_contingency['sequence']

# Set the index to 'id'. This makes it easier to assign data based on the id.
final_contingency = final_contingency.set_index('id')

# Get the column names from og_contingency for each sample
filter_cols = [col for col in og_contingency if col.startswith('sample')]
# Add an 'id' column name
filter_cols_with_id = ['id'] + filter_cols

print('reading listofclusters input file')
num_lines = sum(1 for line in open(listofclusters_input))
with open(listofclusters_input) as f:
	# This speeds up as we go, as the line lengths get shorter
	bar = Bar('Processing lines...', max=num_lines)
	for line in f:
		temp_table = pd.DataFrame(columns=filter_cols_with_id)
		seed_ID = line.split(';')[0]
		line_ID_list = line.split(' ')
		for i in line_ID_list:
			line_id = i.split(';')[0]
			og_cont_row = og_contingency.loc[og_contingency['id'] == line_id][filter_cols_with_id]
			# Note, the temp_table will end up with random integer index positions without the following line,
			# which is OK (index not used/needed), so leaving this out to maybe gain some performance.
			# og_cont_row = og_cont_row.reset_index().drop('index', axis=1)
			temp_table = pd.concat([temp_table, og_cont_row]) # add the row to temp_table
		# we are done assigning each row into temp table from og_contingency, now sum and assign to final_contingency
		for column in temp_table:
			if column not in ('id',):
				final_contingency.at[seed_ID,column] = temp_table[column].sum()
		bar.next()
	bar.finish()
	print('All lines in listofclusters processed!')

print('Writing final_contingency file...')
final_contingency.reset_index(inplace=True)
final_contingency.to_csv(output_file, sep="\t", index=False)
print('FINISHED')