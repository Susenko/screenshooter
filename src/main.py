import gi
import time
import numpy as np
import imageio
import subprocess
import os
import pyautogui
from PIL import Image
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

ICON_PATH = "icons/icon.png"
GIF_PATH = "screenshots/recording.gif"
SCREENSHOT_PATH = "screenshots/screenshot.png"
RECORDING = False  # Flag to control GIF recording

class TrayApp:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "Screenshooter",
            ICON_PATH,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.create_menu()

    def create_menu(self):
        self.menu = Gtk.Menu()

        # Take Screenshot
        screenshot_item = Gtk.MenuItem(label="📸 Take Screenshot")
        screenshot_item.connect("activate", self.take_screenshot)
        self.menu.append(screenshot_item)

        # Start GIF Recording
        self.record_gif_item = Gtk.MenuItem(label="🎥 Start GIF Recording")
        self.record_gif_item.connect("activate", self.start_gif_recording)
        self.menu.append(self.record_gif_item)

        # Stop GIF Recording
        stop_recording_item = Gtk.MenuItem(label="⏹ Stop GIF Recording")
        stop_recording_item.connect("activate", self.stop_gif_recording)
        self.menu.append(stop_recording_item)

        # Exit Option
        exit_item = Gtk.MenuItem(label="❌ Exit")
        exit_item.connect("activate", self.quit_app)
        self.menu.append(exit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def take_screenshot(self, _):
        try:
            # Define the screenshot directory and file path
            screenshot_dir = os.path.expanduser("screenshots")
            screenshot_path = os.path.join(screenshot_dir, "screenshot.png")

            # Ensure the directory exists
            os.makedirs(screenshot_dir, exist_ok=True)

            # Capture the screenshot
            subprocess.run(["gnome-screenshot", "-f", screenshot_path], check=True)
            print(f"✅ Screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")


    def start_gif_recording(self, _):
        global RECORDING
        if RECORDING:
            print("⚠️ Already recording!")
            return

        RECORDING = True
        duration = 5  # Record for 5 seconds
        fps = 10
        frames = []

        print("🎥 Recording GIF...")

        for _ in range(duration * fps):
            frame = pyautogui.screenshot()
            frames.append(np.array(frame))
            time.sleep(1 / fps)

        imageio.mimsave(GIF_PATH, frames, fps=fps)
        print(f"✅ GIF saved to {GIF_PATH}")
        RECORDING = False

    def stop_gif_recording(self, _):
        global RECORDING
        if RECORDING:
            RECORDING = False
            print("⏹ Recording stopped.")
        else:
            print("⚠️ No active recording.")

    def quit_app(self, _):
        Gtk.main_quit()

def main():
    app = TrayApp()
    Gtk.main()

if __name__ == "__main__":
    main()
