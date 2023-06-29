import token

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivymd.uix.toolbar import MDTopAppBar
from pyzbar.pyzbar import ZBarSymbol
from kivymd.uix.snackbar import Snackbar
from kivy_garden.zbarcam import ZBarCam
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton

from request import get_token_from_api_with_qrcode, token_decode, get_all_product, add_to_cart


class MainLayout(BoxLayout):
    pass


class MainApp(MDApp):
    def build(self):
        Window.size = (300, 500)  # Remplacer par la taille souhaitée
        Window.borderless = False
        Window.resizable = False  # Désactive le redimensionnement
        self.cam = None  # ajoutez cette ligne
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.layout = MainLayout()
        self.login_screen = Builder.load_file('views/login.kv')
        self.home_screen = Builder.load_file('views/home.kv')
        self.cart_screen = Builder.load_file('views/cart.kv')
        self.layout.add_widget(self.login_screen)
        self.cart = []
        return self.layout

    def place_order(self):

        popup = Popup(title='Commande passée',
                      content=Label(text='Votre commande a été passée avec succès!'),
                      size_hint=(None, None), size=(250, 250))
        popup.open()
    def add_to_cart(self, product):
        self.cart.append(product)
        add_to_cart("c95a6a66-c9c6-4f79-b30b-dbac376793d8", product.id, 1)

    def show_cart(self):
        self.layout.clear_widgets()
        self.cart_screen = Builder.load_file('views/cart.kv')
        self.update_cart_list()
        self.layout.add_widget(self.cart_screen)

    def update_cart_list(self):
        cart_list = self.cart_screen.ids['cart_list']
        cart_list.clear_widgets()

        for product in self.cart:
            item = TwoLineIconListItem(text=product.name, secondary_text=f"Prix : {product.price}€")
            item.add_widget(IconLeftWidget(icon="shopping"))
            cart_list.add_widget(item)

    def go_back(self, instance):
        self.layout.clear_widgets()
        self.stop_qrcode()
        self.layout.add_widget(self.login_screen)

    def scan_qrcode(self):
        self.layout.clear_widgets()
        self.qr_code_screen = Builder.load_file('views/qrcodecam.kv')
        self.cam = self.qr_code_screen.ids.zbarcam
        self.layout.add_widget(self.qr_code_screen)
        self.back_button = MDFlatButton(text="Retour", on_release=self.go_back)
        self.layout.add_widget(self.back_button)

    def stop_qrcode(self):
        if self.cam:
            self.cam.play = False
            self.cam = None
        self.layout.clear_widgets()
        self.qr_code_screen = None
        self.update_product_list()
        self.layout.add_widget(self.home_screen)

    def go_home(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.home_screen)

    def on_symbols(self, instance, symbols):
        if symbols:
            for symbol in symbols:
                token = get_token_from_api_with_qrcode(symbol.data.decode())
                if (token is not False):
                    self.stop_qrcode()
                else:
                    print("wrong token")

    def update_product_list(self):
        product_list = self.home_screen.ids['product_list']
        product_list.clear_widgets()

        for product in get_all_product():
            item = TwoLineIconListItem(text=product.name, secondary_text=f"Prix : {product.price}€")
            item.add_widget(IconLeftWidget(icon="shopping"))
            product_list.add_widget(item)


            def create_callback(product):
                return lambda x: self.show_product_details(product)


            item.bind(on_release=create_callback(product))

    def show_product_details(self, product):
        detail_screen = ProductDetailScreen(product=product)


        add_to_cart_button = MDFillRoundFlatButton(
            text="Ajouter au panier",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.add_to_cart(product),
            md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
            text_color=MDApp.get_running_app().theme_cls.primary_light
        )

        detail_screen.add_widget(add_to_cart_button)

        self.layout.clear_widgets()
        self.layout.add_widget(detail_screen)


class ProductDetailScreen(BoxLayout):
    def __init__(self, product, quantity=None, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.bind(minimum_height=self.setter('height'))

        product_appbar = MDTopAppBar(title=product.name, pos_hint={'top': 1})
        self.add_widget(product_appbar)
        product_name = MDLabel(text=product.name, font_style='H5', theme_text_color="Secondary")
        product_price = MDLabel(text=f"Prix : {product.price}€", theme_text_color="Secondary")
        product_description = MDLabel(text=product.description, theme_text_color="Secondary")

        # Creation of a card for the product
        product_card = MDCard(orientation='vertical',
                              padding='8dp',
                              size_hint=(None, None),
                              size=("250dp", "350dp"),
                              pos_hint={"center_x": .5})

        product_image = AsyncImage(source=product.photo, size_hint=(1, 1))
        product_card.add_widget(product_image)

        product_card.add_widget(product_name)
        product_card.add_widget(product_price)
        product_card.add_widget(product_description)

        self.add_widget(product_card)

        back_button = MDFillRoundFlatButton(
            text="Retour",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: MDApp.get_running_app().go_home(),
            md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
            text_color=MDApp.get_running_app().theme_cls.primary_light
        )

        self.add_widget(back_button)




MainApp().run()
