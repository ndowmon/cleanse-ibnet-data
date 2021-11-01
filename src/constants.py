from os import path

DATA_DIR = path.abspath(path.join(path.dirname(path.abspath(__file__)), '../data'))
DATA_INPUT_DIR = path.join(DATA_DIR, 'input')
DATA_OUTPUT_DIR = path.join(DATA_DIR, 'output')
DATA_OUTPUT_INDIVIDUAL_DIR = path.join(DATA_OUTPUT_DIR, 'individual')

EXCEL_FILE_NAME = path.join(DATA_DIR, 'input/IBNET_export.xlsx')

MERGED_OUTPUT_FILE_NAME = path.join(DATA_OUTPUT_DIR, 'merged-ibnet-data.csv')

def get_output_file_for_sheet(sheet_name):
  return path.join(DATA_OUTPUT_INDIVIDUAL_DIR, "sheet_" + sheet_name + ".csv")

