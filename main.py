import flet as ft
import time
import threading
import random
import os
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

class ErgonomicsApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ergonomics Helper"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window_width = 450
        self.page.window_height = 400 # Adjusted height
        self.page.window_visible = False # Start hidden
        self.page.window_skip_task_bar = True # Try to hide from taskbar/dock (experimental)
        self.page.on_window_event = self.window_event_handler

        # --- Tip Data ---
        self.tips_data = {
            "Maintain a neutral wrist posture.": "wrist.png",
            "Adjust your chair height so your feet are flat on the floor.": "chair_height.png",
            "Take short breaks every 30 minutes to stretch.": "stretch.png",
            "Position your monitor an arm's length away.": "monitor_distance.png",
            "Ensure your screen top is at or slightly below eye level.": "monitor_height.png",
            # Add more tips and corresponding image names in 'assets/'
            "Relax your shoulders.": "shoulders.png",
            "Blink often to keep eyes moist.": "eyes.png",
        }
        self.tips = list(self.tips_data.keys())

        # --- UI Elements ---
        self.tip_display = ft.Text(
            "Time for an ergo tip!",
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            width=380,
        )

        self.image_control = ft.Image(
            width=250,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )

        self.image_display_container = ft.Container(
            content=self.image_control,
            width=252,
            height=152,
            border=ft.border.all(1, ft.Colors.GREY_400),
            alignment=ft.alignment.center
        )

        self.dismiss_button = ft.ElevatedButton("Got it!", on_click=self.dismiss_window)

        # --- Pop-up Timer Settings ---
        self.popup_interval_seconds = int(os.getenv("POPUP_INTERVAL_SECONDS", 30))
        self._popup_thread = None
        self._stop_popup_event = threading.Event()

        # --- Layout ---
        self.page.add(
            ft.Column(
                [
                    ft.Container(height=10), # Top padding
                    self.tip_display,
                    ft.Container(height=15),
                    self.image_display_container,
                    ft.Container(height=20),
                    self.dismiss_button,
                    ft.Container(height=10), # Bottom padding
                ],
                alignment=ft.MainAxisAlignment.CENTER, # Center content vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )
        # Ensure the window is hidden after setup
        self.page.update() # Update to apply initial settings like hidden


    def show_window_with_tip(self) -> None:
        """Makes the window visible and displays a random tip."""
        if self._stop_popup_event.is_set() or not self.page:
             return

        logging.info("Popup triggered.")
        random_tip = random.choice(self.tips)
        image_file = self.tips_data.get(random_tip, "default.png")
        image_path = f"/assets/{image_file}"

        self.tip_display.value = random_tip
        self.image_control.src = image_path

        try:
            self.page.window_visible = True
            self.page.update()
            # Try to bring the window to the front (might not work reliably on all OS)
            self.page.window_to_front()
            logging.info("Showing tip: %s", random_tip)
        except Exception as e:
             logging.error("Error showing window: %s", e)


    def dismiss_window(self, e: ft.ControlEvent = None):
        """Hides the window."""
        logging.debug("dismiss_window method called.")
        if not self.page:
            logging.warning("Page object is None. Cannot dismiss window.")
            return
        try:
            logging.info("Dismissing window.")
            self.page.window_visible = False
            self.page.update()
            logging.debug("Window visibility set to False and page updated.")
        except Exception as e:
            logging.error("Error dismissing window: %s", e)


    def _popup_loop(self) -> None:
        """Background loop to trigger pop-ups."""
        logging.info("Popup thread started. Interval: %s seconds", self.popup_interval_seconds)
        # Wait a bit initially before first popup
        time.sleep(5)
        while not self._stop_popup_event.wait(self.popup_interval_seconds):
            if self.page: # Check if page exists
                try:
                    # Schedule the UI update on the main Flet thread if needed,
                    # but direct call might work for visibility change.
                    self.show_window_with_tip()
                except Exception as e:
                    logging.error("Error in popup loop calling show_window: %s", e)
            else:
                logging.warning("Page object no longer exists, stopping popup loop.")
                break # Exit loop if page is gone
        logging.info("Popup thread stopped.")


    def start_popup_thread(self) -> None:
        """Starts the pop-up timer thread."""
        if self._popup_thread is None or not self._popup_thread.is_alive():
            self._stop_popup_event.clear()
            self._popup_thread = threading.Thread(target=self._popup_loop, daemon=True)
            self._popup_thread.start()
            logging.info("Popup thread initiated.")


    def stop_popup_thread(self) -> None:
        """Signals the pop-up timer thread to stop."""
        logging.info("Stopping popup thread...")
        self._stop_popup_event.set()


    def window_event_handler(self, e: ft.WindowEvent) -> None:
        """Handle window events, like closing."""
        if e.data == "close":
            logging.info("Window close event detected by user.")
            # Instead of destroying, just hide the window
            self.dismiss_window()
            # To prevent the default close action which terminates the app,
            # we might need more complex handling or rely on the user
            # not expecting termination from this close button.
            # For now, this dismisses, but Flet might still terminate depending on version/OS.
            # A truly robust solution often needs a system tray icon to manage the lifecycle.


def main(page: ft.Page):
    # Set window properties that might need to be set early
    # page.window_title = "Ergo Helper BG" # Title might show briefly

    # Create the app instance (which sets window_visible=False initially)
    app = ErgonomicsApp(page)

    # Start the background thread that will periodically show the window
    app.start_popup_thread()

    # No need to manually show a tip here as it starts hidden.

# Note: System tray icon features are not added here but would be needed
# for a proper way to exit the application gracefully when hidden.
ft.app(target=main, assets_dir="assets")