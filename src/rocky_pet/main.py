import sys
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("Rocky Desktop Pet")

    from rocky_pet.app import RockyApp
    rocky_app = RockyApp()
    rocky_app.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
