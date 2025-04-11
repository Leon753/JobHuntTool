from services.builders.sheets.base.sheet_format_base import SheetFormatterBase

class GoogleSheetFormatter(SheetFormatterBase):
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.requests = []

    def clear_format(self) -> "GoogleSheetFormatter":
        self.requests.append(
            {
                "updateCells": {
                    "range": {
                        "sheetId": self.sheet_id,
                    },
                    "fields": "userEnteredFormat",
                }
            }
        )
        return self

    def auto_resize(self, start_index, end_index) -> "GoogleSheetFormatter":

        self.requests.append(
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": self.sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": start_index,
                        "endIndex": end_index,
                    }
                }
            }
        )
        return self

    def set_header_format(
        self, 
        start_col, 
        end_col, 
        background_color, 
        font_size=12, 
        bold=True
    ) -> "GoogleSheetFormatter":

        self.requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": start_col,
                        "endColumnIndex": end_col,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": background_color,
                            "textFormat": {"bold": bold, "fontSize": font_size},
                            "horizontalAlignment": "CENTER",
                            # "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,wrapStrategy)",
                }
            }
        )
        return self

    def update_borders(
        self, 
        start_row, 
        end_row, 
        start_col, 
        end_col, 
        border_color
    ) -> "GoogleSheetFormatter":

        self.requests.append(
            {
                "updateBorders": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": start_col,
                        "endColumnIndex": end_col,
                    },
                    "top": {"style": "SOLID", "width": 1, "color": border_color},
                    "bottom": {"style": "SOLID", "width": 1, "color": border_color},
                    "left": {"style": "SOLID", "width": 1, "color": border_color},
                    "right": {"style": "SOLID", "width": 1, "color": border_color},
                    "innerHorizontal": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0.5, "green": 0.5, "blue": 0.5},
                    },
                    "innerVertical": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0.5, "green": 0.5, "blue": 0.5},
                    },
                }
            }
        )
        return self

    def freeze_row(self, frozen_row_count) -> "GoogleSheetFormatter":
        self.requests.append(
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": self.sheet_id,
                        "gridProperties": {"frozenRowCount": frozen_row_count},
                    },
                    "fields": "gridProperties.frozenRowCount",
                }
            }
        )
        return self

    def set_cell_background(
        self,
        start_row,
        end_row,
        start_col,
        end_col,
        background_color: dict = None,
        background_color_style: dict = None,
        theme_color: str = None,
    ) -> "GoogleSheetFormatter":
        """
        Sets the background color for the specified range.

        :param background_color: A dict with keys "red", "green", "blue", and optionally "alpha".
        :param background_color_style: A dict representing the backgroundColorStyle with an "rgbColor" key.
        :param theme_color: A string representing a theme color.
        """
        cell_format = {}

        if background_color:
            cell_format["backgroundColor"] = background_color
        if background_color_style:
            cell_format["backgroundColorStyle"] = background_color_style
        if theme_color:
            cell_format["themeColor"] = theme_color

        self.requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": start_col,
                        "endColumnIndex": end_col,
                    },
                    "cell": {"userEnteredFormat": cell_format},
                    "fields": "userEnteredFormat(backgroundColor,backgroundColorStyle,themeColor)",
                }
            }
        )
        return self

    def add_conditional_format_rule(
        self,
        condition_value: str,
        background_color: dict,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        condition_type: str = "TEXT_EQ",
        index: int = 0,
    ) -> "GoogleSheetFormatter":
        """
        Adds a conditional formatting rule.

        Parameters:
            condition_value (str): The value to compare against (e.g. "interview", "offer", "rejected").
            background_color (dict): The background color to apply (e.g. {"red": 1.0, "green": 0.0, "blue": 0.0}).
            start_row (int): Starting row index (inclusive).
            end_row (int): Ending row index (exclusive).
            start_col (int): Starting column index (inclusive).
            end_col (int): Ending column index (exclusive).
            condition_type (str): The type of condition. Default is "TEXT_EQ".
            index (int): The index in the list where this rule should be inserted.

        Returns:
            SheetFormatter: Self, for chaining.
        """
        rule = {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": self.sheet_id,
                            "startRowIndex": start_row,
                            "endRowIndex": end_row,
                            "startColumnIndex": start_col,
                            "endColumnIndex": end_col,
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": condition_type,
                            "values": [{"userEnteredValue": condition_value}],
                        },
                        "format": {"backgroundColor": background_color},
                    },
                },
                "index": index,
            }
        }
        self.requests.append(rule)
        return self

    def add_banded_rows(
        self,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        first_band_color: dict,
        second_band_color: dict,
        header_color: dict = None,
    ) -> "GoogleSheetFormatter":
        """
        Applies alternating row colors (banding) for the specified range.
        Optionally sets a header color for the first row of the banded range.

        Parameters:
          - start_row, end_row, start_col, end_col: Define the range for the banding.
          - first_band_color: Color for the first band (e.g., white).
          - second_band_color: Color for the second band (e.g., light gray).
          - header_color: (Optional) Color for the header row in the banded range.

        Returns:
          The SheetFormatter instance (for chaining).
        """
        row_properties = {
            "firstBandColor": first_band_color,
            "secondBandColor": second_band_color,
        }
        if header_color:
            row_properties["headerColor"] = header_color

        self.requests.append(
            {
                "addBanding": {
                    "bandedRange": {
                        "bandedRangeId": 42,  # The ID of the banded range.
                        "range": {
                            "sheetId": self.sheet_id,
                            "startRowIndex": start_row,
                            "endRowIndex": end_row,
                            "startColumnIndex": start_col,
                            "endColumnIndex": end_col,
                        },
                        "rowProperties": row_properties,
                    }
                }
            }
        )
        return self

    def deleted_banded_rows(self) -> "GoogleSheetFormatter":
        self.requests.append(
            {
                "deleteBanding": {  # Removes the banded range with the given ID from the spreadsheet. # Removes a banded range
                    "bandedRangeId": 42,  # The ID of the banded range to delete.
                }
            }
        )
        return self

    def wrap_and_allign_text(
        self,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        vertical_alignment: str = "MIDDLE",
        horizontal_alignment: str = "LEFT",
        font_size: int = 10,
    ) -> "GoogleSheetFormatter":
        self.requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": start_col,
                        "endColumnIndex": end_col,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "wrapStrategy": "WRAP",
                            "verticalAlignment": vertical_alignment.upper(),
                            "horizontalAlignment": horizontal_alignment.upper(),  # e.g., "LEFT", "CENTER", "RIGHT"
                            "textFormat": {"fontSize": font_size},
                        }
                    },
                    "fields": "userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment,userEnteredFormat.textFormat.fontSize",
                }
            }
        )
        return self

    def set_column_width(
        self, start_index: int, end_index: int, pixel_size: int = 400
    ) -> "GoogleSheetFormatter":
        self.requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": start_index,
                        "endIndex": end_index,
                    },
                    "properties": {"pixelSize": pixel_size},
                    "fields": "pixelSize",
                }
            }
        )
        return self

    def set_font_size(
        self,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        font_size: int = 10,
    ) -> "GoogleSheetFormatter":
        self.requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": start_col,
                        "endColumnIndex": end_col,
                    },
                    "cell": {
                        "userEnteredFormat": {"textFormat": {"fontSize": font_size}}
                    },
                    "fields": "userEnteredFormat.textFormat.fontSize",
                }
            }
        )
        return self

    def build(self):
        return {"requests": self.requests}
