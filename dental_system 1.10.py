import sys
import json
import os
import shutil  # (NEW) For backup/restore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QVBoxLayout,
    QHBoxLayout, QGroupBox, QLabel, QLineEdit, QComboBox, QTextEdit,
    QRadioButton, QButtonGroup, QSizePolicy, QSpacerItem, QFormLayout,
    QDateEdit, QFileDialog, QMessageBox,
    QListWidget, QCheckBox, QDateTimeEdit, QListWidgetItem,
    QTabWidget, QSplitter, QFrame, QScrollArea, QAbstractButton,
    QDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import (
    QColor, QPalette, QFont, QIcon, QPixmap, QTextDocument,
    QDesktopServices, QDoubleValidator  # (ថ្មី) បន្ថែម QDoubleValidator
)

# (CHANGED) Imports for printing
from PyQt5.QtGui import (
    QColor, QPalette, QFont, QIcon, QPixmap, QTextDocument,
    QDesktopServices  # (NEW) For opening image links
)
from PyQt5.QtCore import (
    pyqtSlot, Qt, QSize, QDate, QDateTime,
    pyqtSignal, QUrl  # (NEW) For signals and opening links
)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# (NEW) Import the translation dictionaries
from translations import LANG_STRINGS, STATUS_LIST_KEYS

# --- Enhanced Global QSS Stylesheet ---
GLOBAL_QSS = """
/* --- Base Window --- */
QMainWindow, QWidget {
    background-color: #F8F9FA;
    color: #2C3E50;
    font-family: "Segoe UI", "Khmer OS", Arial, sans-serif;
    font-size: 9pt; 
}

/* --- Header Styles --- */
.header-label {
    font-size: 14pt; 
    font-weight: bold;
    color: #2C3E50;
    padding: 10px;
    background-color: #3498DB;
    color: white;
    border-radius: 8px;
    margin: 5px;
}

.subheader-label {
    font-size: 10pt; 
    font-weight: bold;
    color: #3498DB;
    margin: 5px 0px;
}

/* --- Group Boxes --- */
QGroupBox {
    background-color: #FFFFFF;
    border: 2px solid #E9ECEF;
    border-radius: 10px;
    margin-top: 20px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 15px;
    background-color: #3498DB;
    color: white;
    border-radius: 6px;
    font-weight: bold;
}

/* --- Cards --- */
.card {
    background-color: #FFFFFF;
    border: 1px solid #E9ECEF;
    border-radius: 8px;
    padding: 15px;
    margin: 5px;
}

/* --- Labels --- */
QLabel {
    color: #2C3E50;
    background-color: transparent;
    padding: 2px;
}

.emphasis-label {
    font-weight: bold;
    color: #2C3E50;
    font-size: 9pt; 
}

/* --- Input Fields --- */
QLineEdit, QTextEdit, QComboBox, QDateEdit, QDateTimeEdit {
    background-color: #FFFFFF;
    color: #2C3E50;
    border: 2px solid #E9ECEF;
    border-radius: 6px;
    padding: 8px;
    font-size: 9pt; 
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QDateTimeEdit:focus {
    border-color: #3498DB;
    background-color: #F8F9FA;
}

QListWidget {
    background-color: #FFFFFF;
    color: #2C3E50;
    border: 2px solid #E9ECEF;
    border-radius: 6px;
    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #E9ECEF;
}

QListWidget::item:hover {
    background-color: #EAF2F8;
}

QListWidget::item:selected {
    background-color: #3498DB;
    color: white;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #2C3E50;
    selection-background-color: #3498DB;
    border: 1px solid #E9ECEF;
    border-radius: 6px;
}

/* === Buttons === */

/* Primary Button */
QPushButton {
    background-color: #3498DB;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 9pt; 
}

QPushButton:hover {
    background-color: #2980B9;
}

QPushButton:pressed {
    background-color: #21618C;
}

QPushButton:disabled {
    background-color: #BDC3C7;
    color: #7F8C8D;
}

/* Success Button */
QPushButton.success-button {
    background-color: #27AE60;
}

QPushButton.success-button:hover {
    background-color: #229954;
}

QPushButton.success-button:pressed {
    background-color: #1E8449;
}

/* Warning Button */
QPushButton.warning-button {
    background-color: #E67E22;
}

QPushButton.warning-button:hover {
    background-color: #D35400;
}

QPushButton.warning-button:pressed {
    background-color: #BA4A00;
}

/* Danger Button */
QPushButton.danger-button {
    background-color: #E74C3C;
}

QPushButton.danger-button:hover {
    background-color: #CB4335;
}

QPushButton.danger-button:pressed {
    background-color: #A93226;
}

/* Info Button */
QPushButton.info-button {
    background-color: #17A2B8;
}

QPushButton.info-button:hover {
    background-color: #138496;
}

QPushButton.info-button:pressed {
    background-color: #0F6674;
}

/* --- Radio Buttons --- */
QRadioButton {
    color: #2C3E50;
    padding: 5px;
    background-color: transparent;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
}

QRadioButton::indicator::unchecked {
    border: 2px solid #BDC3C7;
    background-color: #FFFFFF;
}

QRadioButton::indicator::checked {
    border: 2px solid #3498DB;
    background-color: #3498DB;
}

/* --- Check Box --- */
QCheckBox {
    color: #2C3E50;
    padding: 5px;
    background-color: transparent;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
}

QCheckBox::indicator::unchecked {
    border: 2px solid #BDC3C7;
    background-color: #FFFFFF;
}

QCheckBox::indicator::checked {
    border: 2px solid #3498DB;
    background-color: #3498DB;
}

/* --- Tab Widget --- */
QTabWidget::pane {
    border: 2px solid #E9ECEF;
    border-top: none;
    background-color: #FFFFFF;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}

QTabBar::tab {
    background-color: #EAECEE;
    color: #5D6D7E;
    padding: 12px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 2px solid #E9ECEF;
    border-bottom: none;
    font-weight: bold;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #3498DB;
    border-color: #E9ECEF;
    border-bottom: none;
}

QTabBar::tab:!selected:hover {
    background-color: #F4F6F6;
    color: #2980B9;
}

/* --- Splitter --- */
QSplitter::handle {
    background-color: #E9ECEF;
    border: 1px solid #D6DBDF;
}

QSplitter::handle:horizontal {
    width: 8px;
}

QSplitter::handle:vertical {
    height: 8px;
}

QSplitter::handle:hover {
    background-color: #3498DB;
}

/* --- Message Box --- */
QMessageBox {
    background-color: #FFFFFF;
}

QMessageBox QLabel {
    color: #2C3E50;
    font-size: 9pt; 
}

QMessageBox QPushButton {
    padding: 8px 20px;
    min-width: 80px;
    margin: 5px;
}

/* --- Status Indicators --- */
.status-indicator {
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 9pt; 
}

.status-present {
    background-color: #D5F5E3;
    color: #27AE60;
}

.status-missing {
    background-color: #FADBD8;
    color: #E74C3C;
}

.status-treatment {
    background-color: #D6EAF8;
    color: #2980B9;
}

/* --- Separator Line --- */
.line {
    background-color: #E9ECEF;
    border: none;
    margin: 10px 0px;
}
"""""

# Backend Logic
class Tooth:
    def __init__(self, fdi_number, name_keys_tuple):
        self.fdi_number = fdi_number
        # (CHANGED) Store language keys, not a translated string
        self.name_keys = name_keys_tuple 
        # (CHANGED) Store status as a language key
        self.status = "present" 
        self.notes = ""

    def __repr__(self):
        # (CHANGED) Represent using keys
        return f"Tooth {self.fdi_number} ({self.name_keys}): {self.status}"

class DentalChart:
    # (CHANGED) Quadrants now use language keys
    PERMANENT_QUADRANTS = {
        1: "perm_up_right",
        2: "perm_up_left",
        3: "perm_low_left",
        4: "perm_low_right",
    }
    PRIMARY_QUADRANTS = {
        5: "prim_up_right",
        6: "prim_up_left",
        7: "prim_low_left",
        8: "prim_low_right",
    }
    # (CHANGED) Tooth names now use language keys
    PERMANENT_TOOTH_NAMES = {
        1: "central_incisor",
        2: "lateral_incisor",
        3: "canine",
        4: "premolar_1",
        5: "premolar_2",
        6: "molar_1",
        7: "molar_2",
        8: "molar_3",
    }
    PRIMARY_TOOTH_NAMES = {
        1: "central_incisor",
        2: "lateral_incisor",
        3: "canine",
        4: "primary_molar_1",
        5: "primary_molar_2",
    }

    def __init__(self, chart_type='permanent'):
        self.teeth = {}
        self.chart_type = chart_type
        self._initialize_chart()

    def _get_tooth_name_keys(self, quadrant, tooth_index):
        # (CHANGED) This function now returns a tuple of (quadrant_key, tooth_key)
        if quadrant in self.PERMANENT_QUADRANTS:
            q_key = self.PERMANENT_QUADRANTS.get(quadrant, "unknown")
            t_key = self.PERMANENT_TOOTH_NAMES.get(tooth_index, "unknown")
            return (q_key, t_key)
        elif quadrant in self.PRIMARY_QUADRANTS:
            q_key = self.PRIMARY_QUADRANTS.get(quadrant, "unknown")
            t_key = self.PRIMARY_TOOTH_NAMES.get(tooth_index, "unknown")
            return (q_key, t_key)
        return ("unknown", "unknown")

    def _initialize_chart(self):
        self.teeth.clear()

        if self.chart_type == 'permanent':
            quadrants = [1, 2, 3, 4]
            teeth_indices = range(1, 9)
        elif self.chart_type == 'primary':
            quadrants = [5, 6, 7, 8]
            teeth_indices = range(1, 6)
        else:
            return

        for q in quadrants:
            for t in teeth_indices:
                fdi_number = (q * 10) + t
                # (CHANGED) Get name keys tuple
                name_keys = self._get_tooth_name_keys(q, t)
                self.teeth[fdi_number] = Tooth(fdi_number, name_keys)

    def get_tooth(self, fdi_number):
        return self.teeth.get(fdi_number)

    def update_status(self, fdi_number, new_status_key, notes=""):
        # (CHANGED) new_status is now a key (e.g., "caries")
        tooth = self.get_tooth(fdi_number)
        if tooth:
            tooth.status = new_status_key
            tooth.notes = notes

