import get
from typing import Callable, Dict, Optional, Union


fields: Dict[str, Callable[str, Optional[Union[dict, str]]]] = {
    'product_isbn': lambda x: x,
    'product_title': get.title,
    'format': get.binding,
    'product_description': get.description,
    'product_retail': get.msrp,
    'publisher': get.publisher,
    'product_weight': get.weight,
    'product_width': get.width,
    'product_height': get.height,
    'product_thickness': get.thickness,
    'Author': get.authors,
    'image': get.image_url
}


def translate(field: str) -> Callable[str, Optional[Union[dict, str]]]:
    """A mapping from field names to their respective getter functions

    Parameters
    ----------
    field : str
        The field to return

    Returns
    -------
    Callable[str, Optional[Union[dict, str]]]
        a function returned from the dictionary lookup in fields
    returned by field corresponding to the method associated
    with looking up that field
    """
    return fields[field]
