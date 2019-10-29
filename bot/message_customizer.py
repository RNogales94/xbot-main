from bot.line_formater import LineFormater
from bot.message import Message


class MessageCustomizer:

    @classmethod
    def __has_at_least_minimal_information(cls, product):
        has_title = product.title is not None and len(product.title) > 0
        has_price = product.price is not None
        has_img_url = product.image_url is not None
        return has_img_url and has_price and has_title


    @classmethod
    def build_message(cls, product, user=None, coupon=None):
        """
            Coupon is a dictionary with the following structure:
                cupon = {
                        'code': args[0],
                        'final_price': args[1],
                        'link': args[2]
                        }
        """

        title = product.title
        description = product.description
        features = product.features
        price = product.price
        size = product.size
        old_price = product.standard_price
        img_url = product.image_url
        url = product.url
        end_date = product.end_date

        if cls.__has_at_least_minimal_information(product):

            msg = Message(
                            image_url_line=LineFormater.get_image_url_line(img_url),
                            title_line=LineFormater.get_title_line(title=title),
                            description_line=LineFormater.get_description_line(description, features, coupon),
                            size_line=LineFormater.get_size_line(size),
                            temporal_line=LineFormater.get_temporal_line(end_date),
                            old_price_line=LineFormater.get_old_price_line(old_price),
                            price_line=LineFormater.get_price_line(price),
                            coupon_line=LineFormater.get_coupon_line(coupon),
                            shop_line=LineFormater.get_shop_line(url),
                            link_line=LineFormater.get_link_line(url),
                            watched_in_line=LineFormater.watched_in()
                        ),

            return msg

