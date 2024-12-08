import cv2
import pytesseract
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.text_input = TextInput(hint_text='Сканируйте текст здесь', multiline=True, size_hint_y=0.8)
        scan_button = Button(text='Сканировать текст', size_hint_y=0.1)
        save_button = Button(text='Сохранить текст', size_hint_y=0.1)

        scan_button.bind(on_press=self.scan_text)
        save_button.bind(on_press=self.save_to_db)

        layout.add_widget(self.text_input)
        layout.add_widget(scan_button)
        layout.add_widget(save_button)

        return layout

    def scan_text(self, instance):
        cap = cv2.VideoCapture(0)  # Используйте 0 для захвата с веб-камеры
        ret, frame = cap.read()
        if ret:
            # Примените OCR
            text = pytesseract.image_to_string(frame)
            self.text_input.text = text
        cap.release()

    def save_to_db(self, instance):
        text = self.text_input.text
        if text:
            conn = sqlite3.connect('books.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS texts (content TEXT)')
            c.execute('INSERT INTO texts (content) VALUES (?)', (text,))
            conn.commit()
            conn.close()
            self.text_input.text = ''  # Очистить поле ввода после сохранения

if __name__ == '__main__':
    MyApp().run()