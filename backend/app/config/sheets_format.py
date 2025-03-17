SHEET_ID = 0 
TABLE_SIZE_ROW = 100
TABLE_SIZE_COUMN = 7
sheet_format_json = {
  "requests": [
    #TOD0: REMOVE AFFTER DEBUGGING clears all formating 
    {
      "repeatCell": {
        "range": {
          "sheetId": 0,
          "startRowIndex": 0,
          "endRowIndex": 0
        },
        "cell": {
          "userEnteredFormat": {}
        },
        "fields": "userEnteredFormat"
      }
    },
    {
      "autoResizeDimensions": {
        "dimensions": {
          "sheetId": 0,
          "dimension": "COLUMNS",
          "startIndex": 0
        }
      }
    },
    {
      "updateBorders": {
        "range": {
          "sheetId": 0,
          "startRowIndex": 0,
          "startColumnIndex": 0
        },
        "top": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
        "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
        "left": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
        "right": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}},
        "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.5, "green": 0.5, "blue": 0.5}},
        "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.5, "green": 0.5, "blue": 0.5}}
      }
    },
    {
      "repeatCell": {
        "range": {
          "sheetId": 0,
          "startRowIndex": 0, # TODO: ADD IN ROW & COLUMN
          "endRowIndex": 1
        },
        "cell": {
          "userEnteredFormat": {
            "wrapStrategy": "WRAP", 
            "backgroundColor": {
              "red": 0.2,
              "green": 0.2,
              "blue": 0.6 # TODO: FIX COLORS
            },
            "textFormat": {
              "bold": "true",
              "fontSize": 12
            },
            "horizontalAlignment": "CENTER"
          }
        },
        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
      }
    },
    {
      "updateSheetProperties": {
        "properties": {
          "sheetId": 0,
          "gridProperties": {
            "frozenRowCount": 1
          }
        },
        "fields": "gridProperties.frozenRowCount"
      }
    },
    {
      "setBasicFilter": {
        "filter": {
          "range": {
            "sheetId": 0,
            "startRowIndex": 0,
            "startColumnIndex": 3
          }
        }
      }
    },
  ]
}
