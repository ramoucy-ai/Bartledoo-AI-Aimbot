# overlay.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QTimer
import ctypes
from ctypes import wintypes

class PyQtOverlay(QWidget):
    def __init__(self, boxes_queue, confidences_queue, config):
        super().__init__()
        self.boxes_queue = boxes_queue
        self.confidences_queue = confidences_queue
        self.config = config
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.setGeometry(0, 0, config.width, config.height)
        self.boxes = []
        self.confidences = []
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_overlay)
        
        # 使用與檢測間隔一致的更新頻率
        update_interval_ms = max(int(config.detect_interval * 1000), 16)  # 最小16ms (約60fps)
        self.timer.start(update_interval_ms)
        
        self.show()
        self.set_click_through()

    def set_click_through(self):
        try:
            hwnd = self.winId().__int__()
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_TRANSPARENT = 0x20
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception as e:
            print(f"滑鼠穿透設置失敗: {e}")

    def update_overlay(self):
        # 從隊列獲取最新的檢測結果
        new_boxes = None
        new_confidences = None
        
        try:
            new_boxes = self.boxes_queue.get_nowait()
        except:
            pass
            
        try:
            new_confidences = self.confidences_queue.get_nowait()
        except:
            pass
        
        # 更新顯示數據
        if new_boxes is not None:
            self.boxes = new_boxes
        if new_confidences is not None:
            self.confidences = new_confidences
            
        # 只在功能啟用時重繪
        if self.config.AimToggle:
            self.update()

    def draw_corner_box(self, painter, x1, y1, x2, y2, corner_size=15):
        """繪製四個角點"""
        # 設定點的大小
        point_size = 3
        
        # 左上角點
        painter.drawEllipse(x1 - point_size//2, y1 - point_size//2, point_size, point_size)
        
        # 右上角點
        painter.drawEllipse(x2 - point_size//2, y1 - point_size//2, point_size, point_size)
        
        # 左下角點
        painter.drawEllipse(x1 - point_size//2, y2 - point_size//2, point_size, point_size)
        
        # 右下角點
        painter.drawEllipse(x2 - point_size//2, y2 - point_size//2, point_size, point_size)

    def paintEvent(self, event):
        if not self.config.AimToggle:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 讀取顯示設置
        show_fov = getattr(self.config, 'show_fov', True)
        show_boxes = getattr(self.config, 'show_boxes', True)
        
        # 繪製 FOV 框
        if show_fov:
            fov = self.config.fov_size
            cx, cy = self.config.crosshairX, self.config.crosshairY
            pen = QPen(QColor(255, 0, 0, 180), 1)
            painter.setPen(pen)
            painter.drawRect(cx - fov // 2, cy - fov // 2, fov, fov)

        # 繪製檢測框和置信度
        if show_boxes and self.boxes:
            pen_box = QPen(QColor(0, 255, 0, 200), 2)
            painter.setPen(pen_box)
            
            show_confidence = self.config.show_confidence
            if show_confidence:
                pen_text = QPen(QColor(255, 255, 0, 220), 1)
                font = QFont('Arial', 9, QFont.Weight.Bold)
                painter.setFont(font)
            
            for i, box in enumerate(self.boxes):
                x1, y1, x2, y2 = map(int, box)
                
                # 使用新的角框繪製方法
                self.draw_corner_box(painter, x1, y1, x2, y2)
                
                if show_confidence and i < len(self.confidences):
                    confidence = self.confidences[i]
                    text = f"{confidence:.0%}"
                    painter.setPen(pen_text)
                    # 將文字移到左上角外側，並增加距離
                    painter.drawText(x1 - 20, y1 - 15, text)
                    painter.setPen(pen_box)

def start_pyqt_overlay(boxes_queue, confidences_queue, config):
    print("警告: start_pyqt_overlay 函式已被棄用，UI 啟動邏輯已移至 main.py。")
    pass