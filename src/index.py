import pandas as pd
import numpy as np
from os import path
from constants import EXCEL_FILE_NAME, get_output_file_for_sheet

SEQUENTIAL_VARIABLE_RENAMES = [
  { 'from_name': 'Wuvi Standard',	'to_name': 'wuvi'},
  { 'from_name': 'Wuvi (5)',	'to_name': 'wuvi5'},
  { 'from_name': 'Wuvi (7)',	'to_name': 'wuvi7'},
  { 'from_name': 'APGAR',	'to_name': 'apgar'},
  { 'from_name': 'Gross Fixed Assets – water & wastewater', 'to_name':	'gross_fixed_assets_$_pop_watww'},
  { 'from_name': 'Gross Fixed Assets - water', 'to_name':	'gross_fixed_assets_$_pop_wat'},
  { 'from_name': 'Gross Fixed Assets – wastewater', 'to_name':	'gross_fixed_assets_$_pop_ww'},
  { 'from_name': 'Gross Fixed Assets – water & wastewater', 'to_name':	'gross_fixed_assets_$_watww'},
  { 'from_name': 'Water Network  Renewal',	'to_name': 'wat_network_renew'},
  { 'from_name': 'Network  Renewal per population',	'to_name': 'wat_network_renew_km_pop'},
  { 'from_name': 'Annual investments over total assets ',	'to_name': 'annual_invest_assets'},
  { 'from_name': 'Annual water bill for a household consuming 6m3 of water per month through a household or shared yard tap (but excluding the use of standposts)?',	'to_name': 'annual_hh_bill'},
  { 'from_name': 'Residential fixed component of tariff',	'to_name': 'res_tariff_fixed_conn_yr'},
  { 'from_name': 'Residential fixed component of tariff',	'to_name': 'res_tariff_fixed_prop'},
  { 'from_name': 'Residential fixed component of tariff - water',	'to_name': 'res_tariff_fixed_conn_yr_wat'},
  { 'from_name': 'Residential fixed component of tariff - wastewater',	'to_name': 'res_tariff_fixed_conn_yr_ww'},
  { 'from_name': 'Residential fixed component of tariff - water',	'to_name': 'res_tariff_fixed_prop_wat'},
  { 'from_name': 'Residential fixed component of tariff - wastewater',	'to_name': 'res_tariff_fixed_prop_ww'},
  { 'from_name': 'Ratio of industrial to residential tariff',	'to_name': 'tariff_res_ind_prop'},
  { 'from_name': 'Ratio of industrial to residential tariff - water',	'to_name': 'tariff_res_ind_prop_wat'},
  { 'from_name': 'Ratio of industrial to residential tariff - wastewater',	'to_name': 'tariff_res_ind_prop_ww'},
  { 'from_name': 'Connection Charge - water',	'to_name': 'conn_charge_wat'},
  { 'from_name': 'Connection Charge - water',	'to_name': 'conn_charge_wat_GNI'},
  { 'from_name': 'Connection Charge -  sewerage',	'to_name': 'conn_charge_ww'},
  { 'from_name': 'Connection Charge -  sewerage',	'to_name': 'conn_charge_ww_GNI'},
  { 'from_name': 'Average Revenue W&WW',	'to_name': 'rev_watww_m3'},
  { 'from_name': 'Average Revenue W&WW',	'to_name': 'rev_watww_conn'},
  { 'from_name': 'Average Revenue – water only',	'to_name': 'rev_wat_m3'},
  { 'from_name': 'Revenue Split - % water',	'to_name': 'rev_wat_prop'},
  { 'from_name': 'Revenue Split - % wastewater',	'to_name': 'rev_ww_prop'},
  { 'from_name': 'Water revenue – residential',	'to_name': 'rev_res_prop'},
  { 'from_name': 'Water revenue – industrial/commercial',	'to_name': 'rev_indcom_prop'},
  { 'from_name': 'Water revenue – institutions & others',	'to_name': 'rev_inst_prop'},
  { 'from_name': 'Water revenue – bulk treated supply',	'to_name': 'rev_bulk_prop'},
  { 'from_name': 'Wastewater revenue per person served',	'to_name': 'rev_ww_person'},
  { 'from_name': 'Total revenues per service pop/GNI',	'to_name': 'rev_GNI_person'},
  { 'from_name': 'Collection Period',	'to_name': 'collection_period'},
  { 'from_name': 'Collection ratio',	'to_name': 'collection_ratio'},
  { 'from_name': 'Cash Flow in US$ per M3',	'to_name': 'cash_flow_m3'},
  { 'from_name': 'Operating Cost Coverage',	'to_name': 'opex_coverage'},
  { 'from_name': 'Debt Service Ratio',	'to_name': 'debt_service'},
  { 'from_name': 'Metering level',	'to_name': 'meter_level'},
  { 'from_name': 'Water sold that is metered %',	'to_name': 'wat_meter'},
  { 'from_name': 'Pipe Breaks',	'to_name': 'pipe_breaks'},
  { 'from_name': 'Sewer System Blockages',	'to_name': 'sew_block_km_yr'},
  { 'from_name': 'Sewerage blockage',	'to_name': 'sew_block_conn'},
  { 'from_name': 'Capacity Utilization: Amount of m3 produced over the maximum possible',	'to_name': 'capacity_utilization_wat'},
  { 'from_name': 'Electricity Consumption per m3 sold',	'to_name': 'elec_consump_sold_wat'},
  { 'from_name': 'Electricity Consumption per m3 of wastewater',	'to_name': 'elec_consump_ww'},
  { 'from_name': 'Percentage of operational costs that are maintenance',	'to_name': 'opex_maint_prop'},
  { 'from_name': 'Average cost of each repair',	'to_name': 'avg_repair_cost'},
  { 'from_name': 'Average depreciation ratio of assets',	'to_name': 'avg_deprec_assets'},
  { 'from_name': 'Average depreciation ratio of water assets',	'to_name': 'avg_deprec_assets_wat'},
  { 'from_name': 'Average depreciation ratio of wastewater assets',	'to_name': 'avg_deprec_assets_ww'},
  { 'from_name': 'Percentage of government transfers over total operating revenues',	'to_name': 'govt_transfer_rev_prop'},
  { 'from_name': 'Percentage of female staff',	'to_name': 'female_staff'},
  { 'from_name': 'Average women salary',	'to_name': 'female_salary'},
  { 'from_name': 'Capacity Utilization: Treated wastewater over maximum amount of treated wastewater possible',	'to_name': 'capacity_utilization_ww'},
  { 'from_name': 'Percentage of woman engineers',	'to_name': 'female_eng'},
  { 'from_name': 'Non Revenue Water',	'to_name': 'NRW'},
  { 'from_name': 'Non Revenue Water',	'to_name': 'NRW_m3_km'},
  { 'from_name': 'Non Revenue Water',	'to_name': 'NRW_m3_conn'},
  { 'from_name': 'Staff Water /000 Water connections',	'to_name': 'staff_conn_wat'},
  { 'from_name': 'Staff W&WW/000 water and wastewater connections',	'to_name': 'staff_conn_watww'},
  { 'from_name': 'Staff Water/000 Water pop served',	'to_name': 'staff_pop_wat'},
  { 'from_name': 'Staff W&WW/000 W&WW pop served',	'to_name': 'staff_pop_watww'},
  { 'from_name': 'Staff wastewater/000 wastewater connections',	'to_name': 'staff_conn_ww'},
  { 'from_name': 'Staff Wastewater/000 Wastewater pop served',	'to_name': 'staff_pop_ww'},
  { 'from_name': 'Staff % Water',	'to_name': 'staff_prop_wat'},
  { 'from_name': 'Staff % Wastewater',	'to_name': 'staff_prop_ww'},
  { 'from_name': 'Unit Operational Cost Water and Wastewater (W&WW)',	'to_name': 'unit_opex_sold_watww'},
  { 'from_name': 'Unit Operational Cost Water and Wastewater',	'to_name': 'unit_opex_prod_watww'},
  { 'from_name': 'Unit Operational Cost – Water only',	'to_name': 'unit_opex_sold_wat'},
  { 'from_name': 'Operational Cost Split - % Water',	'to_name': 'unit_opex_prop_wat'},
  { 'from_name': 'Operational Cost Split - % Wastewater',	'to_name': 'unit_opex_prop_ww'},
  { 'from_name': 'Unit Operational Cost – Wastewater',	'to_name': 'unit_opex_pop_ww'},
  { 'from_name': 'Labor Costs vs Operational Costs',	'to_name': 'cost_lab_opex_prop'},
  { 'from_name': 'Electrical Energy Costs as percentage of Operational Costs',	'to_name': 'cost_elec_opex_prop'},
  { 'from_name': 'Contracted-out service costs as percentage of operational costs',	'to_name': 'cost_contract_opex_prop'},
  { 'from_name': 'Revenue per staff',	'to_name': 'rev_staff'},
  { 'from_name': 'Average Anual Salary',	'to_name': 'avg_salary'},
  { 'from_name': 'Energy Efficiency for Water Production',	'to_name': 'elec_consump_prod'},
  { 'from_name': 'Energy Efficiency for Wastewater',	'to_name': 'elec_consump_ww_2'},
  { 'from_name': 'Energy Efficiency other Services ',	'to_name': 'elec_consump_other'},
  { 'from_name': 'Chemical Costs as percentage of Operational Costs',	'to_name': 'cost_chem_opex_prop'},
  { 'from_name': 'Other Costs as percentage of Operational Costs',	'to_name': 'cost_other_opex_prop'},
  { 'from_name': 'Wastewater – at least primary treatment',	'to_name': 'ww_treat_atleast_primary'},
  { 'from_name': 'Wastewater primary treatment only',	'to_name': 'ww_treat_primary_only'},
  { 'from_name': 'Wastewater secondary treatment or better',	'to_name': 'ww_treat_secondary'},
  { 'from_name': 'Continuity of Service',	'to_name': 'continuity'},
  { 'from_name': 'Customers with discontinuous supply',	'to_name': 'cust_discontinuous'},
  { 'from_name': 'Quality of water supplied: nr of tests for residual chlorine',	'to_name': 'chlorine_test'},
  { 'from_name': 'Quality of water supplied: samples passing on residual chlorine',	'to_name': 'chlorine_pass'},
  { 'from_name': 'Complaints about W&WW services',	'to_name': 'complaints'},
  { 'from_name': 'Wastewater – at least primary treatment',	'to_name': 'ww_treat_atleast_primary_2'},
  { 'from_name': 'Water Coverage',	'to_name': 'coverage_wat'},
  { 'from_name': 'Water Coverage – Household Connections',	'to_name': 'coverage_hh_wat'},
  { 'from_name': 'Water Coverage – Public Water Points',	'to_name': 'coverage_wpt_wat'},
  { 'from_name': 'Sewerage Coverage',	'to_name': 'coverage_sew'},
  { 'from_name': 'Network Density',	'to_name': 'network_density'},
  { 'from_name': 'Water Production',	'to_name': 'prod_wat_lpcd'},
  { 'from_name': 'Water Production',	'to_name': 'prod_wat_m3_conn_month'},
  { 'from_name': 'Total Water Consumption',	'to_name': 'consump_wat_lpcd'},
  { 'from_name': 'Total Water Consumption',	'to_name': 'consump_wat_m3_conn_month'},
  { 'from_name': 'Water consumption split by Residential Consumption',	'to_name': 'consump_wat_res_prop'},
  { 'from_name': 'Water consumption split by Industrial / commercial Consumption',	'to_name': 'consump_wat_indcom_prop'},
  { 'from_name': 'Water consumption split by Consumption by Institutions & others',	'to_name': 'consump_wat_inst_prop'},
  { 'from_name': 'Water consumption split by Bulk treated supply',	'to_name': 'consump_wat_bulk_prop'},
  { 'from_name': 'Residential Consumption',	'to_name': 'consump_wat_res_lpcd'},
  { 'from_name': 'Residential Consumption – connections to mains supply',	'to_name': 'consump_wat_main_res_lpcd'},
  { 'from_name': 'Residential consumption - public water points',	'to_name': 'consump_wat_wpt_lpcd'},
  { 'from_name': 'Residential Consumption per Connection',	'to_name': 'consump_wat_res_conn'},
]

