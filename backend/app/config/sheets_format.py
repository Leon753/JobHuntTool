SHEET_ID = 0 
TABLE_SIZE_ROW = 100
TABLE_SIZE_COLUMN = 9
HEADER_ROW = 1
HEADER_COLUMNS = ["A","B","C","D","E","F","G","H","I"]
HEADER_NAMES = [
    "COMPANY",
    "POSITION",
    "STATUS",
    "JOB_DESCRIPTION",
    "PAY_RANGE",
    "INTERVIEW_PROCESS",
    "EXAMPLE_INTERVIEW_EXPERIENCE",
    "CAREER_GROWTH",
    "EXAMPLE_TECHNICAL_QUESTIONS"
]

sheet_format_json = {
  "requests": [
    {
      "autoResizeDimensions": {
        "dimensions": {
          "sheetId": 0,
          "dimension": "COLUMNS",
          "startIndex": 0,
          "endIndex": 12
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
          "endRowIndex": 1,
          "startColumnIndex": 0,
          "endColumnIndex": 10
        },
        "cell": {
          "userEnteredFormat": {
            "wrapStrategy": "WRAP", 
            "backgroundColor": {
              "red": 0.25,
              "green": 0.41,
              "blue": 0.88 # TODO: FIX COLORS
            },
            # "textFormat": {
            #   "bold": "true",
            #   "fontSize": 12
            # },
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
