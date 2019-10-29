# from utils.web_utils import is_aliexpress, is_amazon
from utils.amazon.tools import AmazonTools


emoji = {
    # Positive
    'check': '&#9989;',
    'blue_diamond': '&#128313;',
    'bangbang': '&#8252;',
    '': '',
    '': '',
    # Neutral
    'sand_clock': '&#x23F3;',
    'right_arrow': '&#10145;',
    'microphone': '&#127897;',
    'trolley': '&#x1F6D2;',
    # Negative
    '': '',
    'red_circle': '&#11093;',
    'red_cross': '&#10060;',
    'fear': '&#128561;',
    'globe': '&#127760;',
    # Special
    'empty_character': '&#8205;'

}


def user_template(product, template=None, coupon=None):
    """
        Coupon is a dictionary with the following structure:
            cupon = {
                    'code': args[0],
                    'final_price': args[1],
                    'link': args[2]
                    }
    """

    if template is None:
        template = 'standard'

    title = product.short_description
    description = product.description
    features = product.features
    price = product.price
    size = product.size
    old_price = product.standard_price
    img_url = product.image_url
    url = product.url
    end_date = product.end_date

    def get_coupon_line(coupon):
        if coupon is not None:
            coupon_price = coupon['final_price']
            code = coupon['code']
            # <b>(Pulsa sobre &#128070; el cupón para copiarlo)</b>
            default_coupon_line = f'\n<b>PRECIO CON CUPÓN: {coupon_price} {emoji["check"]}</b>\n#CUPÓN: {code}\n\n'
            return default_coupon_line
        else:
            return ''

    def get_shop_name(url):
        if AmazonTools.is_amazon(url):
            return 'Amazon'
        else:
            return ''

    def get_description_line(description, features, coupon):
        if coupon is None:
            if description:
                # Takes the first line of the description
                description_line = description.splitlines()[0]
                # If it's long we append '...' at the end, we remove the last word for avoid truncated words as well
                if len(description_line) > 300:
                    description_line = ' '.join(description_line[0:300].split()[:-1]) + '...'
            elif features:
                description_line = features
                if len(description_line) > 300:
                    description_line = '\n'.join(description_line[0:300].splitlines()[:-1])
            else:
                description_line = ''

        else:
            description_line = 'Recuerda aplicar el cupón de descuento'

        return description_line

    if title and price and img_url:
        try:

            image_url_line = {
                'default': f'<a href="{img_url}">{emoji["empty_character"]}</a>',
            }
            title_line = {
                'default': f'<b> {title}</b>\n\n',
                'TheCifu': f'<b>{emoji["blue_diamond"]} {title} {emoji["blue_diamond"]}</b> \n\n',
                'Katka95': f'<b>{emoji["blue_diamond"]} {title} {emoji["blue_diamond"]}</b> \n\n',
            }

            description_line = {
                'default': '',
                'TheCifu':  f'{emoji["microphone"]} CHOLLAZO: {get_description_line(description, features, coupon)} {emoji["bangbang"]}\n\n',
                'Katka95':  f'{emoji["microphone"]} {get_description_line(description, features, coupon)} {emoji["bangbang"]}\n\n',
            }

            size_line = {
                'default': f'<b> Talla {size} </b>\n\n' if size else '',
                'TheCifu': f'<b> CHOLLAZO, en diferentes tallas !! </b>\n\n' if size else '',
                'Vincent_Vegaa': '',
            }

            temporal_line = {
                'default': f'<b> {emoji["sand_clock"]} Oferta Temporal!! {end_date}</b>\n\n' if product.end_date else '',
            }

            old_price_line = {
                'default': f'<b>{emoji["red_cross"]} {old_price}</b>\n' if old_price else '',
                'gavaste': '',
                'TheCifu': f'{emoji["check"] if coupon is None else ""} <b>Precio{" Oferta" if old_price else ""}: {price}</b> {emoji["fear"] if coupon is None else emoji["red_circle"]}\n',

            }

            price_line = {
                'default': f'<b>{emoji["check"]}{price}</b>\n',
                'Vincent_Vegaa': f'<b>{price} {emoji["check"]} </b>\n',
                'TheCifu': f'{emoji["red_circle"]} Sin oferta: {old_price}\n' if old_price else '',
            }

            coupon_line = {
                'default': get_coupon_line(coupon)
            }

            shop_line = {
                'default': '',
                'TheCifu': f'{emoji["trolley"]} Tienda: <a href="{url}">#{get_shop_name(url)} </a>\n\n',
            }


            link_line = {
                'default': f'{emoji["trolley"]}<b>Comprar </b>\n{emoji["right_arrow"]}<a href="{url}">Ver en {get_shop_name(url)} </a>\n',
                #'gavaste': f'<b>Comprar </b>\n{emoji["right_arrow"]} {url}\n',
                'TheCifu': f'\n{emoji["globe"]}<a href="{url}">Ver en {get_shop_name(url)} </a>\n',
                'Vincent_Vegaa': f'<b>&#x1F6D2;Comprar </b><a href="{url}">aquí</a>\n\n',

            }
            watched_in_line = {
                'default': f'',
                #'Vincent_Vegaa': f'<b>&#128064;Visto en: </b><a href="https://t.me/AmznSports">AmznSports</a>\n\n',
                'Katka95': f'<b>&#128064;Visto en: </b><a href="https://t.me/TusChollosBelleza">TusChollosBelleza</a>\n\n',

            }

            def get_msg_property(property):
                return property.get(template, property['default'])

            msg = get_msg_property(image_url_line)
            msg += get_msg_property(title_line)
            msg += get_msg_property(description_line)
            msg += get_msg_property(size_line)
            msg += get_msg_property(temporal_line)
            msg += get_msg_property(old_price_line)
            msg += get_msg_property(price_line)
            msg += get_msg_property(coupon_line)
            msg += get_msg_property(shop_line)
            msg += get_msg_property(link_line)
            msg += get_msg_property(watched_in_line)

        except Exception as e:
            msg = f'Error creando el mensaje, Exception: {e}'






        #msg = image_url_line.get(template, coupon_line['default'])
        #msg += title_line.get(template, coupon_line['default'])
        #msg += size_line.get(template, coupon_line['default'])
        #msg += temporal_line.get(template, coupon_line['default'])
        #msg += old_price_line.get(template, coupon_line['default'])
        #msg += price_line.get(template, coupon_line['default'])
        #if coupon:
        #    msg += coupon_line.get(template, coupon_line['default'])
        #msg += link_line.get(template, coupon_line['default'])
        #msg += watched_in_line.get(template, coupon_line['default'])

        success = True

    else:
        success = False
        failed = []
        if title is None: failed.append('title')
        if price is None: failed.append('price')
        if img_url is None: failed.append('img_url')

        msg = f'Error al leer el producto {", &#10060; ".join(failed)}\n\n'
        msg += f'{emoji["check"]} El link convertido es:\n{url}'

    return msg, success

