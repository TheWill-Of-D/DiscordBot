import os
import json
import gspread

# If modifying these scopes, update the secret google-json-key.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']



creds_json = json.loads(os.environ['google-json-key'])
gc = gspread.service_account_from_dict(creds_json)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CYLIwfrZLWoN_6E3a4RyI1K2h5qToKzao5OlKgKO1k0/edit?usp=drivesdk')
worksheet = sh.get_worksheet(0)
  
def get_group_gsheet(input):
  try:
    to_find = str(input).lower()
    cell = worksheet.find(to_find)
    if cell.col != 3:
      return [0,0]
    worksheet.update_cell(cell.row, 6, "\U00002705")
    name = worksheet.cell(cell.row, 2).value
    team = worksheet.cell(cell.row, 4).value
    return [team, name]

  except Exception as e:
      print(e)
      return [0,0]


      

  
   
  


