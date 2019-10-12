from xbot.models.product import Product


def load_product_from_json(json_obj):
    short_description = json_obj.get('short_description', None)
    description = json_obj.get('description', None)
    features = json_obj.get('features', None)
    standard_price = json_obj.get('standard_price', None)
    price = json_obj.get('price', None)
    url = json_obj.get('url', None)
    image_url = json_obj.get('image_url', None)
    end_date = json_obj.get('end_date', None)
    size = json_obj.get('size', None)

    return Product(short_description=short_description,
                   description=description,
                   features=features,
                   standard_price=standard_price,
                   price=price,
                   url=url,
                   image_url=image_url,
                   end_date=end_date,
                   size=size
                   )
