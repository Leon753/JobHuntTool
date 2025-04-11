from abc import ABC, abstractmethod

class SheetFormatterBase(ABC):
    def __init__(self, sheet_id: int):
        self.sheet_id = sheet_id
        self.requests = []

    def build(self) -> dict:
        return {"requests": self.requests}

    @abstractmethod
    def clear_format(self):
        pass

    @abstractmethod
    def auto_resize(
        self, 
        start_index: int, 
        end_index: int
    ):
        pass

    @abstractmethod
    def set_header_format(
        self, 
        start_col: int, 
        end_col: int, 
        background_color: dict, 
        font_size: int = 12, 
        bold: bool = True
    ):
        pass

    @abstractmethod
    def update_borders(
        self, 
        start_row: int, 
        end_row: int, 
        start_col: int, 
        end_col: int, 
        border_color: dict
    ):
        pass

    @abstractmethod
    def freeze_row(
        self, 
        frozen_row_count: int
    ):
        pass

    @abstractmethod
    def set_cell_background(
        self, 
        start_row: int, 
        end_row: int, 
        start_col: int, 
        end_col: int,
        background_color: dict = None, 
        background_color_style: dict = None, 
        theme_color: str = None
    ):
        pass

    @abstractmethod
    def add_conditional_format_rule(
        self, 
        condition_value: str, 
        background_color: dict, 
        start_row: int, end_row: int, 
        start_col: int, end_col: int, 
        condition_type: str = "TEXT_EQ",
        index: int = 0
    ):
        pass

    @abstractmethod
    def add_banded_rows(
        self, 
        start_row: int, 
        end_row: int, 
        start_col: int, 
        end_col: int, 
        first_band_color: dict, 
        second_band_color: dict, 
        header_color: dict = None
    ):
        pass

    @abstractmethod
    def deleted_banded_rows(self):
        pass

    @abstractmethod
    def wrap_and_allign_text(
        self, 
        start_row: int, 
        end_row: int, 
        start_col: int, 
        end_col: int, 
        vertical_alignment: str = "MIDDLE",
        horizontal_alignment: str = "LEFT", 
        font_size: int = 10
    ):
        pass

    @abstractmethod
    def set_column_width(
        self, 
        start_index: int, 
        end_index: int, 
        pixel_size: int = 400
    ):
        pass

    @abstractmethod
    def set_font_size(
        self, 
        start_row: int, 
        end_row: int, 
        start_col: int, 
        end_col: int, 
        font_size: int = 10
    ):
        pass
