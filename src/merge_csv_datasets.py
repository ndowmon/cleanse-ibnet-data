from constants import DATA_OUTPUT_INDIVIDUAL_DIR, MERGED_OUTPUT_FILE_NAME
from os import listdir, path
import pandas as pd


def run(directory_name, merged_output_file_name):
  merged_df = pd.DataFrame(
    index=pd.MultiIndex(
        names=['utility', 'year'], 
        levels=[[],[]], 
        codes=[[],[]]
    )
  )
  for filename in listdir(directory_name):
    file = path.join(directory_name, filename)
    print(file)
    df = pd.read_csv(file, index_col=['utility', 'year'])
    merged_df = pd.concat(
      [merged_df, df],
    )
  merged_df.to_csv(merged_output_file_name)




run(DATA_OUTPUT_INDIVIDUAL_DIR, MERGED_OUTPUT_FILE_NAME)
