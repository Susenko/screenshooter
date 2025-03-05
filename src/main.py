import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

ICON_PATH = "icons/icon.png"

class TrayApp:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "Screenshooter",
            ICON_PATH,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Create the menu
        self.menu = Gtk.Menu()

        # Exit menu item
        exit_item = Gtk.MenuItem(label="Exit")
        exit_item.connect("activate", self.quit_app)
        self.menu.append(exit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def quit_app(self, _):
        Gtk.main_quit()

def main():
    app = TrayApp()
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Handle Ctrl+C properly
    Gtk.main()

if __name__ == "__main__":
    main()
