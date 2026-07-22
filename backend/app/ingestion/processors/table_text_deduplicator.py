from typing import List

from app.models.document import Block
from app.models.table import TableModel
from app.utils.bbox import overlap_ratio

class TableTextDeduplicator:
    """
    Removes text blocks that are completely overlapped by table blocks from a structured document.
    """

# why comma at last - The comma at the end of the parameter list in the `__init__` method is syntactically valid in Python and is often used for a few reasons:
# 1. Readability: It can make it easier to add new parameters in the future without modifying the existing line, which can help with version control diffs and code reviews.
# 2. Consistency: If you have a multi-line parameter list, having a trailing comma can make the formatting more consistent and easier to read. if i remove comma ? - then parameter list will still be valid, but if you later add another parameter, you'll need to remember to add a comma to the previous line. This can lead to syntax errors if forgotten.

    def __init__(self,overlap_threshold:float=0.8,): 
        """
        Constructor for TableTextDeduplicator.
        """
        self.overlap_threshold=overlap_threshold
    
    def process(self,blocks:list[Block],tables:list[TableModel])->list[Block]:
        """
        Process the blocks and tables to remove text blocks that are completely overlapped by table blocks.
        """
        # Edge case: If there are no tables, return the original blocks
        if not tables:
            return blocks

        cleaned_blocks=[]
        for block in blocks:

            # Edge case: If the block has no bounding box, keep it
            if block.bbox is None:
                cleaned_blocks.append(block)
                continue

            # Check if the block is completely overlapped by any table
            is_inside_table=False

            for table in tables:

                # Edge case: If the table has no bounding box, skip it
                if table.bbox is None:
                    continue

                # Calculate the overlap ratio between the block and the table
                overlap=overlap_ratio(block.bbox,table.bbox)

              
                if overlap >= self.overlap_threshold:
                    is_inside_table=True # it means the block is completely overlapped by the table
                    break # it means we found a table that completely overlaps the block, so we can stop checking other tables

            if not is_inside_table:
                cleaned_blocks.append(block) # it means the block is not completely overlapped by any table, so we keep it
        return cleaned_blocks