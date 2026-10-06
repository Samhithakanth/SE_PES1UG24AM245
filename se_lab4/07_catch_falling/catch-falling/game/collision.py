"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    # Check horizontal overlap.
    horizontal_overlap = (
        basket_rect.left <= obj.x <= basket_rect.right
    )

    # Check vertical overlap between the falling object and basket.
    object_bottom = obj.y + obj.radius
    object_top = obj.y - obj.radius

    vertical_overlap = (
        object_bottom >= basket_rect.top
        and object_top <= basket_rect.bottom
    )

    return horizontal_overlap and vertical_overlap