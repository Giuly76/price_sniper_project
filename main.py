from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from scraper import get_suspicious_prices

class PriceSniperApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        results_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        results_layout.bind(minimum_height=results_layout.setter('height'))

        sospetti = get_suspicious_prices()
        if not sospetti:
            results_layout.add_widget(Label(text="Nessun prezzo sospetto trovato"))
        else:
            for item in sospetti:
                text = f"{item['Sito']} - {item['Nome']} : €{item['Prezzo (€)']}"
                btn = Button(text=text, size_hint_y=None, height=50, on_release=lambda x, link=item['Link']: self.open_link(link))
                results_layout.add_widget(btn)

        scroll.add_widget(results_layout)
        layout.add_widget(scroll)
        return layout

    def open_link(self, link):
        import webbrowser
        webbrowser.open(link)

if __name__ == '__main__':
    PriceSniperApp().run()
