import fitz
from pathlib import Path
from uuid import uuid4
from .base_extractor import BaseExtractor
from app.models.common import BoundingBox
from app.models.table import TableModel
from app.ingestion.context import ParserContext

class TableExtractor(BaseExtractor):
    def extract(self, context: ParserContext) -> list[TableModel]:
        """
        Extracts tables from a PDF page.

        Args:
            context (ParserContext): The context for parsing the document.
        """
        page = context.page # Get the current page from the context
        extracted_tables: list[TableModel] = []  # List to hold the extracted tables

        # Detect tables on the current page
        table_finder = page.find_tables()  # Use PyMuPDF's find_tables method to detect tables on the page

        for table in table_finder.tables:  # Iterate through each detected table

            # Extract the raw data from the table using the extract method of the table object
            raw_data=table.extract()  # Extract the raw data from the table

            if not raw_data:  # If the extracted data is empty, skip this table
                continue

            # Treat first row as header and the rest as data
            header = [self._clean_cell(cell) for cell in raw_data[0]]  # Clean the header cells by removing any unwanted characters or whitespace

            # Remaining rows are treated as data
            rows = [[self._clean_cell(cell) for cell in row] for row in raw_data[1:]]  # Clean the data cells by removing any unwanted characters or whitespace and store them in a list of lists

            bbox = BoundingBox(
                x0=table.rect.x0,
                y0=table.rect.y0,
                x1=table.rect.x1,
                y1=table.rect.y1,
            )
            extracted_tables.append(

                TableModel(
                    table_id=str(uuid4()),  # Generate a unique identifier for the table
                    page_number=context.page_number,  # Page numbers are 0-indexed in PyMuPDF, so we add 1 for human-readable format
                    bbox=bbox,
                    header=header,  # Store the cleaned header row
                    rows=rows,  # Store the cleaned data rows

                    metadata={
                        "num_rows": len(rows),  # Number of data rows in the table
                        "num_columns": len(header),
                    },
                            # Number of columns in the table (based on header)    
                      # Assuming table.cells contains the structured data of the table
                )
            )
            return extracted_tables
    
    @staticmethod
    def _clean_cell(cell: str) -> str:
        """
        Cleans a cell's content by removing unwanted characters or whitespace.

        Args:
            cell (str): The raw cell content.
            """
        return str(cell).strip()  # Remove leading and trailing whitespace from the cell content