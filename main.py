from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from pyzbar.pyzbar import ZBarSymbol
from kivymd.uix.snackbar import Snackbar
from kivy_garden.zbarcam import ZBarCam
from kivymd.uix.button import MDFlatButton

from request import get_token_from_api_with_passphrase, token_decode


class MainLayout(BoxLayout):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.layout = MainLayout()
        self.login_screen = Builder.load_file('views/login.kv')
        self.home_screen = Builder.load_file('views/home.kv')
        self.layout.add_widget(self.login_screen)

        return self.layout

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
        self.layout.clear_widgets()
        self.cam.play = False
        self.qr_code_screen = None
        self.layout.add_widget(self.home_screen)

    def go_home(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.home_screen)

    def on_symbols(self, instance, symbols):
        if symbols:
            for symbol in symbols:
                token = get_token_from_api_with_passphrase(symbol.data.decode())
                if (token is not False):
                    self.stop_qrcode()
                else:
                    print("wrong token")


MainApp().run()
