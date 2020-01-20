

class Message:
    def __init__(self,
                image_url_line= '',
                title_line = '',
                description_line = '',
                size_line = '',
                temporal_line = '',
                old_price_line = '',
                price_line = '',
                coupon_line = '',
                shop_line = '',
                link_line = '',
                watched_in_line = '',
                ):

        self.image_url_line = image_url_line
        self.title_line = title_line
        self.description_line = description_line
        self.size_line = size_line
        self.temporal_line = temporal_line
        self.old_price_line = old_price_line
        self.price_line = price_line
        self.coupon_line = coupon_line
        self.shop_line = shop_line
        self.link_line = link_line
        self.watched_in_line = watched_in_line

    def __str__(self):
        msg = self.image_url_line
        msg += self.title_line
        msg += self.description_line
        msg += self.size_line
        msg += self.temporal_line
        msg += self.old_price_line
        msg += self.price_line
        msg += self.coupon_line
        msg += self.shop_line
        msg += self.link_line
        msg += self.watched_in_line

        return msg