from services.builders.sheets.base.sheet_data_base import SheetDataInterface

class GoogleSheetDataBuilder(SheetDataInterface):
    def __init__(self):
        self.data = []

    def update_cell(
        self, 
        col: str, 
        row: int, 
        value: list, 
    ) -> "GoogleSheetDataBuilder":
        self.data.append({
            "range": f"{col}{row}",
            "majorDimension": "ROWS",
            "values": [[value]]
        })
        return self

    def update_row(
        self, 
        start_col: str, 
        end_col:str , row: int,
        values: list
    ) -> "GoogleSheetDataBuilder":
        self.data.append({
            "range": f"{start_col}{row}:{end_col}{row}",
            "majorDimension": "ROWS",
            "values": [values]
        })
        return self

    def build(self):
        return {
            "valueInputOption": "USER_ENTERED",
            "data": self.data
        }
