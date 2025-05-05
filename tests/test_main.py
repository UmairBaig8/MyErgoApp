import unittest
from unittest.mock import MagicMock
import flet as ft
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import ErgonomicsApp

class TestErgonomicsApp(unittest.TestCase):
    def setUp(self):
        self.page = MagicMock(spec=ft.Page)
        self.app = ErgonomicsApp(self.page)

    def test_show_window_with_tip(self):
        self.app.show_window_with_tip()
        self.assertTrue(self.page.window_visible)
        self.page.update.assert_called_once()

    def test_dismiss_window(self):
        self.app.dismiss_window()
        self.assertFalse(self.page.window_visible)
        self.page.update.assert_called_once()

    def test_start_popup_thread(self):
        self.app.start_popup_thread()
        self.assertIsNotNone(self.app._popup_thread)
        self.assertTrue(self.app._popup_thread.is_alive())

    def test_stop_popup_thread(self):
        self.app.start_popup_thread()
        self.app.stop_popup_thread()
        self.assertTrue(self.app._stop_popup_event.is_set())

if __name__ == "__main__":
    unittest.main()