def run(excel_file_name):
  for sheet_name in get_sheets_in_excel_document(excel_file_name):
    print("SHEET: " + sheet_name)

    if (path.isfile(get_output_file_for_sheet(sheet_name))):
      print("Sheet " + sheet_name + " already exists. Skipping. (" + get_output_file_for_sheet(sheet_name) + ")")
      continue

    try:
      sheet_df = create_1d_ibnet_dataframe(excel_file_name, sheet_name)
      sheet_df.to_csv(get_output_file_for_sheet(sheet_name))
    except Exception as err:
      print("ERROR aggregating data for sheet: " + sheet_name)
      print(err)   

def get_sheets_in_excel_document(excel_file_name):
  print("Loading excel file at " + excel_file_name + " (" + str(path.getsize(excel_file_name)/1024/1024) + " MB)")
  excel_file = pd.read_excel(excel_file_name, None)
  return excel_file.keys()

def split_dataframe_by_blank_rows(excel_file_name, sheet_name):
  sheet_df = pd.read_excel(EXCEL_FILE_NAME, sheet_name)
  last_index = 0
  for next_index in sheet_df[sheet_df.isnull().all(1)].index:
    yield pd.read_excel(excel_file_name, sheet_name, skiprows = last_index, nrows = next_index - last_index)
    last_index = next_index + 2

