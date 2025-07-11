import os
import polib
import shutil
from datetime import datetime
from googletrans import Translator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QPushButton, QTextEdit, QFileDialog,
                             QListWidget, QCheckBox, QMessageBox, QProgressBar, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon


class TranslationWorker(QThread):
    progress = pyqtSignal(int, str)  # Progress percentage and status message
    finished = pyqtSignal(dict)  # Final results
    error = pyqtSignal(str)  # Errors

    def __init__(self, target_lang, po_file_path, selected_types):
        super().__init__()
        self.target_lang = target_lang
        self.po_file_path = po_file_path
        self.selected_types = selected_types
        self.translator = Translator(service_urls=['translate.google.com'])
        self.is_running = True

    def run(self):
        try:
            # Create backup
            backup_dir = 'locale_backups'
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f'django_{self.target_lang}_{timestamp}.po')
            shutil.copyfile(self.po_file_path, backup_path)
            self.progress.emit(5, "Backup file created")

            # Load PO file
            po = polib.pofile(self.po_file_path)
            total_entries = len(po)
            translate_all_types = not self.selected_types
            self.progress.emit(10, f"Found {total_entries} entries to process")

            results = {
                'translated': 0,
                'skipped': 0,
                'errors': 0,
                'backup_path': backup_path
            }

            for i, entry in enumerate(po):
                if not self.is_running:
                    self.progress.emit(0, "Translation stopped by user")
                    return

                if entry.msgstr.strip() == "" and self.is_entry_from_selected_type(entry, translate_all_types):
                    try:
                        # Improved translation logic
                        if self.target_lang == 'fa':
                            # Translate from English to Persian
                            translated = self.translate_text(entry.msgid, 'en', 'fa')
                        elif entry.msgid.strip() == "":
                            # Skip empty strings
                            results['skipped'] += 1
                            continue
                        else:
                            # For other languages, translate from English to target
                            translated = self.translate_text(entry.msgid, 'en', self.target_lang)

                        entry.msgstr = translated
                        results['translated'] += 1
                        self.progress.emit(int((i + 1) / total_entries * 80), f"Translating entry {i + 1}")
                    except Exception as e:
                        results['errors'] += 1
                        entry.comment = f"Translation error: {str(e)}"
                        self.progress.emit(int((i + 1) / total_entries * 80), f"Error translating entry {i + 1}")
                else:
                    results['skipped'] += 1

            # Save file
            po.save()
            self.progress.emit(95, "Saving translated file...")
            results['output_path'] = self.po_file_path
            self.finished.emit(results)

        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        self.is_running = False

    def is_entry_from_selected_type(self, entry, translate_all):
        if translate_all:
            return True
        for comment in entry.occurrences:
            for file_type in self.selected_types:
                if comment[0].endswith(f".{file_type}"):
                    return True
        return False

    def translate_text(self, text, src, dest):
        try:
            # اگر متن خالی است، همان را برگردان
            if not text.strip():
                return ""

            # اگر زبان مقصد فارسی است، از انگلیسی به فارسی ترجمه کن
            if dest == 'fa':
                # بررسی کنیم که آیا متن ورودی انگلیسی است یا نه
                # اگر متن انگلیسی است (فقط حروف ASCII دارد)، مستقیما ترجمه کنیم
                if text.isascii():
                    return self.translator.translate(text, src='en', dest='fa').text
                # اگر متن انگلیسی نیست، احتمالا فارسی است و نیازی به ترجمه نیست
                else:
                    return text
            else:
                # برای سایر زبان‌ها از انگلیسی به زبان مقصد ترجمه کنیم
                if text.isascii():
                    # اگر متن انگلیسی است، مستقیما ترجمه کنیم
                    return self.translator.translate(text, src='en', dest=dest).text
                else:
                    # اگر متن انگلیسی نیست، احتمالا فارسی است، پس اول به انگلیسی ترجمه کنیم
                    english_text = self.translator.translate(text, src='fa', dest='en').text
                    # سپس از انگلیسی به زبان مقصد ترجمه کنیم
                    return self.translator.translate(english_text, src='en', dest=dest).text
        except Exception as e:
            raise Exception(f"ترجمه ناموفق: {str(e)}")


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_connections()
        self.setup_styles()

        # PO file path
        self.po_file_path = None
        # Translation worker
        self.worker = None

    def setup_ui(self):
        """Setup the UI"""
        self.setWindowTitle("Django Translation Assistant - Advanced Version")
        self.setWindowIcon(QIcon('translate_icon.png'))  # You need an icon file
        self.setGeometry(100, 100, 900, 700)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # File and language selection group
        file_group = QGroupBox("Translation Settings")
        file_layout = QVBoxLayout()

        # Language selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Target Language:"))
        self.lang_combo = QComboBox()
        self.available_languages = {
            'en': 'English',
            'ar': 'Arabic',
            'fa': 'Persian',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'ru': 'Russian',
            'zh-cn': 'Chinese (Simplified)'
        }
        for code, name in self.available_languages.items():
            self.lang_combo.addItem(f"{name} ({code})", code)
        lang_layout.addWidget(self.lang_combo)
        file_layout.addLayout(lang_layout)

        # File selection
        file_sel_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #666; font-style: italic;")
        file_sel_layout.addWidget(self.file_label, stretch=1)

        self.browse_btn = QPushButton("Select .po File")
        self.browse_btn.setIcon(QIcon('folder_icon.png'))  # You need an icon file
        file_sel_layout.addWidget(self.browse_btn)
        file_layout.addLayout(file_sel_layout)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # Advanced settings group
        settings_group = QGroupBox("Advanced Settings")
        settings_layout = QVBoxLayout()

        # File type selection
        settings_layout.addWidget(QLabel("Only translate files with these extensions:"))
        self.file_types_list = QListWidget()
        self.file_types_list.setSelectionMode(QListWidget.MultiSelection)
        for ext in ['html', 'py', 'txt', 'js', 'json', 'xml', 'md']:
            self.file_types_list.addItem(ext)
        settings_layout.addWidget(self.file_types_list)

        # Options
        self.backup_check = QCheckBox("Create backup before translation (recommended)")
        self.backup_check.setChecked(True)
        settings_layout.addWidget(self.backup_check)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(True)
        self.progress.setFormat("%v% - %p%")
        main_layout.addWidget(self.progress)

        self.status_label = QLabel("Ready to start...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #444; font-weight: bold;")
        main_layout.addWidget(self.status_label)

        # Log
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Translation log will appear here...")
        main_layout.addWidget(self.log, stretch=1)

        # Buttons
        btn_layout = QHBoxLayout()

        self.translate_btn = QPushButton("Start Translation")
        self.translate_btn.setIcon(QIcon('start_icon.png'))
        self.translate_btn.setToolTip("Start translation process")
        btn_layout.addWidget(self.translate_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setIcon(QIcon('stop_icon.png'))
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("Stop current translation")
        btn_layout.addWidget(self.stop_btn)

        self.compile_btn = QPushButton("Compile Messages")
        self.compile_btn.setIcon(QIcon('compile_icon.png'))
        self.compile_btn.setToolTip("Run compilemessages command")
        btn_layout.addWidget(self.compile_btn)

        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.setIcon(QIcon('clear_icon.png'))
        self.clear_btn.setToolTip("Clear log window")
        btn_layout.addWidget(self.clear_btn)

        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setIcon(QIcon('exit_icon.png'))
        btn_layout.addWidget(self.exit_btn)

        main_layout.addLayout(btn_layout)

        # Status bar
        self.statusBar().showMessage("Version 2.0 - Developed for Django")

    def setup_connections(self):
        """Setup signal-slot connections"""
        self.browse_btn.clicked.connect(self.browse_po_file)
        self.translate_btn.clicked.connect(self.start_translation)
        self.stop_btn.clicked.connect(self.stop_translation)
        self.compile_btn.clicked.connect(self.compile_messages)
        self.clear_btn.clicked.connect(self.clear_log)
        self.exit_btn.clicked.connect(self.close)

        # RTL direction for Persian
        self.setLayoutDirection(Qt.RightToLeft)
        self.lang_combo.setLayoutDirection(Qt.LeftToRight)
        self.file_types_list.setLayoutDirection(Qt.LeftToRight)

    def setup_styles(self):
        """Setup visual styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                right: 10px;
                padding: 0 3px;
            }
            QPushButton {
                padding: 5px 10px;
                min-width: 80px;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                font-family: 'Courier New', monospace;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)

        # Font for Persian support
        font = QFont()
        font.setFamily("B Nazanin" if os.name == 'nt' else "DejaVu Sans")
        font.setPointSize(10)
        self.setFont(font)

    def browse_po_file(self):
        """Select PO file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Please select .po file",
            "locale", "Translation files (*.po)")

        if file_path:
            self.po_file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.file_label.setStyleSheet("color: #000; font-style: normal;")
            self.log.append(f"Selected file: {file_path}")

    def start_translation(self):
        """Start translation process"""
        if not self.po_file_path:
            QMessageBox.warning(self, "Error", "Please select a .po file first")
            return

        target_lang = self.lang_combo.currentData()
        selected_types = [item.text() for item in self.file_types_list.selectedItems()]

        self.log.append(f"\nStarting translation to {self.available_languages[target_lang]}...")
        self.log.append(f"Selected file types: {', '.join(selected_types) if selected_types else 'All types'}")

        # Disable buttons during translation
        self.translate_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.browse_btn.setEnabled(False)

        # Create translation worker
        self.worker = TranslationWorker(target_lang, self.po_file_path, selected_types)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.translation_complete)
        self.worker.error.connect(self.translation_error)
        self.worker.start()

    def stop_translation(self):
        """Stop running translation"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.terminate()
            self.log.append("\nTranslation stopped by user!")
            self.status_label.setText("Translation stopped")
            self.reset_ui_after_translation()

    def update_progress(self, value, message):
        """Update progress and status message"""
        self.progress.setValue(value)
        self.status_label.setText(message)

        if value >= 95:
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        elif value >= 70:
            self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #444; font-weight: bold;")

    def translation_complete(self, results):
        """After translation completes"""
        self.log.append("\nTranslation completed successfully!")
        self.log.append(f"→ Translated: {results['translated']}")
        self.log.append(f"→ Skipped: {results['skipped']}")
        self.log.append(f"→ Errors: {results['errors']}")
        self.log.append(f"→ Backup path: {results['backup_path']}")

        self.status_label.setText("Translation completed successfully!")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.progress.setValue(100)

        self.reset_ui_after_translation()

        QMessageBox.information(
            self,
            "Completed",
            f"Translation completed successfully!\n\n"
            f"Translated: {results['translated']}\n"
            f"Skipped: {results['skipped']}\n"
            f"Errors: {results['errors']}"
        )

    def translation_error(self, error_msg):
        """Handle translation errors"""
        self.log.append(f"\nError: {error_msg}")
        self.status_label.setText("Translation error!")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        self.reset_ui_after_translation()

        QMessageBox.critical(
            self,
            "Translation Error",
            f"The following error occurred:\n\n{error_msg}"
        )

    def reset_ui_after_translation(self):
        """Reset UI after translation completes"""
        self.translate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.browse_btn.setEnabled(True)
        if self.worker:
            self.worker = None

    def compile_messages(self):
        """Compile messages"""
        try:
            self.log.append("\nCompiling messages...")
            os.system('python manage.py compilemessages')
            self.log.append("Messages compiled successfully")
            QMessageBox.information(self, "Completed", "Messages compiled successfully")
        except Exception as e:
            self.log.append(f"\nCompilation error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error compiling messages:\n{str(e)}")

    def clear_log(self):
        """Clear log window"""
        self.log.clear()
        self.status_label.setText("Ready to start...")
        self.status_label.setStyleSheet("color: #444; font-weight: bold;")
        self.progress.setValue(0)

    def closeEvent(self, event):
        """Handle window close event"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, 'Translation in progress',
                "Translation is still running. Are you sure you want to quit?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.worker.stop()
                self.worker.terminate()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication([])

    # Set application style
    app.setStyle('Fusion')

    # Set default font for Persian support
    font = QFont()
    font.setFamily("B Nazanin" if os.name == 'nt' else "DejaVu Sans")
    font.setPointSize(10)
    app.setFont(font)

    window = TranslatorApp()
    window.show()
    app.exec_()