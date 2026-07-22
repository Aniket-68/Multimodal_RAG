from app.models.common import BoundingBox

def intersection_area(box1:BoundingBox,box2:BoundingBox)->float:
    """
    Calculate the area of intersection between two bounding boxes.

    Parameters
    ----------
    box1 : BoundingBox
        The first bounding box.
    box2 : BoundingBox
        The second bounding box.

    Returns
    -------
    float
        The area of intersection between the two bounding boxes. Returns 0 if there is no intersection.
    """
    x_left = max(box1.x0, box2.x0)
    y_top = max(box1.y0, box2.y0)
 
    x_right = min(box1.x1, box2.x1)
    y_bottom = min(box1.y1, box2.y1)

    if x_right <= x_left or y_bottom <= y_top:
        return 0.0  # No intersection

    return (x_right - x_left) * (y_bottom - y_top)


# this function calculates the area of a bounding box - what is bbox area? it is the area of the rectangle defined by the bounding box coordinates. The area is calculated as the width multiplied by the height of the rectangle. The width is determined by subtracting the x-coordinate of the left edge (x0) from the x-coordinate of the right edge (x1), and the height is determined by subtracting the y-coordinate of the top edge (y0) from the y-coordinate of the bottom edge (y1). If either dimension is negative, it is set to zero to avoid negative area values.
def bbox_area(box:BoundingBox)->float:
    """
    calculate the area of a bounding box.
    """
    width = max(box.x1 - box.x0, 0)
    height = max(box.y1 - box.y0, 0)
    return width * height


def overlap_ratio(source:BoundingBox,target:BoundingBox)->float:
    """
    Calculate the overlap ratio between two bounding boxes.

    Parameters
    ----------
    source : BoundingBox
        The source bounding box (text block).
    target : BoundingBox
        The target bounding box ().

    Returns:
    -------
        0.0 -> no overlap
        1.0 -> source completely inside target
    """
    area=bbox_area(source)

    if area==0:
        return 0.0
    

    intersection = intersection_area(source, target,)
   
    return intersection /area
