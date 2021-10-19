import get


fields = {
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


def translate(x):
    return fields[x]
