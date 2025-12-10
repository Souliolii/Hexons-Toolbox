import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame,
)
from PySide6.QtCore import Qt


def get_tools_source_dir() -> Path:
    """
    Where the bundled tool EXEs live.

    - When frozen (PyInstaller): use sys._MEIPASS/tools
    - When running from source: use ./tools next to this .py
    """
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent

    return base / "tools"


def get_tools_runtime_dir() -> Path:
    """
    Where we extract/copy the tool EXEs to run them from.
    This is a temp folder specific to Hexon's Toolbox.
    """
    temp_root = Path(tempfile.gettempdir()) / "HexonsToolboxTools"
    temp_root.mkdir(parents=True, exist_ok=True)
    return temp_root


class ToolCard(QFrame):
    def __init__(self, title: str, description: str, exe_name: str, parent=None):
        super().__init__(parent)
        self.exe_name = exe_name

        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("toolCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("toolTitle")

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setObjectName("toolDescription")

        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.launch_tool)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(open_btn)
        layout.addLayout(btn_row)

    def launch_tool(self):
        source_dir = get_tools_source_dir()
        runtime_dir = get_tools_runtime_dir()

        src_path = source_dir / self.exe_name
        dst_path = runtime_dir / self.exe_name

        if not src_path.exists():
            QMessageBox.critical(
                self,
                "Tool Missing",
                f"Bundled tool not found:\n{src_path}\n\n"
                "Make sure it was included with --add-data when building."
            )
            return

        try:
            # Copy (or overwrite) the tool into the runtime temp folder
            shutil.copy2(src_path, dst_path)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Failed to Extract Tool",
                f"Could not copy tool to temp folder.\n\n"
                f"Source: {src_path}\n"
                f"Dest: {dst_path}\n\n"
                f"Error: {e}"
            )
            return

        try:
            subprocess.Popen([str(dst_path)], cwd=str(runtime_dir))
        except Exception as e:
            QMessageBox.critical(
                self,
                "Failed to Launch",
                f"Could not launch tool:\n{dst_path}\n\nError:\n{e}"
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hexon's Toolbox")
        self.resize(600, 380)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header = QLabel("Hexon's Toolbox")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("headerLabel")

        subtitle = QLabel("Quick access to your MapleStory dev tools.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitleLabel")

        layout.addWidget(header)
        layout.addWidget(subtitle)

        # --- TOOLS YOU CURRENTLY HAVE ---
        tools = [
            (
                "Quest Editor",
                "GUI editor for MapleStory quest XMLs (QuestInfo, Check, Act).",
                "MapleStory Quest Editor.exe",
            ),
            (
                "WZ Icon Flattener",
                "Flatten dumped WZ data into PNG icons + JSON database (icon_db.json).",
                "wz_icon_flattener_gui.exe",
            ),
            (
                "WZ Icon Viewer",
                "Browse and search the flattened MapleStory PNG icons.",
                "wz_icon_viewer_gui.exe",
            ),
        ]

        for title, desc, exe in tools:
            layout.addWidget(ToolCard(title, desc, exe))

        layout.addStretch()

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #101014;
            }

            #headerLabel {
                font-size: 22px;
                font-weight: bold;
                color: white;
            }

            #subtitleLabel {
                color: #bbbbbb;
                font-size: 12px;
            }

            #toolCard {
                background-color: #181820;
                border: 1px solid #2b2b35;
                border-radius: 10px;
            }

            #toolTitle {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }

            #toolDescription {
                font-size: 11px;
                color: #c0c0c0;
            }
        """)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