# (ថ្មី) Dialog សម្រាប់បន្ថែមការព្យាបាល
# (ថ្មី) Dialog សម្រាប់បន្ថែមការព្យាបាល
class AddTreatmentDialog(QDialog):
    def __init__(self, services_data, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle(self.tr("treat_add_title"))
        self.setWindowIcon(QIcon("Data/toothdoctor_diente_10727.ico"))
        self.setMinimumWidth(450)
        
        # --- (ថ្មី) បន្ថែម Variables សម្រាប់រក្សាតម្លៃដើម ---
        self.base_price_usd = 0.0
        self.base_price_khr = 0.0
        # --------------------------------------------------
        
        self.layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        self.service_category_combo = QComboBox()
        self.service_name_combo = QComboBox()
        
        self.tooth_num_edit = QLineEdit()
        
        # --- (ថ្មី) បន្ថែមช่อง "ចំនួន" ---
        self.quantity_edit = QLineEdit("1")
        # ----------------------------------
        
        self.cost_usd_edit = QLineEdit("0")
        self.cost_khr_edit = QLineEdit("0")
        self.notes_edit = QLineEdit()
        
        form_layout.addRow(self.tr("treat_category"), self.service_category_combo)
        form_layout.addRow(self.tr("treat_service"), self.service_name_combo)
        form_layout.addRow(self.tr("treat_tooth_num"), self.tooth_num_edit)
        
        # --- (ថ្មី) បន្ថែម Row សម្រាប់ "ចំនួន" ---
        form_layout.addRow(self.tr("treat_quantity"), self.quantity_edit)
        # ----------------------------------------
        
        form_layout.addRow(self.tr("treat_cost_usd"), self.cost_usd_edit)
        form_layout.addRow(self.tr("treat_cost_khr"), self.cost_khr_edit)
        form_layout.addRow(self.tr("treat_notes"), self.notes_edit)
        
        self.layout.addLayout(form_layout)
        
        # ប៊ូតុង
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton(self.tr("treat_add_button"))
        self.ok_button.setObjectName("success-button")
        self.cancel_button = QPushButton(self.tr("treat_cancel_button"))
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        
        self.layout.addLayout(button_layout)
        
        # ផ្ទុកទិន្នន័យ
        self.services_data = services_data
        self.service_category_combo.addItems(self.services_data.keys())
        
        # ភ្ជាប់ Signals
        self.service_category_combo.currentTextChanged.connect(self._on_category_changed)
        self.service_name_combo.currentTextChanged.connect(self._on_service_changed)
        
        # --- (ថ្មី) ភ្ជាប់ Signal របស់ "ចំនួន" ---
        self.quantity_edit.textChanged.connect(self._update_total_cost)
        # ---------------------------------------
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self._on_category_changed(self.service_category_combo.currentText()) # ផ្ទុកតម្លៃដំបូង

    def tr(self, key, **kwargs):
        """Helper to access the parent's translation function"""
        if self.parent_app:
            return self.parent_app.tr(key, **kwargs)
        return key

    def _on_category_changed(self, category_name):
        self.service_name_combo.clear()
        if category_name in self.services_data:
            self.service_name_combo.addItems(self.services_data[category_name].keys())

    def _on_service_changed(self, service_name):
        category_name = self.service_category_combo.currentText()
        if category_name in self.services_data and service_name in self.services_data[category_name]:
            prices = self.services_data[category_name][service_name]
            
            # --- (កែប្រែ) រក្សាតម្លៃដើម ជំនួសការកំណត់តម្លៃផ្ទាល់ ---
            try:
                self.base_price_usd = float(prices.get("usd", 0) or 0)
            except ValueError:
                self.base_price_usd = 0.0
            try:
                self.base_price_khr = float(prices.get("khr", 0) or 0)
            except ValueError:
                self.base_price_khr = 0.0
                
            # ហៅ Function គណនា
            self._update_total_cost()
            # ----------------------------------------------------

    # --- (ថ្មី) Function សម្រាប់គណនាតម្លៃសរុប ---
    def _update_total_cost(self):
        """Calculates the total cost based on base price and quantity."""
        try:
            quantity = float(self.quantity_edit.text() or 1)
        except ValueError:
            quantity = 1.0
            
        if quantity <= 0:
            quantity = 1.0
            
        total_usd = self.base_price_usd * quantity
        total_khr = self.base_price_khr * quantity
        
        # បង្ហាញលទ្ធផល
        self.cost_usd_edit.setText(f"{total_usd:.2f}")
        self.cost_khr_edit.setText(f"{total_khr:.0f}")
    # ---------------------------------------------

    def get_data(self):
        """ប្រគល់ទិន្នន័យដែលបានជ្រើសរើស"""
        return {
            "service_name": self.service_name_combo.currentText(),
            "tooth_num": self.tooth_num_edit.text(),
            "quantity": self.quantity_edit.text() or "1", # (ថ្មី)
            "cost_usd": self.cost_usd_edit.text() or "0",
            "cost_khr": self.cost_khr_edit.text() or "0",
            "notes": self.notes_edit.text()
        }

# (NEW) Dialog to show all patients in a table
class ViewAllPatientsDialog(QDialog):
    patient_selected = pyqtSignal(str)
    patient_deleted = pyqtSignal(str) # (ថ្មី) Signal សម្រាប់ប្រាប់ឲ្យលុប

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.all_data = data 
        
        self.setWindowTitle(self.tr("view_all_title"))
        self.setWindowIcon(QIcon("Data/toothdoctor_diente_10727.ico"))
        self.resize(1300, 850) 
        
        self.layout = QVBoxLayout(self)
        
        self._create_filter_bar()
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table, 1) 
        
        self._create_footer_bar()
        
        self._setup_table_headers()
        self._populate_table() 
        self._connect_signals()

    def tr(self, key, **kwargs):
        """Helper to access the parent's translation function"""
        if self.parent_app:
            return self.parent_app.tr(key, **kwargs)
        return key 

    def _create_filter_bar(self):
        """Creates the top filter and search bar"""
        filter_group = QGroupBox(self.tr("view_all_filters"))
        filter_layout = QHBoxLayout()
        
        self.search_bar_label = QLabel(self.tr("search_button")) 
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText(self.tr("search_placeholder")) 
        
        self.unpaid_check = QCheckBox(self.tr("view_all_unpaid_only"))
        
        filter_layout.addWidget(self.search_bar_label)
        filter_layout.addWidget(self.search_bar)
        filter_layout.addStretch()
        filter_layout.addWidget(self.unpaid_check)
        
        filter_group.setLayout(filter_layout)
        self.layout.addWidget(filter_group)

    def _create_footer_bar(self):
        """(កែប្រែ) Creates the bottom summary and action button bar"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        
        # (ថ្មី) Label សម្រាប់បង្ហាញប្រាក់ជំពាក់សរុប
        self.unpaid_summary_label = QLabel(self.tr("view_all_unpaid_loading"))
        self.unpaid_summary_label.setStyleSheet("font-weight: bold; color: #E74C3C;")
        
        # (ចាស់) Label សម្រាប់បង្ហាញចំនួនអ្នកជំងឺ
        self.summary_label = QLabel(self.tr("view_all_summary_loading"))
        self.summary_label.setStyleSheet("font-weight: bold; color: #2C3E50;")
        
        # (ថ្មី) ប៊ូតុង "ផ្ទុក" (Load)
        self.load_button = QPushButton(self.tr("view_all_load"))
        self.load_button.setObjectName("success-button")

        # (ថ្មី) ប៊ូតុង "លុប" (Delete)
        self.delete_button = QPushButton(self.tr("view_all_delete"))
        self.delete_button.setObjectName("danger-button")

        # (ចាស់) ប៊ូតុង "បិទ" (Close)
        self.close_button = QPushButton(self.tr("view_all_close"))
        self.close_button.setObjectName("info-button") 
        
        footer_layout.addWidget(self.unpaid_summary_label) # (ថ្មី)
        footer_layout.addStretch()
        footer_layout.addWidget(self.summary_label)
        footer_layout.addWidget(self.load_button) # (ថ្មី)
        footer_layout.addWidget(self.delete_button) # (ថ្មី)
        footer_layout.addWidget(self.close_button)
        
        self.layout.addWidget(footer_widget)

    def _connect_signals(self):
        """Connects the new filter widgets"""
        self.search_bar.textChanged.connect(self._on_filter_changed)
        self.unpaid_check.toggled.connect(self._on_filter_changed)
        
        # (ថ្មី) ភ្ជាប់ប៊ូតុង Treatment
        # --- FIX 1: REMOVED THESE TWO LINES (Buttons do not exist here) ---
        # self.add_treatment_button.clicked.connect(self._on_add_treatment)
        # self.remove_treatment_button.clicked.connect(self._on_remove_treatment)
        # -----------------------------------------------------------------
        
        # (កែប្រែ) ភ្ជាប់ប៊ូតុងថ្មី
        self.load_button.clicked.connect(self._on_load_selected_patient)
        self.delete_button.clicked.connect(self._on_delete_selected_patient)
        self.close_button.clicked.connect(self.accept) 

        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _setup_table_headers(self):
        """Sets up the table headers and base styles"""
        self.headers = [
            "info_id", "info_name", "info_phone", "info_age", 
            "info_address", "billing_total_usd", "billing_total_khr", 
            "billing_paid_check", "appt_group_title"
        ]
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels([self.tr(key) for key in self.headers])
        
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

    @pyqtSlot()
    def _on_filter_changed(self):
        """Slot to re-populate the table when any filter changes"""
        self._populate_table()

    def _populate_table(self):
        """
        (កែប្រែ) Filters data, populates table, and calculates unpaid totals.
        """
        if not self.all_data:
            return
            
        # (ថ្មី) Variables សម្រាប់គណនាបំណុល
        total_unpaid_usd_calc = 0.0
        total_unpaid_khr_calc = 0.0

        search_term = self.search_bar.text().lower().strip()
        unpaid_only = self.unpaid_check.isChecked()
        
        filtered_data = {}
        for patient_id, patient_data in self.all_data.items():
            if unpaid_only:
                is_paid = patient_data.get("is_paid", False)
                if is_paid: 
                    continue
            
            if search_term:
                name = patient_data.get("patient_name", "").lower()
                phone = patient_data.get("patient_phone", "").lower()
                id_str = str(patient_id).lower()
                
                if search_term not in name and search_term not in phone and search_term not in id_str:
                    continue 
            
            filtered_data[patient_id] = patient_data
        
        
        self.table.setSortingEnabled(False) 
        
        self.table.clearContents()
        self.table.setRowCount(len(filtered_data))
        
        for row, (patient_id, patient_data) in enumerate(filtered_data.items()):
            name = patient_data.get("patient_name", "")
            phone = patient_data.get("patient_phone", "")
            age = patient_data.get("patient_age", "")
            address = patient_data.get("patient_address", "")
            is_paid_bool = patient_data.get("is_paid", False)
            is_paid_text = self.tr("yes") if is_paid_bool else self.tr("no")
            
            # (កែប្រែ) គណនា total_usd_calc និង total_khr_calc
            if "treatments" in patient_data:
                total_usd_calc = sum(float(t.get("cost_usd", 0) or 0) for t in patient_data["treatments"])
                total_khr_calc = sum(float(t.get("cost_khr", 0) or 0) for t in patient_data["treatments"])
                total_usd = f"{total_usd_calc:,.2f}"
                total_khr = f"{total_khr_calc:,.0f}"
            else:
                total_usd = patient_data.get("total_amount_usd", "0")
                total_khr = patient_data.get("total_amount_khr", "0")
                # (ថ្មី) ត្រូវแปลง string ទៅ float សម្រាប់គណនា
                try:
                    total_usd_calc = float(total_usd.replace(",", "") or 0)
                except ValueError:
                    total_usd_calc = 0.0
                try:
                    total_khr_calc = float(total_khr.replace(",", "") or 0)
                except ValueError:
                    total_khr_calc = 0.0
            
            # (ថ្មី) បូកសរុបបំណុល
            if not is_paid_bool:
                total_unpaid_usd_calc += total_usd_calc
                total_unpaid_khr_calc += total_khr_calc

            
            appt_string = patient_data.get("next_appointment", "")
            appt_datetime = QDateTime.fromString(appt_string, Qt.ISODate)
            if appt_datetime.isValid():
                appt_display = appt_datetime.toString("dd/MM/yyyy hh:mm ap")
            else:
                appt_display = ""

            self.table.setItem(row, 0, QTableWidgetItem(patient_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(phone))
            self.table.setItem(row, 3, QTableWidgetItem(age))
            self.table.setItem(row, 4, QTableWidgetItem(address))
            
            usd_item = QTableWidgetItem(total_usd)
            khr_item = QTableWidgetItem(total_khr)
            usd_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            khr_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 5, usd_item)
            self.table.setItem(row, 6, khr_item)
            
            paid_item = QTableWidgetItem(is_paid_text)
            paid_item.setTextAlignment(Qt.AlignCenter)
            if is_paid_bool:
                paid_item.setForeground(QColor("#27AE60")) # Green
                paid_item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            else:
                paid_item.setForeground(QColor("#E74C3C")) # Red
                paid_item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.table.setItem(row, 7, paid_item)
            
            self.table.setItem(row, 8, QTableWidgetItem(appt_display))

        self.table.setSortingEnabled(True)
        
        # (កែប្រែ) Update summary labels ទាំងពីរ
        self.summary_label.setText(self.tr("view_all_summary",
                                            count=len(filtered_data),
                                            total=len(self.all_data)))
        
        unpaid_text = self.tr("view_all_unpaid_summary",
                                usd=f"{total_unpaid_usd_calc:,.2f}",
                                khr=f"{total_unpaid_khr_calc:,.0f}")
        self.unpaid_summary_label.setText(unpaid_text)
                                        
    @pyqtSlot(QTableWidgetItem)
    def _on_item_double_clicked(self, item):
        """(NEW) Emits the patient ID and closes the dialog"""
        if item is None:
            return
            
        row = item.row()
        id_item = self.table.item(row, 0)
        
        if id_item:
            patient_id = id_item.text()
            self.patient_selected.emit(patient_id)
            self.accept()

    # --- (ថ្មី) SLOTS សម្រាប់ប៊ូតុងថ្មី ---

    @pyqtSlot()
    def _on_load_selected_patient(self):
        """ផ្ទុកអ្នកជំងឺដែលបានជ្រើសរើស (triggered by load button)"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, self.tr("view_all_select_title"),
                                      self.tr("view_all_select_load_msg"))
            return
        
        # យក item ណាមួយក្នុងជួរដេកដែលបានជ្រើសរើស
        self._on_item_double_clicked(selected_items[0])

    @pyqtSlot()
    def _on_delete_selected_patient(self):
        """លុបអ្នកជំងឺដែលបានជ្រើសរើស (triggered by delete button)"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, self.tr("view_all_select_title"),
                                      self.tr("view_all_select_del_msg"))
            return

        # យក ID និង ឈ្មោះ ពីជួរដេក
        row = selected_items[0].row()
        id_item = self.table.item(row, 0)
        name_item = self.table.item(row, 1)

        if not id_item or not name_item:
            return # មិនគួរកើតឡើងទេ

        patient_id = id_item.text()
        patient_name = name_item.text()

        # សួរការបញ្ជាក់
        reply = QMessageBox.warning(self, self.tr("delete_confirm_title"),
                                      self.tr("delete_confirm_msg", patient_name=patient_name, patient_id=patient_id),
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # 1. លុបចេញពី data cache បច្ចុប្បន្ន
                if patient_id in self.all_data:
                    del self.all_data[patient_id]
                
                # 2. បញ្ជូន Signal ទៅ Main Window ឲ្យលុបចេញពី database
                self.patient_deleted.emit(patient_id)
                
                # 3. ធ្វើបច្ចុប្បន្នភាពតារាង (UI) ឡើងវិញ
                self._populate_table()

            except Exception as e:
                QMessageBox.critical(self, self.tr("delete_fail_title"),
                                           self.tr("delete_fail_msg", e=e))
                

# Enhanced GUI Application
class DentalChartApp(QMainWindow):
    # (CHANGED) STATUS_COLORS now uses the language-neutral keys
    STATUS_COLORS = {
    "present": "#FFFFFF",           # បៃតងចាស់
    "missing": "#566573",           # ប្រផេះចាស់
    "missing_extracted": "#34495E", # ប្រផេះ-ខៀវចាស់
    "missing_unerupted": "#2C3E50", # ប្រផេះ-ខៀវ (ដិតជាងគេ)
    "to_be_extracted": "#D35400",   # ទឹកក្រូចចាស់
    "caries": "#C0392B",            # ក្រហមចាស់ (ពុក)
    "fractured": "#873600",         # ពណ៌ត្នោតចាស់
    "filling": "#2980B9",           # ខៀវចាស់ (បក)
    "crown": "#2471A3",             # ខៀវ (ស្រោប)
    "metal": "#1C1D1A",
    "ssc": "#5BA3F0",               # ប្រផេះ (ដែក)
    "veneer": "#B7950B",            # លឿងចាស់ (មាស)
    "sealant": "#B03A2E",           # ក្រហម-ផ្កាឈូកចាស់
    "implant": "#16A085",           # បៃតង-ខៀវ (Teal)
    "root_canal": "#8E44AD",        # ពណ៌ស្វាយចាស់
}
    
    # (CHANGED) STATUS_LIST now points to the keys from translations.py
    STATUS_LIST = STATUS_LIST_KEYS

    def __init__(self):
        super().__init__()
        
        # (NEW) Translation setup
        self.translations = LANG_STRINGS
        self.current_lang = "kh" # Default language
        
        self.chart = DentalChart(chart_type='permanent')
        self.tooth_buttons = {}
        self.current_selected_tooth_num = None
        self.found_files = {}
        self.database_file = "clinic_database.json"
        self.master_patient_list = {}
        self.current_payments_list = []
        self.address_list = [] 

        # (ថ្មី) បន្ថែម Variables សម្រាប់ Treatment
        self.services_file = "services.json"
        self.services_data = {} # នឹងផ្ទុកទិន្នន័យពី services.json
        self.current_treatments_list = [] # បញ្ជី Treatment សម្រាប់អ្នកជំងឺបច្ចុប្បន្ន

        # (NEW) List to hold image paths for the current patient
        self.current_image_list = []

        # (CHANGED) Set title using tr() function
        self.setWindowTitle(self.tr("window_title"))
        self.setGeometry(100, 100, 1400, 870)
        self.setWindowIcon(QIcon("Data/toothdoctor_diente_10727.ico"))

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        
        self._load_master_database()
        self._load_addresses()

        self._load_services() 

        # Create the new enhanced UI
        self._create_header()
        self._create_main_content()
        self._create_footer()

        # Connect signals
        self._connect_signals()

        self._build_chart_grid()
        self._update_details_panel(None)

        # --- (កែប្រែ) បង្កើត ID ស្វ័យប្រវត្តិ នៅពេលបើកកម្មវិធី ---
        self.patient_id_edit.setText(self._get_next_patient_id())
        
        # (NEW) Call the stats updater after loading the database
        self._update_header_stats()
        # ពិនិត្យមើលការណាត់ជួបថ្ងៃនេះ ពេលបើកកម្មវិធី
        self._check_today_appointments() 
        # --- (ចប់ការបន្ថែម) ---

    # (NEW) Translation function
    def tr(self, key, **kwargs):
        """
        Translate a given key into the current language.
        Defaults to the key itself if not found.
        """
        # Get the dictionary for the current language, default to 'en'
        lang_dict = self.translations.get(self.current_lang, self.translations["en"])
        # Get the translated string, default to the key
        text = lang_dict.get(key, key)
        
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass # Ignore formatting errors if kwargs don't match
        return text

    def _connect_signals(self):
        """Connect all signals to their slots"""
        # (NEW) Language selector
        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)
        
        # Chart type - FIXED: Use idClicked signal instead of buttonClicked
        self.chart_type_group.idClicked.connect(self._on_chart_type_changed)
        
        # Tooth details
        self.details_save_button.clicked.connect(self._on_save_details)
        
        # Search
        
        # Payments
        self.add_payment_button.clicked.connect(self._on_add_payment)
        
        # --- FIX 2: REMOVED these two lines. Calculation is triggered by _recalculate_totals_from_treatments ---
        # self.total_amount_usd_edit.textChanged.connect(self._calculate_remaining_amount)
        # self.total_amount_khr_edit.textChanged.connect(self._calculate_remaining_amount)
        # -----------------------------------------------------------------------------------------------------
        
        # Main actions
        self.save_button.clicked.connect(self._on_save_chart)
        self.clear_button.clicked.connect(self._on_clear_chart)
        self.report_button.clicked.connect(self._on_show_income_report)
        self.viewall_button.clicked.connect(self._viewall_button)

        # --- (NEW) ភ្ជាប់ប៊ូតុង Print ---
        self.print_button.clicked.connect(self._on_print_patient)
        # -----------------------------
        
        # --- (NEW) Connections for new footer buttons ---
        self.delete_patient_button.clicked.connect(self._on_delete_patient)
        self.appointments_button.clicked.connect(self._on_view_appointments)
        self.backup_button.clicked.connect(self._on_backup_database)
        self.restore_button.clicked.connect(self._on_restore_database)
        # --------------------------------------------------
        
        # --- (NEW) Connections for treatment tab ---
        self.add_treatment_button.clicked.connect(self._on_add_treatment)
        self.remove_treatment_button.clicked.connect(self._on_remove_treatment)
        # -------------------------------------------

    def _create_header(self):
        """Creates the application header with clinic info"""
        header_widget = QWidget()
        header_widget.setObjectName("header")
        header_widget.setStyleSheet("""
            #header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498DB, stop:1 #2C3E50);
                border-radius: 10px;
                margin: 5px;
            }
        """)
        header_layout = QHBoxLayout(header_widget)
        
        # Clinic info
        clinic_info = QVBoxLayout()
        # (CHANGED) Use tr() for title
        self.clinic_title_label = QLabel(self.tr("clinic_title"))
        self.clinic_title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 25pt; 
                font-weight: bold;
                padding: 10px;
            }
        """)
        clinic_info.addWidget(self.clinic_title_label)
        
        # Quick stats
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        # (CHANGED) Store stat cards to update them
        self.stat_total = self._create_stat_card(self.tr("total_patients"), f"{len(self.master_patient_list)}")
        self.stat_today = self._create_stat_card(self.tr("today_patients"), "0")
        self.stat_month = self._create_stat_card(self.tr("month_patients"), "0")
        
        stats_layout.addWidget(self.stat_total)
        stats_layout.addWidget(self.stat_today)
        stats_layout.addWidget(self.stat_month)
        
        # (NEW) Language Selector
        lang_widget = QWidget()
        lang_layout = QHBoxLayout(lang_widget)
        self.lang_label = QLabel(self.tr("lang_label"))
        #self.lang_label.setStyleSheet("color: white; font-weight: bold;")

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["ខ្មែរ", "English"])
        self.lang_combo.setStyleSheet("color: black;")
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        
        
        header_layout.addLayout(clinic_info)
        header_layout.addStretch()
        header_layout.addWidget(stats_widget)
        header_layout.addWidget(lang_widget) # Add lang selector
        
        self.main_layout.addWidget(header_widget)

    def _create_stat_card(self, title, value):
        """Creates a statistic card for the header"""
        card = QWidget()
        card.setFixedSize(100, 60)
        card.setStyleSheet("background-color: #2980B9; border-radius: 8px;")
        layout = QVBoxLayout(card)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: white; font-size: 12pt; font-weight: bold;") 
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #E8F6F3; font-size: 9pt;") 
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        # (NEW) Store labels for retranslation
        card.title_label = title_label
        card.value_label = value_label
        
        return card

    def _create_main_content(self):
        """Creates the main content area with splitter"""
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Patient Management
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Dental Chart
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Configure splitter
        main_splitter.setStretchFactor(0, 0)
        main_splitter.setStretchFactor(1, 1)
        main_splitter.setSizes([550, 1000])
        
        self.main_layout.addWidget(main_splitter, 1)

    def _get_next_patient_id(self):
        """Finds the highest existing patient ID and returns the next one."""
        max_id = 0
        if not self.master_patient_list:
            return "0001"
            
        for id_str in self.master_patient_list.keys():
            try:
                id_num = int(id_str)
                if id_num > max_id:
                    max_id = id_num
            except ValueError:
                # Ignore any non-numeric IDs
                pass
                
        next_id = max_id + 1
        return f"{next_id:04d}" # Format as 4 digits, e.g., 0001, 0012, 0123

    def _create_left_panel(self):
        """Creates the left panel with patient management"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        
        # Patient information tabs
        self.patient_tabs = QTabWidget()
        # (CHANGED) Use tr()
        self.patient_tabs.addTab(self._create_patient_info_tab(), self.tr("tab_info"))
        self.patient_tabs.addTab(self._create_treatment_tab(), self.tr("tab_treatment"))
        self.patient_tabs.addTab(self._create_billing_tab(), self.tr("tab_billing"))
        self.patient_tabs.addTab(self._create_appointment_tab(), self.tr("tab_appointment"))
        

        # (NEW) Add the Images Tab
        self.patient_tabs.addTab(self._create_images_tab(), self.tr("tab_images"))
        
        left_layout.addWidget(self.patient_tabs)
        
        return left_widget
    
    def _create_treatment_tab(self):
        """(ថ្មី) Creates the treatment/services tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.treatment_group = QGroupBox(self.tr("treat_group_title"))
        group_layout = QVBoxLayout(self.treatment_group)

        # តារាងសម្រាប់បង្ហាញ Treatment
        self.treatment_table = QTableWidget()
        self.treatment_table.setColumnCount(6) # (កែប្រែ) បន្ថែម Column សម្រាប់ Date
        self.treatment_table.setHorizontalHeaderLabels([
            self.tr("treat_col_date"), # (ថ្មី)
            self.tr("treat_col_service"),
            self.tr("treat_col_tooth"),
            self.tr("treat_col_cost_usd"),
            self.tr("treat_col_cost_khr"),
            self.tr("treat_col_notes")
        ])
        self.treatment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.treatment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.treatment_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.treatment_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.treatment_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) # Date
        self.treatment_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents) # Tooth
        self.treatment_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) # USD
        self.treatment_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents) # KHR

        group_layout.addWidget(self.treatment_table)

        # ប៊ូតុង
        button_layout = QHBoxLayout()
        self.add_treatment_button = QPushButton(self.tr("treat_add_button"))
        self.add_treatment_button.setObjectName("success-button")

        self.remove_treatment_button = QPushButton(self.tr("treat_remove_button"))
        self.remove_treatment_button.setObjectName("danger-button")

        button_layout.addStretch()
        button_layout.addWidget(self.remove_treatment_button)
        button_layout.addWidget(self.add_treatment_button)

        group_layout.addLayout(button_layout)
        layout.addWidget(self.treatment_group)
        return widget

    def _create_right_panel(self):
        """Creates the right panel with dental chart"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Chart controls
        controls_card = QWidget()
        controls_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E9ECEF; border-radius: 8px; padding: 15px; margin: 5px;")
        controls_layout = QHBoxLayout(controls_card)
        
        # (CHANGED) Use tr()
        self.chart_title_label = QLabel(self.tr("chart_title"))
        self.chart_title_label.setStyleSheet("font-weight: bold; color: #3498DB; font-size: 11pt; margin: 5px 0px;") 
        
        # Chart type selector
        chart_type_widget = QWidget()
        chart_type_layout = QHBoxLayout(chart_type_widget)
        # (CHANGED) Use tr()
        self.chart_type_label = QLabel(self.tr("chart_type_label"))
        chart_type_layout.addWidget(self.chart_type_label)
        
        # (CHANGED) Use tr()
        self.perm_radio = QRadioButton(self.tr("chart_perm"))
        self.prim_radio = QRadioButton(self.tr("chart_prim"))
        self.perm_radio.setChecked(True)
        
        self.chart_type_group = QButtonGroup()
        self.chart_type_group.addButton(self.perm_radio, 1)
        self.chart_type_group.addButton(self.prim_radio, 2)
        
        chart_type_layout.addWidget(self.perm_radio)
        chart_type_layout.addWidget(self.prim_radio)
        chart_type_layout.addStretch()
        
        controls_layout.addWidget(self.chart_title_label)
        controls_layout.addStretch()
        controls_layout.addWidget(chart_type_widget)
        
        # Dental chart
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        
        # Upper jaw
        # (CHANGED) Use tr()
        self.upper_jaw_group = QGroupBox(self.tr("upper_jaw"))
        self.upper_jaw_layout = QGridLayout()
        self.upper_jaw_group.setLayout(self.upper_jaw_layout)
        
        # Lower jaw
        # (CHANGED) Use tr()
        self.lower_jaw_group = QGroupBox(self.tr("lower_jaw"))
        self.lower_jaw_layout = QGridLayout()
        self.lower_jaw_group.setLayout(self.lower_jaw_layout)
        
        chart_layout.addWidget(self.upper_jaw_group)
        chart_layout.addWidget(self.lower_jaw_group)
        
        # Tooth details
        self.tooth_details_card = self._create_tooth_details_card()
        
        right_layout.addWidget(controls_card)
        right_layout.addWidget(chart_container, 1)
        right_layout.addWidget(self.tooth_details_card)
        
        return right_widget

    def _create_patient_info_tab(self):
        """Creates the patient information tab"""
        # 1. Create the main widget for the tab
        widget = QWidget()
        
        # 2. Create the main vertical layout for the tab
        main_layout = QVBoxLayout(widget)

        # 3. Create a GroupBox to hold the form (this is the container)
        # (CHANGED) Use tr()
        self.form_group = QGroupBox(self.tr("info_group_title"))
        
        # 4. Create the FormLayout and assign it to the GroupBox
        layout = QFormLayout(self.form_group)
        
        # --- All your original widgets are created here ---
        self.patient_name_edit = QLineEdit()
        self.patient_id_edit = QLineEdit()
        
        # --- (កែប្រែ) ធ្វើឲ្យ ID កែមិនបាន (Read-only) ---
        self.patient_id_edit.setReadOnly(True)
        # -----------------------------------------------

        # (CHANGED) Use tr()
        self.patient_id_edit.setPlaceholderText(self.tr("info_id_placeholder"))
        self.patient_phone_edit = QLineEdit()
        
        # --- (កែប្រែ) ជំនួស ថ្ងៃខែឆ្នាំកំណើត ដោយ អាយុ ---
        self.patient_age_edit = QLineEdit()
        # (CHANGED) Use tr()
        self.patient_age_edit.setPlaceholderText(self.tr("info_age_placeholder"))
        # -----------------------------------------
        
        # ---  widget ថ្មីសម្រាប់អាសយដ្ឋាន ---
        self.patient_address_combo = QComboBox()
        self.patient_address_combo.setEditable(True) # អនុញ្ញាតឲ្យវាយបញ្ចូលថ្មី
        self.patient_address_combo.addItems(self.address_list) # បញ្ចូលទិន្នន័យពី address_list
        # --- ចប់ widget ថ្មី ---
        
        # --- (កែប្រែ) បន្ថែម background-color សម្រាប់ช่อง ID ---
        self.patient_id_edit.setStyleSheet("border: 2px solid #3498DB; background-color: #F4F6F6;")
        
        # (CHANGED) Use tr() for labels
        self.info_id_label = QLabel(self.tr("info_id"))
        self.info_name_label = QLabel(self.tr("info_name"))
        self.info_phone_label = QLabel(self.tr("info_phone"))
        self.info_age_label = QLabel(self.tr("info_age"))
        self.info_address_label = QLabel(self.tr("info_address"))

        # --- Add rows to the FormLayout ---
        layout.addRow(self.info_id_label, self.patient_id_edit)
        layout.addRow(self.info_name_label, self.patient_name_edit)
        
        layout.addRow(self.info_phone_label, self.patient_phone_edit)
        
        # --- (កែប្រែ) ប្តូរ Label និង Widget ---
        layout.addRow(self.info_age_label, self.patient_age_edit)
        # ---------------------------------
        
        layout.addRow(self.info_address_label, self.patient_address_combo) # <--- បន្ថែម
        
        # --- (NEW) General Notes Field ---
        self.info_notes_label = QLabel(self.tr("info_general_notes"))
        self.patient_notes_edit = QTextEdit()
        self.patient_notes_edit.setFixedHeight(70)
        self.patient_notes_edit.setPlaceholderText(self.tr("info_general_notes_ph"))
        layout.addRow(self.info_notes_label, self.patient_notes_edit)
        # ---------------------------------
        
        # 5. Add the GroupBox (which contains the form) to the main layout
        main_layout.addWidget(self.form_group)
        
        # 6. Add the stretch to push the form to the top
        main_layout.addStretch()
        
        return widget
    
    def _load_services(self):
        """(ថ្មី) ផ្ទុកបញ្ជីសេវាកម្មពី services.json"""
        try:
            if os.path.exists(self.services_file):
                with open(self.services_file, 'r', encoding='utf-8') as f:
                    self.services_data = json.load(f)
            else:
                QMessageBox.warning(self, "File Not Found", f"មិនអាចរកឃើញឯកសារ {self.services_file} បានទេ។")
                self.services_data = {}
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Services", f"Error: {e}")
            self.services_data = {}

    @pyqtSlot()
    def _on_add_treatment(self):
        """(ថ្មី) បង្ហាញ Dialog ដើម្បីបន្ថែម Treatment"""
        dialog = AddTreatmentDialog(self.services_data, self)
        
        # (ថ្មី) ព្យាយាមយកលេខធ្មេញដែលបានជ្រើសរើស
        if self.current_selected_tooth_num:
            dialog.tooth_num_edit.setText(str(self.current_selected_tooth_num))
            
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            # (ថ្មី) បន្ថែមថ្ងៃខែបច្ចុប្បន្ន
            data["date"] = QDate.currentDate().toString(Qt.ISODate)
            
            self.current_treatments_list.append(data)
            self._update_treatment_table_ui()
            self._recalculate_totals_from_treatments()

    @pyqtSlot()
    def _on_remove_treatment(self):
        """(ថ្មី) លុប Treatment ដែលបានជ្រើសរើសចេញពីតារាង"""
        selected_row = self.treatment_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, self.tr("treat_remove_warn_title"), self.tr("treat_remove_warn_msg"))
            return
            
        # យក item ចេញពី list
        del self.current_treatments_list[selected_row]
        
        # ធ្វើបច្ចុប្បន្នភាព UI
        self._update_treatment_table_ui()
        self._recalculate_totals_from_treatments()

    def _update_treatment_table_ui(self):
        """(ថ្មី) ធ្វើបច្ចុប្បន្នភាពតារាង Treatment ពី self.current_treatments_list"""
        self.treatment_table.setRowCount(0) # សម្អាតតារាង
        
        for row, item in enumerate(self.current_treatments_list):
            self.treatment_table.insertRow(row)
            
            # (ថ្មី) បង្ហាញថ្ងៃខែ
            date_str = item.get("date", QDate.currentDate().toString(Qt.ISODate))
            date_item = QTableWidgetItem(QDate.fromString(date_str, Qt.ISODate).toString("dd/MM/yyyy"))
            
            service_item = QTableWidgetItem(item.get("service_name", "N/A"))
            tooth_item = QTableWidgetItem(item.get("tooth_num", ""))
            
            # ធ្វើឲ្យតួលេខតម្រឹមស្តាំ
            try:
                cost_usd_val = float(item.get("cost_usd", 0) or 0)
            except ValueError:
                cost_usd_val = 0.0
            try:
                cost_khr_val = float(item.get("cost_khr", 0) or 0)
            except ValueError:
                cost_khr_val = 0.0
                
            cost_usd_item = QTableWidgetItem(f"{cost_usd_val:,.2f}")
            cost_khr_item = QTableWidgetItem(f"{cost_khr_val:,.0f}")
            cost_usd_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            cost_khr_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            notes_item = QTableWidgetItem(item.get("notes", ""))
            
            self.treatment_table.setItem(row, 0, date_item) # (ថ្មី)
            self.treatment_table.setItem(row, 1, service_item)
            self.treatment_table.setItem(row, 2, tooth_item)
            self.treatment_table.setItem(row, 3, cost_usd_item)
            self.treatment_table.setItem(row, 4, cost_khr_item)
            self.treatment_table.setItem(row, 5, notes_item)
            
    def _recalculate_totals_from_treatments(self):
        """(ថ្មី) បូកសរុបតម្លៃពីតារាង Treatment ហើយ Update ផ្ទាំង Billing"""
        total_usd = 0.0
        total_khr = 0.0
        
        for item in self.current_treatments_list:
            try:
                total_usd += float(item.get("cost_usd", 0) or 0)
            except ValueError:
                pass # រំលងបើវាយខុស
            try:
                total_khr += float(item.get("cost_khr", 0) or 0)
            except ValueError:
                pass # រំលងបើវាយខុស

        # Update ផ្ទាំង Billing
        self.total_amount_usd_edit.setText(f"{total_usd:,.2f}")
        self.total_amount_khr_edit.setText(f"{total_khr:,.0f}")
        
        # ត្រូវហៅ function នេះឡើងវិញ ដើម្បីគណនាប្រាក់នៅសល់
        self._calculate_remaining_amount()

    def _create_billing_tab(self):
        """Creates the billing information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Amount section
        # (CHANGED) Use tr()
        self.amount_group = QGroupBox(self.tr("billing_amount_group"))
        amount_layout = QFormLayout(self.amount_group)
        
        total_widget = QWidget()
        total_layout = QGridLayout(total_widget)
        # (CHANGED) Use tr()
        self.billing_usd_label1 = QLabel(self.tr("billing_usd"))
        self.billing_khr_label1 = QLabel(self.tr("billing_khr"))
        total_layout.addWidget(self.billing_usd_label1, 0, 1, Qt.AlignCenter)
        total_layout.addWidget(self.billing_khr_label1, 0, 2, Qt.AlignCenter)
        
        self.total_amount_usd_edit = QLineEdit("0")
        self.total_amount_khr_edit = QLineEdit("0")
        # (CHANGED) Use tr()
        self.total_amount_usd_edit.setReadOnly(True)
        self.total_amount_khr_edit.setReadOnly(True)
        self.total_amount_usd_edit.setStyleSheet("background-color: #F4F6F6;")
        self.total_amount_khr_edit.setStyleSheet("background-color: #F4F6F6;")

        self.billing_total_label = QLabel(self.tr("billing_total"))
        total_layout.addWidget(self.billing_total_label, 1, 0)
        total_layout.addWidget(self.total_amount_usd_edit, 1, 1)
        total_layout.addWidget(self.total_amount_khr_edit, 1, 2)
        
        amount_layout.addRow(total_widget)
        
        # New payment
        # (CHANGED) Use tr()
        self.payment_group = QGroupBox(self.tr("billing_new_payment_group"))
        payment_layout = QFormLayout(self.payment_group)

        # Payment history
        # (CHANGED) Use tr()
        self.history_group = QGroupBox(self.tr("billing_payment_history_group"))
        history_layout = QVBoxLayout(self.history_group)
        self.payment_history_list = QListWidget()
        self.payment_history_list.setFixedHeight(60)
        history_layout.addWidget(self.payment_history_list)
        
        new_payment_widget = QWidget()
        new_payment_layout = QGridLayout(new_payment_widget)
        self.new_payment_usd_edit = QLineEdit("0")
        self.new_payment_khr_edit = QLineEdit("0")
        # (CHANGED) Use tr()
        self.billing_usd_label2 = QLabel(self.tr("billing_usd"))
        self.billing_khr_label2 = QLabel(self.tr("billing_khr"))
        self.billing_payment_label = QLabel(self.tr("billing_payment"))
        new_payment_layout.addWidget(self.billing_usd_label2, 0, 1, Qt.AlignCenter)
        new_payment_layout.addWidget(self.billing_khr_label2, 0, 2, Qt.AlignCenter)
        new_payment_layout.addWidget(self.billing_payment_label, 1, 0)
        new_payment_layout.addWidget(self.new_payment_usd_edit, 1, 1)
        new_payment_layout.addWidget(self.new_payment_khr_edit, 1, 2)
        
        # (CHANGED) Use tr()
        self.add_payment_button = QPushButton(self.tr("billing_add_payment_button"))
        self.add_payment_button.setObjectName("success-button")
        
        payment_layout.addRow(new_payment_widget)
        payment_layout.addRow(self.add_payment_button)
        
        # Remaining amount
        remaining_card = QWidget()
        remaining_card.setStyleSheet("background-color: #E8F6F3; border-radius: 8px; padding: 10px;")
        remaining_layout = QGridLayout(remaining_card)
        
        self.remaining_usd_label = QLabel("0.00 $")
        self.remaining_khr_label = QLabel("0 ៛")
        self.remaining_usd_label.setAlignment(Qt.AlignCenter)
        self.remaining_khr_label.setAlignment(Qt.AlignCenter)
        self.remaining_usd_label.setStyleSheet("font-weight: bold; color: #27AE60; font-size: 10pt;") 
        self.remaining_khr_label.setStyleSheet("font-weight: bold; color: #27AE60; font-size: 10pt;") 
        
        # (CHANGED) Use tr()
        self.billing_remaining_label = QLabel(self.tr("billing_remaining_label"))
        remaining_layout.addWidget(self.billing_remaining_label, 0, 0)
        remaining_layout.addWidget(self.remaining_usd_label, 0, 1)
        remaining_layout.addWidget(self.remaining_khr_label, 0, 2)
        
        # (CHANGED) Use tr()
        self.paid_check = QCheckBox(self.tr("billing_paid_check"))
        
        layout.addWidget(self.amount_group)
        layout.addWidget(self.payment_group)
        layout.addWidget(self.history_group)
        
        layout.addWidget(remaining_card)
        layout.addWidget(self.paid_check)
        layout.addStretch()
        
        return widget

    def _create_appointment_tab(self):
        """Creates the appointment tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        appointment_card = QWidget()
        appointment_card.setStyleSheet("background-color: #FEF9E7; border-radius: 8px; padding: 15px;")
        card_layout = QVBoxLayout(appointment_card)
        
        # (CHANGED) Use tr()
        self.appt_title_label = QLabel(self.tr("appt_group_title"))
        self.appt_title_label.setStyleSheet("font-weight: bold; color: #D35400; font-size: 10pt;") 
        
        self.appointment_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.appointment_edit.setCalendarPopup(True)
        self.appointment_edit.setDisplayFormat("dd/MM/yyyy hh:mm ap")
        
        card_layout.addWidget(self.appt_title_label)
        card_layout.addWidget(self.appointment_edit)
        
        layout.addWidget(appointment_card)
        layout.addStretch()
        
        return widget

    # (NEW) Method to create the new Images tab
    def _create_images_tab(self):
        """Creates the new patient images/x-ray tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.images_group = QGroupBox(self.tr("images_group_title"))
        group_layout = QVBoxLayout(self.images_group)

        # List widget
        self.image_list_widget = QListWidget()
        self.image_list_widget.setAlternatingRowColors(True)

        # Button layout
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.add_image_button = QPushButton(self.tr("images_add_button"))
        self.add_image_button.setObjectName("success-button")
        
        self.view_image_button = QPushButton(self.tr("images_view_button"))
        self.view_image_button.setObjectName("info-button")
        
        self.remove_image_button = QPushButton(self.tr("images_remove_button"))
        self.remove_image_button.setObjectName("danger-button")

        button_layout.addWidget(self.add_image_button)
        button_layout.addWidget(self.view_image_button)
        button_layout.addStretch()
        button_layout.addWidget(self.remove_image_button)

        group_layout.addWidget(self.image_list_widget, 1) # Add stretch
        group_layout.addWidget(button_widget)

        layout.addWidget(self.images_group)
        
        # Connect signals
        self.add_image_button.clicked.connect(self._on_add_image_link)
        self.view_image_button.clicked.connect(self._on_view_image_link)
        self.remove_image_button.clicked.connect(self._on_remove_image_link)
        self.image_list_widget.itemDoubleClicked.connect(self._on_view_image_link)

        return widget

    def _create_tooth_details_card(self):
        """Creates the tooth details card"""
        # (CHANGED) Use tr()
        card = QGroupBox(self.tr("details_group_title"))
        layout = QGridLayout(card)

        # (CHANGED) Use tr()
        self.details_tooth_label = QLabel(self.tr("details_tooth"))
        layout.addWidget(self.details_tooth_label, 0, 0)
        self.details_name_label = QLabel(self.tr("details_tooth_unselected"))
        self.details_name_label.setWordWrap(True)
        self.details_name_label.setStyleSheet("font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.details_name_label, 0, 1, 1, 3)

        # (CHANGED) Use tr()
        self.details_status_label = QLabel(self.tr("details_status"))
        layout.addWidget(self.details_status_label, 1, 0)
        self.details_status_combo = QComboBox()
        # (CHANGED) Populate dropdown by translating keys
        self.details_status_combo.addItems([self.tr(key) for key in self.STATUS_LIST])
        layout.addWidget(self.details_status_combo, 1, 1, 1, 3)

        # (CHANGED) Use tr()
        self.details_notes_label = QLabel(self.tr("details_notes"))
        layout.addWidget(self.details_notes_label, 2, 0, Qt.AlignTop)
        self.details_notes_edit = QTextEdit()
        self.details_notes_edit.setFixedHeight(80)
        layout.addWidget(self.details_notes_edit, 2, 1, 1, 3)

        # (CHANGED) Use tr()
        self.details_save_button = QPushButton(self.tr("details_save_button"))
        self.details_save_button.setObjectName("success-button")
        layout.addWidget(self.details_save_button, 3, 1, 1, 3)
        
        return card

    def _create_footer(self):
        """Creates the footer with action buttons"""
        footer_widget = QWidget()
        footer_widget.setStyleSheet("background-color: #2C3E50; border-radius: 8px; margin: 5px;")
        footer_layout = QHBoxLayout(footer_widget)
        # Left side buttons
        left_buttons = QHBoxLayout()
         # (CHANGED) Use tr()
        self.save_button = QPushButton(self.tr("footer_save"))
        self.save_button.setObjectName("success-button")
        self.clear_button = QPushButton(self.tr("footer_clear"))
        self.clear_button.setObjectName("warning-button") # (CHANGED)

        # (NEW) Delete Button
        self.delete_patient_button = QPushButton(self.tr("footer_delete"))
        self.delete_patient_button.setObjectName("danger-button")

        self.viewall_button = QPushButton(self.tr("viewall_button"))
        #self.viewall_button.setObjectName("danger-button") # (REMOVED) - uses default

        # --- (NEW) ប៊ូតុង Print ថ្មី ---
        self.print_button = QPushButton(self.tr("footer_print"))
        self.print_button.setObjectName("info-button") # ប្រើពណ៌ខៀវ 'info'
        # --------------------------------

        left_buttons.addWidget(self.save_button)
        left_buttons.addWidget(self.clear_button)
        left_buttons.addWidget(self.delete_patient_button) # (NEW)
        left_buttons.addWidget(self.viewall_button) 
        left_buttons.addWidget(self.print_button) # <--- បន្ថែមប៊ូតុងថ្មីទៅ layout
         # Right side buttons
        right_buttons = QHBoxLayout()
        
        # (NEW) New action buttons
        self.appointments_button = QPushButton(self.tr("footer_appts"))
        self.appointments_button.setObjectName("info-button")
        self.backup_button = QPushButton(self.tr("footer_backup"))
        self.backup_button.setObjectName("success-button")
        self.restore_button = QPushButton(self.tr("footer_restore"))
        self.restore_button.setObjectName("warning-button")
        
        self.report_button = QPushButton(self.tr("footer_report"))
        self.report_button.setObjectName("info-button")
        
        right_buttons.addWidget(self.appointments_button) # (NEW)
        right_buttons.addWidget(self.report_button)
        right_buttons.addWidget(self.backup_button) # (NEW)
        right_buttons.addWidget(self.restore_button) # (NEW)
        
        footer_layout.addLayout(left_buttons)
        footer_layout.addStretch()
        footer_layout.addLayout(right_buttons)
        self.main_layout.addWidget(footer_widget)

    def _build_chart_grid(self):
        """Clears and rebuilds the tooth buttons in the grid layouts."""
        self._clear_layout(self.upper_jaw_layout)
        self._clear_layout(self.lower_jaw_layout)
        self.tooth_buttons.clear()

        # Add midline labels
        midline_upper = QLabel("|")
        midline_lower = QLabel("|")
        midline_upper.setAlignment(Qt.AlignCenter)
        midline_lower.setAlignment(Qt.AlignCenter)
        midline_upper.setStyleSheet("font-weight: bold; color: #f7005b; font-size: 14pt;")
        midline_lower.setStyleSheet("font-weight: bold; color: #f7005b; font-size: 14pt;")
        self.upper_jaw_layout.addWidget(midline_upper, 1, 8)
        self.lower_jaw_layout.addWidget(midline_lower, 1, 8)

        

        if self.chart.chart_type == 'permanent':
            # Upper Jaw (Permanent)
            
            # Quadrant 1 (Upper Right on GUI)
            for i in range(8):
                fdi = 21 + i  # <-- FIX: Generates 21, 22, 23...28
                self._add_tooth_button(fdi, self.upper_jaw_layout, 1, i + 9)

            # Quadrant 2 (Upper Left on GUI)
            for i in range(8):
                fdi = 18 - i  # <-- FIX: Generates 18, 17, 16...11
                self._add_tooth_button(fdi, self.upper_jaw_layout, 1, i)

            # Lower Jaw (Permanent)
            # Quadrant 3 (Lower Left on GUI)
            for i in range(8):
                fdi = 48 - i  # <-- FIX: Generates 48, 47, 46...41
                self._add_tooth_button(fdi, self.lower_jaw_layout, 1, i)

            # Quadrant 4 (Lower Right on GUI)
            for i in range(8):
                fdi = 31 + i  # <-- FIX: Generates 31, 32, 33...38
                self._add_tooth_button(fdi, self.lower_jaw_layout, 1, i + 9)

        elif self.chart.chart_type == 'primary':
            # Upper Jaw (Primary)
            
            # Quadrant 2 (Upper Left on GUI)
            for i in range(5):
                # fdi = 65 - i  <-- OLD
                fdi = 55 - i  # <-- FIX: Generates 55, 54, 53, 52, 51
                self._add_tooth_button(fdi, self.upper_jaw_layout, 1, i + 3)

            # Quadrant 1 (Upper Right on GUI)
            for i in range(5):
                # fdi = 51 + i  <-- OLD
                fdi = 61 + i  # <-- FIX: Generates 61, 62, 63, 64, 65
                self._add_tooth_button(fdi, self.upper_jaw_layout, 1, i + 9)

            # Lower Jaw (Primary)
            
            # Quadrant 3 (Lower Left on GUI)
            for i in range(5):
                # fdi = 75 - i  <-- OLD
                fdi = 85 - i  # <-- FIX: Generates 85, 84, 83, 82, 81
                self._add_tooth_button(fdi, self.lower_jaw_layout, 1, i + 3)

            # Quadrant 4 (Lower Right on GUI)
            for i in range(5):
                # fdi = 81 + i  <-- OLD
                fdi = 71 + i  # <-- FIX: Generates 71, 72, 73, 74, 75
                self._add_tooth_button(fdi, self.lower_jaw_layout, 1, i + 9)

    def _add_tooth_button(self, fdi_number, layout, row, col):
        """Helper to create, style, and add a single tooth button."""
        tooth = self.chart.get_tooth(fdi_number)
        if not tooth:
            return

        button = QPushButton(str(fdi_number))
        button.setFixedSize(QSize(45, 45))
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        button.clicked.connect(lambda checked, num=fdi_number: self._on_tooth_clicked(num))
        
        self.tooth_buttons[fdi_number] = button
        layout.addWidget(button, row, col)
        self._update_tooth_visual(fdi_number)

    def _update_tooth_visual(self, fdi_number):
        """Updates a button's color based on its tooth's status."""
        tooth = self.chart.get_tooth(fdi_number)
        button = self.tooth_buttons.get(fdi_number)
        if not tooth or not button:
            return

        # (CHANGED) tooth.status is now a key
        color = self.STATUS_COLORS.get(tooth.status, "#FFFFFF")
        text_color = "white" if QColor(color).value() < 128 else "black"
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}; 
                color: {text_color}; 
                border: 2px solid #7F8C8D;
                border-radius: 6px;
                font-weight: bold;
                padding: 0;
            }}
            QPushButton:checked {{
                border: 3px solid #E74C3C;
            }}
            QPushButton:hover {{
                border: 2px solid #3498DB;
            }}
        """)

    def _clear_layout(self, layout):
        """Helper function to remove all widgets from a layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    layout.removeItem(item)

    def _update_details_panel(self, fdi_number):
        """Updates the details panel widgets with a tooth's info."""
        if fdi_number is None:
            self.tooth_details_card.setEnabled(False)
            # (CHANGED) Use tr()
            self.details_name_label.setText(self.tr("details_tooth_unselected"))
            self.details_status_combo.setCurrentIndex(0)
            self.details_notes_edit.clear()
            self.current_selected_tooth_num = None
        else:
            tooth = self.chart.get_tooth(fdi_number)
            if not tooth:
                return
            
            self.tooth_details_card.setEnabled(True)
            
            # (CHANGED) Get name by translating keys
            q_key, t_key = tooth.name_keys
            q_name = self.tr(q_key)
            t_name = self.tr(t_key)
            self.details_name_label.setText(f"{tooth.fdi_number} - {q_name} {t_name}")
            
            # (CHANGED) Set status by translating key
            self.details_status_combo.setCurrentText(self.tr(tooth.status))
            
            self.details_notes_edit.setText(tooth.notes)
            self.current_selected_tooth_num = fdi_number

    def _refresh_all_tooth_visuals(self):
        """Iterates and updates the color of every tooth button."""
        for fdi_number in self.tooth_buttons.keys():
            self._update_tooth_visual(fdi_number)
            
    # (NEW) Rebuild status dropdown with current language
    def _rebuild_status_dropdown(self):
        self.details_status_combo.clear()
        self.details_status_combo.addItems([self.tr(key) for key in self.STATUS_LIST])

    # === SLOT METHODS ===

    # (NEW) Slot for language change
    @pyqtSlot(int)
    def _on_lang_changed(self, index):
        self.current_lang = "kh" if index == 0 else "en"
        self._retranslate_ui()

    # (NEW) Function to update all UI text
    def _retranslate_ui(self):
        # Window
        self.setWindowTitle(self.tr("window_title"))
        
        # Header
        self.clinic_title_label.setText(self.tr("clinic_title"))
        self.stat_total.title_label.setText(self.tr("total_patients"))
        self.stat_today.title_label.setText(self.tr("today_patients"))
        self.stat_month.title_label.setText(self.tr("month_patients"))
        self.lang_label.setText(self.tr("lang_label"))
        
        # Left Panel
        #self.search_bar.setPlaceholderText(self.tr("search_placeholder"))
        #self.search_button.setText(self.tr("search_button"))
        
        # --- FIX 4: Corrected tab indices ---
        self.patient_tabs.setTabText(0, self.tr("tab_info"))
        self.patient_tabs.setTabText(3, self.tr("tab_treatment"))
        self.patient_tabs.setTabText(1, self.tr("tab_billing"))
        self.patient_tabs.setTabText(2, self.tr("tab_appointment"))
        
        self.patient_tabs.setTabText(4, self.tr("tab_images"))
        # --- END OF FIX 4 ---
        
        # Patient Info Tab
        self.form_group.setTitle(self.tr("info_group_title"))
        self.info_id_label.setText(self.tr("info_id"))
        self.info_name_label.setText(self.tr("info_name"))
        
        self.info_phone_label.setText(self.tr("info_phone"))
        self.info_age_label.setText(self.tr("info_age"))
        self.info_address_label.setText(self.tr("info_address"))
        self.patient_id_edit.setPlaceholderText(self.tr("info_id_placeholder"))
        self.patient_age_edit.setPlaceholderText(self.tr("info_age_placeholder"))
        
        # (NEW) General Notes
        self.info_notes_label.setText(self.tr("info_general_notes"))
        self.patient_notes_edit.setPlaceholderText(self.tr("info_general_notes_ph"))

        # (ថ្មី) Treatment Tab
        self.treatment_group.setTitle(self.tr("treat_group_title"))
        self.treatment_table.setHorizontalHeaderLabels([
            self.tr("treat_col_date"),
            self.tr("treat_col_service"),
            self.tr("treat_col_tooth"),
            self.tr("treat_col_cost_usd"),
            self.tr("treat_col_cost_khr"),
            self.tr("treat_col_notes")
        ])
        self.add_treatment_button.setText(self.tr("treat_add_button"))
        self.remove_treatment_button.setText(self.tr("treat_remove_button"))
        
        # Billing Tab
        self.amount_group.setTitle(self.tr("billing_amount_group"))
        self.billing_usd_label1.setText(self.tr("billing_usd"))
        self.billing_khr_label1.setText(self.tr("billing_khr"))
        self.billing_total_label.setText(self.tr("billing_total"))
        self.payment_group.setTitle(self.tr("billing_new_payment_group"))
        self.history_group.setTitle(self.tr("billing_payment_history_group"))
        self.billing_usd_label2.setText(self.tr("billing_usd"))
        self.billing_khr_label2.setText(self.tr("billing_khr"))
        self.billing_payment_label.setText(self.tr("billing_payment"))
        self.add_payment_button.setText(self.tr("billing_add_payment_button"))
        self.billing_remaining_label.setText(self.tr("billing_remaining_label"))
        self.paid_check.setText(self.tr("billing_paid_check"))
        self._update_payment_history_ui() # Refresh payment list (for "No payments")

        # Appointment Tab
        self.appt_title_label.setText(self.tr("appt_group_title"))
        
        # (NEW) Images Tab
        # self.patient_tabs.setTabText(3, self.tr("tab_images")) # This is set in FIX 4
        self.images_group.setTitle(self.tr("images_group_title"))
        self.add_image_button.setText(self.tr("images_add_button"))
        self.view_image_button.setText(self.tr("images_view_button"))
        self.remove_image_button.setText(self.tr("images_remove_button"))
        
        # Right Panel
        self.chart_title_label.setText(self.tr("chart_title"))
        self.chart_type_label.setText(self.tr("chart_type_label"))
        self.perm_radio.setText(self.tr("chart_perm"))
        self.prim_radio.setText(self.tr("chart_prim"))
        self.upper_jaw_group.setTitle(self.tr("upper_jaw"))
        self.lower_jaw_group.setTitle(self.tr("lower_jaw"))
        
        # Tooth Details Panel
        self.tooth_details_card.setTitle(self.tr("details_group_title"))
        self.details_tooth_label.setText(self.tr("details_tooth"))
        self.details_status_label.setText(self.tr("details_status"))
        self.details_notes_label.setText(self.tr("details_notes"))
        self.details_save_button.setText(self.tr("details_save_button"))
        self._rebuild_status_dropdown() # Rebuild dropdown with new language
        self._update_details_panel(self.current_selected_tooth_num) # Re-translate selected tooth
        
        # Footer
        self.save_button.setText(self.tr("footer_save"))
        self.clear_button.setText(self.tr("footer_clear"))
        self.report_button.setText(self.tr("footer_report"))
        self.viewall_button.setText(self.tr("viewall_button"))
        self.print_button.setText(self.tr("footer_print")) # <--- (NEW)
        
        # (NEW) Footer Buttons
        self.delete_patient_button.setText(self.tr("footer_delete"))
        self.appointments_button.setText(self.tr("footer_appts"))
        self.backup_button.setText(self.tr("footer_backup"))
        self.restore_button.setText(self.tr("footer_restore"))

    @pyqtSlot(int)
    def _on_chart_type_changed(self, button_id):
        """Called when chart type radio button is clicked"""
        chart_type = 'permanent' if button_id == 1 else 'primary'
        if chart_type != self.chart.chart_type:
            self.chart = DentalChart(chart_type=chart_type)
            self._build_chart_grid()
            self._update_details_panel(None)

    @pyqtSlot(int)
    def _on_tooth_clicked(self, fdi_number):
        """Called when a tooth button is clicked"""
        for num, button in self.tooth_buttons.items():
            button.setChecked(num == fdi_number)
        self._update_details_panel(fdi_number)

    @pyqtSlot()
    def _on_save_details(self):
        """Called when the Update Tooth button is clicked"""
        if self.current_selected_tooth_num is None:
            return
            
        # (CHANGED) Get the language key, not the translated text
        selected_index = self.details_status_combo.currentIndex()
        if selected_index == -1: # Nothing selected
            return
        status_key = self.STATUS_LIST[selected_index]
        
        new_notes = self.details_notes_edit.toPlainText()
        
        # (CHANGED) Save using the key
        self.chart.update_status(self.current_selected_tooth_num, status_key, new_notes)
        self._update_tooth_visual(self.current_selected_tooth_num)

    @pyqtSlot()
    def _on_search_clicked(self):
        """Search for patients in the database"""
        self.found_files.clear()
        
        search_term = self.search_bar.text().lower().strip()
        if not search_term:
            return

        for patient_id, data in self.master_patient_list.items():
            try:
                name = data.get("patient_name", "").lower()
                phone = data.get("patient_phone", "").lower()
                id_str = str(patient_id).lower()
                
                if search_term in name or search_term in phone or search_term in id_str:
                    display_text = f"{data.get('patient_name', 'N/A')} (ID: {patient_id} | {data.get('patient_phone', 'N/A')})"
                    self.search_results_list.addItem(display_text)
                    self.found_files[display_text] = patient_id
            except Exception:
                pass

    @pyqtSlot()
    def _on_clear_search(self):
        """Clear search results"""
        self.found_files.clear()

    @pyqtSlot(QListWidgetItem)
    def _on_search_result_selected(self, item):
        """Load patient data when search result is double-clicked"""
        display_text = item.text()
        patient_id_to_load = self.found_files.get(display_text)
        
        if patient_id_to_load:
            patient_data = self.master_patient_list.get(patient_id_to_load)
            if patient_data:
                self._load_chart_from_data(patient_data)

    @pyqtSlot()
    def _on_add_payment(self):
        """Add a new payment to the current patient"""
        try:
            usd = float(self.new_payment_usd_edit.text() or "0")
            khr = float(self.new_payment_khr_edit.text() or "0")
        except ValueError:
            # (CHANGED) Use tr()
            QMessageBox.warning(self, self.tr("invalid_value_title"), self.tr("invalid_value_msg"))
            return
            
        if usd == 0 and khr == 0:
            return

        date_str = QDateTime.currentDateTime().toString(Qt.ISODate)
        
        payment_obj = {
            "date": date_str,
            "amount_usd": usd,
            "amount_khr": khr
        }
        
        self.current_payments_list.append(payment_obj)
        self._update_payment_history_ui()
        self._calculate_remaining_amount()
        
        self.new_payment_usd_edit.setText("0")
        self.new_payment_khr_edit.setText("0")

    def _update_payment_history_ui(self):
        """Update the payment history list display"""
        self.payment_history_list.clear()
        if not self.current_payments_list:
            # (CHANGED) Use tr()
            self.payment_history_list.addItem(self.tr("billing_no_payments"))
            return
        
        for payment in self.current_payments_list:
            date_str_iso = payment.get("date")
            if date_str_iso:
                date_str = QDateTime.fromString(date_str_iso, Qt.ISODate).toString("dd/MM/yyyy")
            else:
                date_str = "??/??/????"
                
            usd = float(payment.get("amount_usd", 0) or 0)
            khr = float(payment.get("amount_khr", 0) or 0)
            display_text = f"[{date_str}] - ${usd:,.2f}  |  {khr:,.0f} ៛"
            self.payment_history_list.addItem(display_text)

    def _calculate_remaining_amount(self):
        """Calculate and display remaining payment amount"""
        total_deposit_usd = 0.0
        total_deposit_khr = 0.0
        for payment in self.current_payments_list:
            total_deposit_usd += float(payment.get("amount_usd", 0) or 0)
            total_deposit_khr += float(payment.get("amount_khr", 0) or 0)

        try:
            total_usd = float(self.total_amount_usd_edit.text() or "0")
        except ValueError:
            total_usd = 0
        
        try:
            total_khr = float(self.total_amount_khr_edit.text() or "0")
        except ValueError:
            total_khr = 0
            
        remaining_usd = total_usd - total_deposit_usd
        remaining_khr = total_khr - total_deposit_khr
        
        self.remaining_usd_label.setText(f"{remaining_usd:,.2f} $")
        self.remaining_khr_label.setText(f"{remaining_khr:,.0f} ៛")

    @pyqtSlot()
    def _on_save_chart(self):
        """Save current patient data to database"""
        patient_id = self.patient_id_edit.text().strip()
        if not patient_id:
            # (CHANGED) Use tr()
            QMessageBox.warning(self, self.tr("save_fail_id_title"), self.tr("save_fail_id_msg"))
            return
            
        if not self.patient_name_edit.text():
            # (CHANGED) Use tr()
            QMessageBox.warning(self, self.tr("save_fail_id_title"), self.tr("save_fail_name_msg"))
            return
        
        # --- (NEW) Auto-save address ---
        current_address = self.patient_address_combo.currentText().strip()
        if current_address and current_address not in self.address_list:
            self.address_list.append(current_address)
            # Add to combo box *without* re-reading the file
            self.patient_address_combo.addItem(current_address) 
            self._save_addresses_file() # Save to address.txt
        # -------------------------------
        
        patient_data = {
            "patient_name": self.patient_name_edit.text(),
            "patient_id": patient_id,
            "patient_phone": self.patient_phone_edit.text(),
            
            # --- (កែប្រែ) រក្សាទុក "អាយុ" ជំនួស "dob" ---
            "patient_age": self.patient_age_edit.text(),
            # ---------------------------------------
            
            "patient_address": current_address, # <--- បន្ថែម
            "chart_type": self.chart.chart_type,
            
            "total_amount_usd": self.total_amount_usd_edit.text(),
            "total_amount_khr": self.total_amount_khr_edit.text(),
            "payments": self.current_payments_list,
            "is_paid": self.paid_check.isChecked(),

            "treatments": self.current_treatments_list, # (ថ្មី) រក្សាទុក Treatments
            "payments": self.current_payments_list,

            "next_appointment": self.appointment_edit.dateTime().toString(Qt.ISODate),
            
            # (NEW) Save general notes and image links
            "general_notes": self.patient_notes_edit.toPlainText(),
            "images": [self.image_list_widget.item(i).text() for i in range(self.image_list_widget.count())]
        }
        
        teeth_data = {}
        for fdi, tooth in self.chart.teeth.items():
            teeth_data[fdi] = {
                # (CHANGED) tooth.status is already a key, this is correct
                "status": tooth.status,
                "notes": tooth.notes
            }
        patient_data["teeth"] = teeth_data
        
        self.master_patient_list[patient_id] = patient_data
        
        if self._save_master_database():
            # (CHANGED) Use tr()
            QMessageBox.information(self, self.tr("save_success_title"),
                                      self.tr("save_success_msg", patient_id=patient_id))
            
            # (NEW) Update header stats after saving
            self._update_header_stats()

    def _load_master_database(self):
        """Load the master database from file"""
        try:
            if os.path.exists(self.database_file):
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    self.master_patient_list = json.load(f)
            else:
                self.master_patient_list = {}
        except Exception as e:
            self.master_patient_list = {}

    # --- (ថ្មី) Function សម្រាប់អាន address.txt ---
    def _load_addresses(self):
        """Loads addresses from address.txt or creates the file if it doesn't exist."""
        self.address_list = []
        filename = "Data/address.txt"
        try:
            # Ensure the "Data" directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            if not os.path.exists(filename):
                # File doesn't exist, create it with default data
                self.address_list = ["ភ្នំពេញ", "ខេត្តកណ្ដាល", "ខេត្តកំពង់ចាម", "ខេត្តបាត់ដំបង", "ខេត្តសៀមរាប"]
                with open(filename, 'w', encoding='utf-8') as f:
                    for address in self.address_list:
                        f.write(address + "\n")
            else:
                # File exists, read from it
                with open(filename, 'r', encoding='utf-8') as f:
                    # Read all lines, strip whitespace, and filter out empty lines
                    self.address_list = [line.strip() for line in f if line.strip()]
                    
        except Exception as e:
            print(f"Error loading address.txt: {e}")
            self.address_list = ["Error: Could not load file"]
    # --- (ចប់ Function ថ្មី) ---

    def _save_master_database(self):
        """Save the master database to file"""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(self.master_patient_list, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "កំហុសក្នុងការរក្សាទុក",
                               f"មិនអាចរក្សាទុកទិន្នន័យបានទេ: {e}")
            return False

    def _load_chart_from_data(self, patient_data):
        """Load patient data into the UI"""
        try:
            self.patient_name_edit.setText(patient_data.get("patient_name", ""))
            self.patient_id_edit.setText(patient_data.get("patient_id", ""))
            self.patient_phone_edit.setText(patient_data.get("patient_phone", ""))
            
            # --- (កែប្រែ) ផ្ទុក "អាយុ" និង "អាសយដ្ឋាន" ---
            self.patient_age_edit.setText(patient_data.get("patient_age", ""))
            self.patient_address_combo.setCurrentText(patient_data.get("patient_address", ""))
            # -----------------------------------
            
            # (NEW) Load general notes and image links
            self.patient_notes_edit.setText(patient_data.get("general_notes", ""))
            
            self.image_list_widget.clear()
            self.image_list_widget.addItems(patient_data.get("images", []))
            
            self.current_treatments_list = patient_data.get("treatments", [])
            self._update_treatment_table_ui()
            self._recalculate_totals_from_treatments() # វានឹង Update ផ្ទាំង Billing ស្វ័យប្រវត្តិ

            self.current_payments_list = patient_data.get("payments", [])
            self._update_payment_history_ui()
            
            

            self.paid_check.setChecked(patient_data.get("is_paid", False))
            self._calculate_remaining_amount()
            
            appt_string = patient_data.get("next_appointment", "")
            appt_datetime = QDateTime.fromString(appt_string, Qt.ISODate)
            self.appointment_edit.setDateTime(appt_datetime if appt_datetime.isValid() else QDateTime.currentDateTime())

            chart_type = patient_data.get("chart_type", "permanent")
            if chart_type == "primary":
                self.prim_radio.setChecked(True)
            else:
                self.perm_radio.setChecked(True)
            
            teeth_data = patient_data.get("teeth", {})
            for fdi_str, data in teeth_data.items():
                try:
                    fdi_num = int(fdi_str)
                    # (CHANGED) status is now loaded as a key, which is correct
                    self.chart.update_status(fdi_num,
                                             data.get("status", "present"),
                                             data.get("notes", ""))
                except ValueError:
                    pass
            
            self._refresh_all_tooth_visuals()
            self._update_details_panel(None)
            
            # (CHANGED) Use tr()
            QMessageBox.information(self, self.tr("load_success_title"),
                                      self.tr("load_success_msg", patient_name=self.patient_name_edit.text()))

        except Exception as e:
            # (CHANGED) Use tr()
            QMessageBox.critical(self, self.tr("load_fail_title"),
                                       self.tr("load_fail_msg", e=e))

    @pyqtSlot()
    def _on_clear_chart(self):
        """Clear all patient data and reset the chart"""
        # (CHANGED) Use tr()
        reply = QMessageBox.question(self, self.tr("clear_title"),
                                       self.tr("clear_msg"),
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.patient_name_edit.clear()
            
            # --- (កែប្រែ) បង្កើត ID ថ្មី ជំនួសឲ្យការលុបចោល ---
            self.patient_id_edit.setText(self._get_next_patient_id())
            # ---------------------------------------------
            
            self.patient_phone_edit.clear()
            
            # --- (កែប្រែ) សម្អាត "អាយុ" និង "អាសយដ្ឋាន" ---
            self.patient_address_combo.setCurrentText("")
            self.patient_age_edit.clear()
            # -------------------------------------
            
            # (NEW) Clear general notes and images
            self.patient_notes_edit.clear()
            self.image_list_widget.clear()
            
            # (ថ្មី) សម្អាត Treatment
            self.current_treatments_list = []
            self._update_treatment_table_ui()
            self._recalculate_totals_from_treatments() # វានឹង clear ផ្ទាំង Billing
            
            self.new_payment_usd_edit.setText("0")
            self.new_payment_khr_edit.setText("0")
            self.current_payments_list = []
            self._update_payment_history_ui()
            self.paid_check.setChecked(False)
            self._calculate_remaining_amount()
            
            self.appointment_edit.setDateTime(QDateTime.currentDateTime())

            self.perm_radio.setChecked(True)
            self._update_details_panel(None)
            self.found_files.clear()

    @pyqtSlot()
    def _viewall_button(self):
        """Show a dialog with all patients in the database"""
        if not self.master_patient_list:
            QMessageBox.information(self, self.tr("view_all_title"), self.tr("view_all_empty"))
            return
            
        dialog = ViewAllPatientsDialog(self.master_patient_list, self)
        
        dialog.patient_selected.connect(self._load_patient_by_id_slot)
        dialog.patient_deleted.connect(self._on_delete_patient_from_dialog) # (ថ្មី) បន្ថែមបន្ទាត់នេះ
        
        dialog.exec_()

    # --- (NEW) FUNCTION សម្រាប់បោះពុម្ព ---
    @pyqtSlot(str)
    def _on_delete_patient_from_dialog(self, patient_id):
        """
        (ថ្មី) Slot នេះត្រូវបានហៅដោយ Dialog 'ViewAll' ពេលប៊ូតុង Delete ត្រូវបានចុច។
        វានឹងលុបអ្នកជំងឺចេញពី master list និងរក្សាទុក database។
        """
        if patient_id in self.master_patient_list:
            try:
                # លុបចេញពី master list
                del self.master_patient_list[patient_id]
                
                # រក្សាទុក database ឡើងវិញ
                if self._save_master_database():
                    # បើអ្នកជំងឺដែលកំពុងលុប ជាអ្នកជំងឺដែលកំពុងបើក
                    if self.patient_id_edit.text() == patient_id:
                        self._on_clear_chart() # សម្អាត Form
                    
                    self._update_header_stats() # Update តួលេខ
                    print(f"Patient {patient_id} deleted successfully from database.")
                else:
                    # បើ save បរាជ័យ, ផ្ទុក database ឡើងវិញ
                    self._load_master_database()

            except Exception as e:
                QMessageBox.critical(self, self.tr("delete_fail_title"),
                                           self.tr("delete_fail_msg", e=e))
                self._load_master_database() # ផ្ទុកឡើងវិញឲ្យប្រាកដ
                
    @pyqtSlot()
    def _on_print_patient(self):
        """Handles the patient print action"""
        patient_name = self.patient_name_edit.text().strip()
        patient_id = self.patient_id_edit.text().strip()
        
        # ពិនិត្យមើលថាតើមានអ្នកជំងឺដែលត្រូវបោះពុម្ពឬអត់
        if not patient_name or not patient_id:
            QMessageBox.warning(self, 
                self.tr("print_fail_title"), 
                self.tr("print_fail_msg"))
            return

        # 1. បង្កើត QPrinter
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A7) # កំណត់ទំហំក្រដាស A4
        printer.setFullPage(True)

        # 2. បង្ហាញ Print Dialog
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(self.tr("print_dialog_title"))
        
        if dialog.exec_() != QDialog.Accepted:
            return # User បានចុច Cancel

        # 3. បង្កើត nội dung ជា HTML
        html_content = self._generate_patient_report_html()

        # 4. បោះពុម្ព HTML ទៅកាន់ printer
        document = QTextDocument()
        document.setHtml(html_content)
        document.print_(printer)

    def _generate_patient_report_html(self):
        """
        Generates a summary of the current patient as an HTML string.
        """
        # --- 1. ប្រមូលទិន្នន័យពី UI ---
        name = self.patient_name_edit.text()
        pid = self.patient_id_edit.text()
        phone = self.patient_phone_edit.text()
        age = self.patient_age_edit.text()
        address = self.patient_address_combo.currentText()
        general_notes = self.patient_notes_edit.toPlainText().replace("\n", "<br>") # (NEW)
        
        total_usd = self.total_amount_usd_edit.text()
        total_khr = self.total_amount_khr_edit.text()
        paid_status = self.tr("yes") if self.paid_check.isChecked() else self.tr("no")
        remaining_usd = self.remaining_usd_label.text()
        remaining_khr = self.remaining_khr_label.text()
        
        appt = self.appointment_edit.dateTime().toString("dd/MM/yyyy hh:mm ap")

        # --- 2. ប្រមូលកំណត់ត្រាធ្មេញ (Dental Chart Notes) ---
        chart_notes = []
        for fdi, tooth in self.chart.teeth.items():
            # រាយតែធ្មេញណាដែលមានបញ្ហា (មិនមែន 'present')
            if tooth.status != "present":
                status_text = self.tr(tooth.status)
                notes = f" ({self.tr('details_notes')}: {tooth.notes})" if tooth.notes else ""
                chart_notes.append(f"<li><b>{self.tr('details_tooth')} {fdi}:</b> {status_text}{notes}</li>")

        if not chart_notes:
            chart_notes.append(f"<li>{self.tr('print_chart_no_issues')}</li>")

        # --- 3. បង្កើត HTML String ---
        # (អ្នកអាចកែសម្រួល CSS នេះតាមចិត្ត)
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: "Khmer OS", "Segoe UI", Arial, sans-serif; font-size: 10pt; }}
                h1 {{ 
                    color: #2C3E50; 
                    border-bottom: 2px solid #3498DB; 
                    padding-bottom: 5px;
                }}
                h2 {{ 
                    color: #3498DB; 
                    background-color: #F4F6F6;
                    padding: 8px;
                    border-radius: 5px;
                }}
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-bottom: 15px;
                }}
                td, th {{ 
                    border: 1px solid #E9ECEF; 
                    padding: 8px; 
                    text-align: left;
                }}
                th {{ background-color: #F8F9FA; }}
                .label {{ font-weight: bold; width: 30%; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 5px; }}
            </style>
        </head>
        <body>
            <h1>{self.tr('clinic_title')}</h1>
            <p>{self.tr('report_today', date=QDate.currentDate().toString('dd/MM/yyyy'))}</p>
            
            <h2>{self.tr("print_header_info")}</h2>
            <table>
                <tr>
                    <td class="label">{self.tr("print_patient_name")}</td>
                    <td>{name}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("print_patient_id")}</td>
                    <td>{pid}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("info_phone")}</td>
                    <td>{phone}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("info_age")}</td>
                    <td>{age}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("info_address")}</td>
                    <td>{address}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("info_general_notes")}</td>
                    <td>{general_notes}</td>
                </tr>
            </table>

            <h2>{self.tr("print_header_billing")}</h2>
            <table>
                <tr>
                    <td class="label">{self.tr("print_total_usd")}</td>
                    <td>{total_usd} $</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("print_total_khr")}</td>
                    <td>{total_khr} ៛</td>
                </tr>
                 <tr>
                    <td class="label">{self.tr("print_paid_status")}</td>
                    <td>{paid_status}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("print_remaining_usd")}</td>
                    <td style="font-weight: bold; color: #E74C3C;">{remaining_usd}</td>
                </tr>
                <tr>
                    <td class="label">{self.tr("print_remaining_khr")}</td>
                    <td style="font-weight: bold; color: #E74C3C;">{remaining_khr}</td>
                </tr>
            </table>

            <h2>{self.tr("print_header_chart")}</h2>
            <ul>
                {''.join(chart_notes)}
            </ul>

            <h2>{self.tr("tab_appointment")}</h2>
            <p><b>{self.tr("appt_group_title")}:</b> {appt}</p>
            
        </body>
        </html>
        """
        return html
    # --- (ចប់ FUNCTION ថ្មី) ---

    @pyqtSlot()
    def _on_show_income_report(self):
        """Show a printable income report dialog"""
        today = QDate.currentDate()
        
        today_usd, today_khr = 0.0, 0.0
        month_usd, month_khr = 0.0, 0.0
        year_usd, year_khr = 0.0, 0.0
        total_usd, total_khr = 0.0, 0.0

        if not self.master_patient_list:
            # (CHANGED) Use tr()
            QMessageBox.information(self, self.tr("report_title"), self.tr("report_no_data"))
            return

        for patient_id, data in self.master_patient_list.items():
            try:
                payments = data.get("payments", [])
                
                for payment in payments:
                    payment_date = QDateTime.fromString(payment.get("date"), Qt.ISODate).date()
                    if not payment_date.isValid():
                        continue
                        
                    usd = float(payment.get("amount_usd", 0) or 0)
                    khr = float(payment.get("amount_khr", 0) or 0)
                    
                    total_usd += usd
                    total_khr += khr
                    
                    if payment_date.year() == today.year():
                        year_usd += usd
                        year_khr += khr
                        
                        if payment_date.month() == today.month():
                            month_usd += usd
                            month_khr += khr
                            
                            if payment_date == today:
                                today_usd += usd
                                today_khr += khr
                                
            except Exception:
                pass

        # (CHANGED) Use tr() for report text
        report_text = f"""
