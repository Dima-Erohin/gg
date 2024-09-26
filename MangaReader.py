# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout
import os

#Window.size = (360, 480)  # Задаем размер окна для эмуляции мобильного экрана

# Определение главного экрана с карточками
class MainScreen(Screen):
    def on_kv_post(self, base_widget):
        # Этот метод вызывается после того, как KV-файл полностью загружен
        self.add_cards()

    def add_cards(self):
        subfolders = [f.path for f in os.scandir('Manga') if f.is_dir()]
        # Добавляем несколько карточек с изображением и подписью
        for subfolder in subfolders:
            files = sorted(os.listdir(subfolder))
            # Ищем первое изображение
            first_image = None
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')):  # Список расширений изображений
                    first_image = file
                    break

            if first_image:
                image_path = os.path.join(subfolder, first_image)
                card = MDCard(
                    orientation='vertical',  # Устанавливаем вертикальную ориентацию
                    size_hint=(None, None),
                    size=("280dp", "180dp"),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    ripple_behavior=True,
                    on_release=lambda *args, index=subfolder: self.on_card_click(index)
                )

                # Создаем контейнер для изображения и текста
                card_box = BoxLayout(orientation='vertical')

                # Добавляем изображение в карточку
                card_box.add_widget(
                    Image(
                        source=image_path,
                        size_hint=(1, 0.8),  # 80% от высоты будет занимать изображение
                        allow_stretch=True  # Разрешаем растягивание изображения
                    )
                )

                # Добавляем текст под изображением
                card_box.add_widget(
                    MDLabel(
                        text=os.path.basename(subfolder),
                        halign='center',  # Выравнивание текста по центру
                        size_hint=(1, 0.2)  # 20% от высоты будет занимать текст
                    )
                )

                # Добавляем всё в карточку
                card.add_widget(card_box)
                self.ids.cards_layout.add_widget(card)

            else:
                print("Изображения не найдены в этой папке.")



    def on_card_click(self, index):
        # При нажатии на карточку переходим на экран просмотра изображений
        self.manager.current = 'viewer'
        self.manager.get_screen('viewer').set_images(index)

# Экран для просмотра изображений .webp
class ImageViewer(Screen):
    images = ListProperty([])

    def set_images(self, index):
        # Устанавливаем изображения для просмотра (для примера используем изображения в формате webp)
        files = sorted(os.listdir(index))
        self.images = [f'{index}/{i}' for i in files]
        self.current_image_index = 0
        self.update_image()

    def update_image(self):
        # Обновляем изображение на экране
        self.ids.image_view.source = self.images[self.current_image_index]

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
        self.update_image()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
        self.update_image()

class ImageApp(MDApp):
    def build(self):
        # Загрузка интерфейса из файла .kv
        return Builder.load_string(KV)

# Определение интерфейса в формате KV Language
KV = '''
ScreenManager:
    MainScreen:
    ImageViewer:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        ScrollView:
            MDGridLayout:
                id: cards_layout
                cols: 1
                adaptive_height: True
        MDFloatLayout:
            MDFlatButton:
                text: 'Exit'
                pos_hint: {'center_x': 0.5, 'center_y': 0.05}
                on_release: app.stop()

<ImageViewer>:
    name: 'viewer'
    BoxLayout:
        orientation: 'vertical'
        Image:
            id: image_view
            source: ''
            allow_stretch: True
        BoxLayout:
            size_hint_y: 0.2
            MDFlatButton:
                text: 'Previous'
                on_release: root.previous_image()
            MDFlatButton:
                text: 'Back to main'
                on_release: app.root.current = 'main'
            MDFlatButton:
                text: 'Next'
                on_release: root.next_image()
'''

# Запуск приложения
if __name__ == '__main__':
    ImageApp().run()