def create_1d_ibnet_dataframe(excel_file_name, sheet_name):
  sheet_df = pd.DataFrame(
    index=pd.MultiIndex(
      names=['utility', 'year'], 
      levels=[[],[]], 
      codes=[[],[]]
    )
  )

  i = 0
  missing_variables = []
  for variable_table_2d in split_dataframe_by_blank_rows(excel_file_name, sheet_name):
    variable_name = variable_table_2d.columns[0]

    while (variable_name != SEQUENTIAL_VARIABLE_RENAMES[i]['from_name']):
      expected_variable_name = SEQUENTIAL_VARIABLE_RENAMES[i]['from_name']
      missing_variables.append(SEQUENTIAL_VARIABLE_RENAMES[i]['to_name'])
      print("  MISSING EXPECTED VARIABLE: " + expected_variable_name)
      if (i + 1 == len(SEQUENTIAL_VARIABLE_RENAMES)):
        print(variable_table_2d)
        raise Exception('Encountered an unexpected variable name. (index=' + str(i) + ', variable_name=' + variable_name + ', expected_variable_name=' + expected_variable_name + ')')
      i = i + 1

    to_variable_name = SEQUENTIAL_VARIABLE_RENAMES[i]['to_name']
    # print("  VARIABLE: " + variable_name + " -> " + to_variable_name)
    variable_table_1d = pd.DataFrame(variable_table_2d.set_index(variable_name).stack()).rename(columns={0: to_variable_name})
    variable_table_1d.index.rename(
      ['utility', 'year'], 
      inplace=True
    )
    sheet_df = sheet_df.merge(
      variable_table_1d, 
      how='outer', 
      left_index=True, 
      right_index=True, 
      copy=True
    )
    i = i + 1

  if (len(missing_variables)):
    print("SHEET " + sheet_name + " is missing expected variables: [ " + ', '.join(missing_variables) + " ]")
  else:
    print("SHEET " + sheet_name + " complete")

  return sheet_df

run(EXCEL_FILE_NAME)