<b>{self.tr("report_title")}</b>
<hr>
<b>{self.tr("report_today", date=today.toString("dd/MM/yyyy"))}</b><br>
&nbsp;&nbsp;&nbsp; ${today_usd:,.2f}<br>
&nbsp;&nbsp;&nbsp; {today_khr:,.0f} ៛
<br><br>
<b>{self.tr("report_month", month=today.month(), year=today.year())}</b><br>
&nbsp;&nbsp;&nbsp; ${month_usd:,.2f}<br>
&nbsp;&nbsp;&nbsp; {month_khr:,.0f} ៛
<br><br>
<b>{self.tr("report_year", year=today.year())}</b><br>
&nbsp;&nbsp;&nbsp; ${year_usd:,.2f}<br>
&nbsp;&nbsp;&nbsp; {year_khr:,.0f} ៛
<br><br>
<b>{self.tr("report_total")}:</b><br>
&nbsp;&nbsp;&nbsp; ${total_usd:,.2f}<br>
&nbsp;&nbsp;&nbsp; {total_khr:,.0f} ៛
        """
        
        # --- (NEW) Show in a printable dialog ---
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("report_title"))
        dialog.setWindowIcon(QIcon("Data/toothdoctor_diente_10727.ico"))
        dialog.setMinimumSize(450, 500)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setHtml(report_text)
        text_edit.setReadOnly(True)
        
        print_button = QPushButton(self.tr("footer_print"))
        print_button.setObjectName("info-button")
        
        # Use a lambda to pass the HTML content to the print helper
        print_button.clicked.connect(lambda: self._print_html_content(report_text))

        layout.addWidget(text_edit)
        layout.addWidget(print_button)
        
        dialog.exec_()
        # --- (End of new section) ---
        
    # === (NEW) SLOTS FOR NEW FEATURES ===

    @pyqtSlot(str)
    def _load_patient_by_id_slot(self, patient_id):
        """(NEW) Slot to load a patient by ID from a signal"""
        patient_data = self.master_patient_list.get(patient_id)
        if patient_data:
            self._load_chart_from_data(patient_data)
        else:
            QMessageBox.warning(self, self.tr("load_fail_title"),
                                      self.tr("load_fail_id_msg", patient_id=patient_id))
    
    @pyqtSlot()
    def _on_delete_patient(self):
        """(NEW) Delete the currently loaded patient"""
        patient_id = self.patient_id_edit.text().strip()
        patient_name = self.patient_name_edit.text().strip()
        
        if not patient_id or patient_id not in self.master_patient_list:
            QMessageBox.warning(self, self.tr("delete_fail_title"),
                                      self.tr("delete_fail_msg_noload"))
            return

        reply = QMessageBox.warning(self, self.tr("delete_confirm_title"),
                                      self.tr("delete_confirm_msg", patient_name=patient_name, patient_id=patient_id),
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Remove from the master list
                del self.master_patient_list[patient_id]
                
                # Save the updated database
                if self._save_master_database():
                    QMessageBox.information(self, self.tr("delete_success_title"),
                                                  self.tr("delete_success_msg", patient_name=patient_name))
                    
                    # Clear the form
                    self._on_clear_chart()
                    
                    # Update header stats
                    self._update_header_stats()
                else:
                    # If save failed, reload (to be safe)
                    self._load_master_database()
                    
            except Exception as e:
                QMessageBox.critical(self, self.tr("delete_fail_title"),
                                           self.tr("delete_fail_msg", e=e))

    @pyqtSlot()
    def _on_add_image_link(self):
        """(NEW) Add a new image file link"""
        file_path, _ = QFileDialog.getOpenFileName(self,
            self.tr("images_dialog_title"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        
        if file_path:
            self.image_list_widget.addItem(file_path)

    @pyqtSlot()
    def _on_view_image_link(self):
        """(NEW) Open a selected image link in the default viewer"""
        selected_item = self.image_list_widget.currentItem()
        if selected_item:
            file_path = selected_item.text()
            if os.path.exists(file_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
            else:
                QMessageBox.warning(self, self.tr("images_fail_title"),
                                          self.tr("images_fail_msg", path=file_path))

    @pyqtSlot()
    def _on_remove_image_link(self):
        """(NEW) Remove a selected image link"""
        selected_item = self.image_list_widget.currentItem()
        if selected_item:
            row = self.image_list_widget.row(selected_item)
            self.image_list_widget.takeItem(row)

    @pyqtSlot()
    def _on_backup_database(self):
        """(NEW) Create a timestamped backup of the database"""
        if not os.path.exists(self.database_file):
            QMessageBox.warning(self, self.tr("backup_fail_title"), self.tr("backup_fail_nodb"))
            return
            
        try:
            timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
            backup_filename = f"clinic_database_backup_{timestamp}.json"
            
            shutil.copy(self.database_file, backup_filename)
            
            QMessageBox.information(self, self.tr("backup_success_title"),
                                          self.tr("backup_success_msg", filename=backup_filename))
        except Exception as e:
            QMessageBox.critical(self, self.tr("backup_fail_title"),
                                       self.tr("backup_fail_msg", e=e))

    @pyqtSlot()
    def _on_restore_database(self):
        """(NEW) Restore the database from a backup file"""
        file_path, _ = QFileDialog.getOpenFileName(self,
            self.tr("restore_dialog_title"), "", "JSON Files (*.json)")
        
        if file_path:
            reply = QMessageBox.warning(self, self.tr("restore_confirm_title"),
                                              self.tr("restore_confirm_msg"),
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                try:
                    shutil.copy(file_path, self.database_file)
                    
                    # Reload the data
                    self._load_master_database()
                    self._on_clear_chart() # Clear the UI
                    self._update_header_stats() # Update header
                    
                    QMessageBox.information(self, self.tr("restore_success_title"),
                                                  self.tr("restore_success_msg"))
                except Exception as e:
                    QMessageBox.critical(self, self.tr("restore_fail_title"),
                                               self.tr("restore_fail_msg", e=e))
                    
    @pyqtSlot()
    def _check_today_appointments(self):
        """(NEW) ពិនិត្យមើលការណាត់ជួបសម្រាប់ថ្ងៃនេះ ហើយបង្ហាញការជូនដំណឹង"""
        today_appts = []
        today = QDate.currentDate() # យកកាលបរិច្ឆេទថ្ងៃនេះ

        # រកមើលនៅក្នុងទិន្នន័យអ្នកជំងឺទាំងអស់
        for patient_id, data in self.master_patient_list.items():
            appt_str = data.get("next_appointment")
            if appt_str:
                appt_dt = QDateTime.fromString(appt_str, Qt.ISODate)
                
                # បើការណាត់ជួបមានថ្ងៃស្មើនឹងថ្ងៃនេះ
                if appt_dt.isValid() and appt_dt.date() == today:
                    name = data.get("patient_name", "N/A")
                    phone = data.get("patient_phone", "N/A")
                    # បន្ថែមទៅក្នុងបញ្ជី (យើងប្រើ QDateTime ពេញ ដើម្បីស្រួលS ort តាមម៉ោង)
                    today_appts.append((appt_dt, name, phone, patient_id))
        
        # បើគ្មានការណាត់ជួប មិនបាច់ធ្វើអ្វីទេ
        if not today_appts:
            return

        # Sort បញ្ជីតាមពេលវេលា (ពីព្រឹកទៅល្ងាច)
        today_appts.sort()
        
        # បង្កើតសារជូនដំណឹង
        title = self.tr("appts_today_title") # ប្រើ key ថ្មី
        
        # បង្កើត HTML សម្រាប់បង្ហាញក្នុង MessageBox
        message_html = f"<b>{self.tr('appts_today_header', date=today.toString('dd/MM/yyyy'))}</b><hr>"
        
        for appt_dt, name, phone, pid in today_appts:
            message_html += (
                f"<b>{appt_dt.toString('hh:mm ap')}</b><br>"
                f"&nbsp;&nbsp;{name} (ID: {pid})<br>"
                f"&nbsp;&nbsp;{phone}<br><br>"
            )
        
        # បង្ហាញ MessageBox
        QMessageBox.information(self, title, message_html)

    @pyqtSlot()
    def _on_view_appointments(self):
        """(NEW) Show a list of all upcoming appointments"""
        upcoming_appts = []
        # now = QDateTime.currentDateTime() # (កែប្រែ) លុបចោល
        today_date = QDate.currentDate() # (ថ្មី) យកតែថ្ងៃ ខែ ឆ្នាំ បច្ចុប្បន្ន

        for patient_id, data in self.master_patient_list.items():
            appt_str = data.get("next_appointment")
            if appt_str:
                appt_dt = QDateTime.fromString(appt_str, Qt.ISODate)
                
                # --- (ការកែប្រែចម្បង) ---
                # ពិនិត្យមើលថាតើ "ថ្ងៃ" ណាត់ជួប ធំជាង ឬស្មើ "ថ្ងៃ" នេះ
                # if appt_dt.isValid() and appt_dt > now: # (ចាស់)
                if appt_dt.isValid() and appt_dt.date() >= today_date: # (ថ្មី)
                # --- (ចប់ការកែប្រែ) ---
                
                    name = data.get("patient_name", "N/A")
                    phone = data.get("patient_phone", "N/A")
                    upcoming_appts.append((appt_dt, name, phone, patient_id))
        
        if not upcoming_appts:
            QMessageBox.information(self, self.tr("appts_title"),
                                          self.tr("appts_none"))
            return

        # Sort by date
        upcoming_appts.sort()
        
        report_html = f"<b>{self.tr('appts_title')}</b><hr>" # ចំណងជើងនៅដដែល
        for appt_dt, name, phone, pid in upcoming_appts:
            report_html += (
                f"<b>{appt_dt.toString('dd/MM/yyyy hh:mm ap')}</b><br>"
                f"&nbsp;&nbsp;{name} (ID: {pid})<br>"
                f"&nbsp;&nbsp;{phone}<br><br>"
            )
            
        # Re-use the printable dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("appts_title"))
        dialog.setWindowIcon(QIcon("Data/toothdoctor_diente_10727.ico"))
        dialog.setMinimumSize(450, 500)
        
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setHtml(report_html)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        dialog.exec_()
        
    # === (NEW) HELPER FUNCTIONS ===
    
    def _print_html_content(self, html_content):
        """(NEW) Helper function to print any HTML string"""
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setFullPage(True)

        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle(self.tr("print_dialog_title"))
        
        if dialog.exec_() == QDialog.Accepted:
            document = QTextDocument()
            document.setHtml(html_content)
            document.print_(printer)
            
    def _save_addresses_file(self):
        """(NEW) Helper to save the address list back to file"""
        filename = "Data/address.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for address in self.address_list:
                    f.write(address + "\n")
        except Exception as e:
            print(f"Error saving address.txt: {e}")
            
    def _update_header_stats(self):
        """(NEW) Calculate and update the header statistics"""
        total_patients = len(self.master_patient_list)
        today_appts = 0
        month_appts = 0
        
        today = QDate.currentDate()

        for patient_id, data in self.master_patient_list.items():
            appt_str = data.get("next_appointment")
            if appt_str:
                appt_dt = QDateTime.fromString(appt_str, Qt.ISODate)
                if appt_dt.isValid():
                    appt_date = appt_dt.date()
                    if appt_date == today:
                        today_appts += 1
                    if appt_date.month() == today.month() and appt_date.year() == today.year():
                        month_appts += 1

        self.stat_total.value_label.setText(str(total_patients))
        self.stat_today.value_label.setText(str(today_appts))
        self.stat_month.value_label.setText(str(month_appts))

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_QSS)
    window = DentalChartApp()
    window.show()
    sys.exit(app.exec_())