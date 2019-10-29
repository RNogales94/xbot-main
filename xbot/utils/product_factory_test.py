import pytest
from xbot.utils.product_factory import ProductFactory


@pytest.fixture
def product_json():
    return {'short_description': 'Versa 20880050 Set mesa y 4 sillas de madera blanca, 75x80x120cm, Juego comedor',
             'description': 'Medidas de: 75 x 80 x 120 cm; peso: 31,8 kg.material: tubo metal + 15mm madera mdf con cubierta de pvc blanco.medidas sillas: 40 x 44 x 82 cm. Altura del asiento: 43,5 cm.',
             'features': 'Medidas de: 75 x 80 x 120 cm; peso: 31,8 kg\nMaterial: tubo metal + 15mm madera mdf con cubierta de pvc blanco.\nMedidas sillas: 40 x 44 x 82 cm. Altura del asiento: 43,5 cm.',
             'standard_price': '320,00\xa0€',
             'end_date': None,
             'price': '75,14\xa0€',
             'url': 'https://www.amazon.es/gp/aw/d/B06XFWF7J4/ref=ox_sc_act_image_1?smid=A1AT7YVPFBWXBL&psc=1',
             'image_url': 'https://images-na.ssl-images-amazon.com/images/I/71uh38DaTsL._SL1500_.jpg',
             'size': None
        }


def test_build(product_json):
    product = ProductFactory.build_product_from_json(product_json)
    assert product.short_description == "Versa 20880050 Set mesa y 4 sillas de madera blanca, 75x80x120cm, Juego comedor"

    product_dict = product.to_dict()
    assert product_dict['shortDescription'] == "Versa 20880050 Set mesa y 4 sillas de madera blanca, 75x80x120cm, Juego comedor"