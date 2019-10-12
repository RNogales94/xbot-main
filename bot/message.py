from bot.user_templates import user_template


class Message:
    def __init__(self, product, username=None, coupon=None):
        # print('Building message...')
        msg = user_template(product, username, coupon)

        self.text = msg[0]
        success = msg[1]
        # print('Message built')
        # print(self.text)
        # if success:
        #     print(f'[OK] Mensaje construido correctamente {product.url}')
        # else:
        #     print(f'[Warning] Mensaje no se ha construido correctamente {product.url} ')

    def __str__(self):
        return self.text


