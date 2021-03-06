# from utils.web_utils import is_aliexpress, is_amazon
from utils.amazon.tools import AmazonTools
from utils.singleton import Singleton


class LineFormater(metaclass=Singleton):

    emoji = {
        # Positive
        'check': '&#9989;',
        'blue_diamond': '&#128313;',
        'bangbang': '&#8252;',
        'fire': '&#128293;',
        'shield': '&#128304;',
        # Neutral
        'sand_clock': '&#x23F3;',
        'right_arrow': '&#10145;',
        'microphone': '&#127897;',
        'trolley': '&#x1F6D2;',
        'man-genie': '&#129502;',
        'headphones': '&#127911;',
        'moneybag': '&#128176;',

        # Negative
        '': '',
        'red_circle': '&#11093;',
        'red_cross': '&#10060;',
        'no-entry': '&#9940;',
        'forbidden': '&#128683;',
        'fear': '&#128561;',
        'globe': '&#127760;',
        # Special
        'empty_character': '&#8205;'

    }

    @classmethod
    def get_image_url_line(cls, img_url):
        return f'<a href="{img_url}">{cls.emoji["empty_character"]}</a>'

    @classmethod
    def get_title_line(cls, title, style='default'):
        title_lines = {
            'default': f'<b> {title}</b>\n\n',
            'adc100': f'<b>{cls.emoji["fire"]} NUEVO CHOLLO #AMAZON \n\n{cls.emoji["fire"]}{title}</b>\n\n',
            'TheCifu': f'<b>{cls.emoji["blue_diamond"]} {title} {cls.emoji["blue_diamond"]}</b> \n\n',
            'Katka95': f'<b>{cls.emoji["blue_diamond"]} {title} {cls.emoji["blue_diamond"]}</b> \n\n',
        }
        return title_lines.get(style, title_lines['default'])

    @classmethod
    def __get_description_line_text(cls, description, features, coupon):
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

    @classmethod
    def get_description_line(cls, description, features=None, coupon=None, style='default'):
        description_line = {
            'default': '',
            'TheCifu': f'{cls.emoji["microphone"]} CHOLLAZO: {cls.__get_description_line_text(description, features, coupon)} {cls.emoji["bangbang"]}\n\n',
            'Katka95': f'{cls.emoji["microphone"]} {cls.__get_description_line_text(description, features, coupon)} {cls.emoji["bangbang"]}\n\n',
        }

        line = description_line
        return line.get(style, line['default'])

    @classmethod
    def get_size_line(cls, size, style='default'):
        size_line = {
            'default': f'<b> Talla {size} </b>\n\n' if size else '',
            'TheCifu': f'<b> CHOLLAZO, en diferentes tallas !! </b>\n\n' if size else '',
            # 'Vincent_Vegaa': '',
        }
        line = size_line
        return line.get(style, line['default'])

    @classmethod
    def get_temporal_line(cls, end_date, style='default'):
        temporal_line = {
            'default': f'<b> {cls.emoji["sand_clock"]} Oferta Temporal!! {end_date}</b>\n\n' if end_date else '',
            'Vincent_Vegaa': f'<b> {cls.emoji["sand_clock"]} Oferta Flash {end_date}</b>\n\n' if end_date else '',
            'Malu320': f'<b> {cls.emoji["sand_clock"]} Oferta Flash {end_date}</b>\n\n' if end_date else '',
        }

        line = temporal_line
        return line.get(style, line['default'])

    @classmethod
    def get_old_price_line(cls, old_price, style='default'):

        old_price_line = {
                'default': f'<b>{cls.emoji["red_cross"]} {old_price}</b>\n' if old_price else '',
                'gavaste': '',
                'Vincent_Vegaa': f'<b>{cls.emoji["no-entry"]} PVP: {old_price}</b>\n' if old_price else '',
                'Malu320': f'<b>{cls.emoji["no-entry"]} PVP: {old_price}</b>\n' if old_price else '',
                'acd100': f'<b>\t{cls.emoji["forbidden"]} PVP: {old_price}</b>\n' if old_price else '',
            }
        line = old_price_line
        return line.get(style, line['default'])

    @classmethod
    def get_price_line(cls, price, style='default'):
        price_line = {
            'default': f'<b>{cls.emoji["check"]}{price}</b>\n',
            'Vincent_Vegaa': f'<b>{cls.emoji["check"]} PRECIO OFERTA: {price} </b>\n',
            'Malu320': f'<b>{cls.emoji["check"]} PRECIO OFERTA: {price} </b>\n',
            'acd100': f'<b>\t{cls.emoji["fire"]} OFERTA ACTUAL: {price} {cls.emoji["fire"]}</b>\n',
        }
        line = price_line
        return line.get(style, line['default'])

    @classmethod
    def get_coupon_line(cls, coupon, style='default'):
        if coupon is not None:
            coupon_price = coupon['final_price']
            code = coupon['code']
            # <b>(Pulsa sobre &#128070; el cupón para copiarlo)</b>
            coupon_line = {
                'default': f'\n<b>PRECIO CON CUPÓN: {coupon_price} {cls.emoji["check"]}</b>\n#CUPÓN: {code}\n\n'
            }
            line = coupon_line
            return line.get(style, line['default'])
        else:
            return ''

    @classmethod
    def get_shop_line(cls, url, style='default'):
        shop_line = {
            'default': '',
            'TheCifu': f'{cls.emoji["trolley"]} Tienda: <a href="{url}">#{cls.__get_shop_name(url)} </a>\n\n',
        }

        line = shop_line
        return line.get(style, line['default'])

    @classmethod
    def __get_shop_name(cls, url):
        if AmazonTools.is_amazon(url):
            return 'Amazon'
        else:
            return ''

    @classmethod
    def get_link_line(cls, url, style='default'):
        link_line = {
            'default': f'{cls.emoji["trolley"]}<b>Comprar </b>\n\\'
                       f'{cls.emoji["right_arrow"]}<a href="{url}">Ver en {cls.__get_shop_name(url)} </a>\n',

            'TheCifu': f'\n{cls.emoji["globe"]}<a href="{url}">Ver en {cls.__get_shop_name(url)} </a>\n',
            'Vincent_Vegaa': f'<b>{cls.emoji["trolley"]} Compra: </b><a href="{url}">Aquí</a>\n\n',
            'Malu320': f'<b>{cls.emoji["trolley"]} Compra: </b><a href="{url}">Aquí</a>\n\n',
            'acd100': f'<b>{cls.emoji["shield"]} COMPRAR: </b><a href="{url}">Aquí</a>\n\n',
        }

        line = link_line
        return line.get(style, line['default'])

    @classmethod
    def watched_in(cls, style='default'):
        watched_in_line = {
            'default': f'',
            'Katka95': f'<b>&#128064;Visto en: </b><a href="https://t.me/TusChollosBelleza">TusChollosBelleza</a>\n\n',

            'Vincent_Vegaa': f'{cls.emoji["man-genie"]} <a href="https://www.amazon.es/gp/aw/gb/?ie=UTF8&ref_=navm_hdr_deals&tag=koko01a-21">Chollos del día</a>\n'
                       f'{cls.emoji["headphones"]} <a href="https://www.amazon.es/music/unlimited?_encoding=UTF8&ref=as_li_ss_tl&tag=koko01a-21">Amazon Music Unlimited</a>\n'
                       f'{cls.emoji["moneybag"]} <a href="http://www.amazon.es/prime?tag=koko01a-21">Amazon Prime GRATIS</a>\n',

            'Malu320': f'{cls.emoji["man-genie"]} <a href="https://www.amazon.es/gp/aw/gb/?ie=UTF8&ref_=navm_hdr_deals&tag=trono06-21">Chollos del día</a>\n'
                       f'{cls.emoji["headphones"]} <a href="https://www.amazon.es/music/unlimited?_encoding=UTF8&ref=as_li_ss_tl&tag=trono06-21">Amazon Music Unlimited</a>\n'
                       f'{cls.emoji["moneybag"]} <a href="http://www.amazon.es/prime?tag=trono06-21">Amazon Prime GRATIS</a>\n',

            'RNogales': f'{cls.emoji["man-genie"]} <a href="https://www.amazon.es/gp/aw/gb/?ie=UTF8&ref_=navm_hdr_deals&tag=trono06-21">Chollos del día</a>\n'
                       f'{cls.emoji["headphones"]} <a href="https://www.amazon.es/music/unlimited?_encoding=UTF8&ref=as_li_ss_tl&tag=trono06-21">Amazon Music Unlimited</a>\n'
                       f'{cls.emoji["moneybag"]} <a href="http://www.amazon.es/prime?tag=trono06-21">Amazon Prime GRATIS</a>\n',

            'acd100': f'<a href="https://goo.gl/mJ2HiL">Comparte en Whatsapp</a>\n\n',

        }
        line = watched_in_line
        return line.get(style, line['default'])





