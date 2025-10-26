# main.py
import threading
import queue
import time
import math
import numpy as np
import cv2
import mss
import win32api
import win32con
import sys
import winsound
import os
import psutil
from typing import Optional

# When bundled with PyInstaller, ensure native dependencies are discoverable.
_DLL_DIR_HANDLES = []
if sys.platform == "win32":
    def _maybe_add_dll_dir(path: str):
        if not path:
            return
        try:
            handle = os.add_dll_directory(path)
            _DLL_DIR_HANDLES.append(handle)
        except AttributeError:
            os.environ["PATH"] = f"{path};{os.environ.get('PATH', '')}"
        except (FileNotFoundError, NotADirectoryError):
            pass

    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, '_MEIPASS', '')
        search_roots = [
            base_dir,
            os.path.join(base_dir, 'onnxruntime'),
            os.path.join(base_dir, 'onnxruntime', 'capi'),
        ]
        for candidate in search_roots:
            if candidate and os.path.isdir(candidate):
                _maybe_add_dll_dir(candidate)

        exe_dir = os.path.dirname(sys.executable)
        fallback_dirs = [
            os.path.join(exe_dir, 'onnxruntime'),
            os.path.join(exe_dir, 'onnxruntime', 'capi'),
        ]
        for candidate in fallback_dirs:
            if os.path.isdir(candidate):
                _maybe_add_dll_dir(candidate)

# 根據模型類型導入不同函式庫
import onnxruntime as ort
import torch
from ultralytics import YOLO

# 從我們自己建立的模組中導入
from config import Config, load_config
from win_utils import send_mouse_move, send_mouse_click, is_key_pressed, check_and_request_admin, test_ddxoft_functions, get_ddxoft_statistics, ensure_ddxoft_ready
from inference import preprocess_image, postprocess_outputs, non_max_suppression, PIDController
from overlay import start_pyqt_overlay, PyQtOverlay
from settings_gui import create_settings_gui
from status_panel import StatusPanel
from scaling_warning_dialog import check_windows_scaling



# 全域變數宣告
ai_thread: Optional[threading.Thread] = None
auto_fire_thread: Optional[threading.Thread] = None

def optimize_cpu_performance(config):
    """優化CPU性能設定"""
    if not getattr(config, 'cpu_optimization', True):
        return
    
    try:
        # 獲取當前進程
        current_process = psutil.Process()
        
        # 設定進程優先級 (Windows 專用)
        if sys.platform == "win32":
            process_priority = getattr(config, 'process_priority', 'high')
            try:
                if process_priority == 'realtime':
                    current_process.nice(psutil.REALTIME_PRIORITY_CLASS)
                    print("[性能優化] 設定進程優先級為：實時")
                elif process_priority == 'high':
                    current_process.nice(psutil.HIGH_PRIORITY_CLASS)
                    print("[性能優化] 設定進程優先級為：高")
                else:
                    current_process.nice(psutil.NORMAL_PRIORITY_CLASS)
                    print("[性能優化] 設定進程優先級為：正常")
            except Exception as e:
                print(f"[性能優化] 設定進程優先級失敗：{e}")
        else:
            print("[性能優化] 跳過進程優先級設定")
        
        # 設定CPU親和性
        cpu_affinity = getattr(config, 'cpu_affinity', None)
        if cpu_affinity is not None:
            current_process.cpu_affinity(cpu_affinity)
            print(f"[性能優化] 設定CPU親和性為：{cpu_affinity}")
        else:
            # 使用所有可用CPU核心
            all_cpus = list(range(psutil.cpu_count()))
            current_process.cpu_affinity(all_cpus)
            print(f"[性能優化] 使用所有CPU核心：{all_cpus}")
        
        # 設定線程優先級函數
        def set_thread_priority(thread_priority='high'):
            try:
                import win32process
                import win32api
                
                if thread_priority == 'realtime':
                    win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_TIME_CRITICAL)
                elif thread_priority == 'high':
                    win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_HIGHEST)
                else:
                    win32process.SetThreadPriority(win32api.GetCurrentThread(), win32process.THREAD_PRIORITY_NORMAL)
            except Exception as e:
                print(f"[性能優化] 設定線程優先級失敗：{e}")
        
        # 返回線程優先級設定函數
        return set_thread_priority
        
    except Exception as e:
        print(f"[性能優化] CPU性能優化失敗：{e}")
        return None

def optimize_onnx_session(config):
    """優化ONNX運行時設定"""
    try:
        # 設定ONNX運行時選項
        session_options = ort.SessionOptions()
        
        # 啟用所有優化
        session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        # 設定線程數量為CPU核心數
        session_options.intra_op_num_threads = psutil.cpu_count()
        session_options.inter_op_num_threads = psutil.cpu_count()
        
        # 設置執行模式為順序（對單個請求更快）
        session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        
        # 啟用記憶體優化
        session_options.enable_mem_pattern = True
        session_options.enable_cpu_mem_arena = True
        
        # 啟用 profiling（可選，用於調試）
        # session_options.enable_profiling = True
        
        print(f"[性能優化] ONNX使用 {psutil.cpu_count()} 個CPU核心，順序執行模式")
        return session_options
        
    except Exception as e:
        print(f"[性能優化] ONNX優化失敗：{e}")
        return None



def ai_logic_loop(config, model, model_type, boxes_queue, confidences_queue):
    """AI 推理和滑鼠控制的主要循環"""
    # 設定線程優先級
    set_thread_priority = optimize_cpu_performance(config)
    if set_thread_priority:
        thread_priority = getattr(config, 'thread_priority', 'high')
        set_thread_priority(thread_priority)
    
    screen_capture = mss.mss()
    
    # Run PyTorch models on CPU
    if model_type == 'pt':
        torch_device = getattr(config, 'torch_device', 'cpu')
        model.to(torch_device)
        config.current_provider = 'CPU'

    input_name = None
    if model_type == 'onnx':
        input_name = model.get_inputs()[0].name
        
    pid_x = PIDController(config.pid_kp_x, config.pid_ki_x, config.pid_kd_x)
    pid_y = PIDController(config.pid_kp_y, config.pid_ki_y, config.pid_kd_y)

    # 真正的配置緩存：避免每次循環都訪問 config 屬性
    last_pid_update = 0
    pid_check_interval = 1.0  # 每秒檢查一次PID參數變化
    
    # ddxoft 統計顯示控制
    last_ddxoft_stats_time = 0
    ddxoft_stats_interval = 30.0  # 每30秒顯示一次 ddxoft 統計
    
    # 音效提示相關變數
    last_sound_time = 0
    
    # 預計算常用值（真正減少重複計算）
    half_width = config.width // 2
    half_height = config.height // 2
    
    # 緩存滑鼠移動方式，避免每次循環都 getattr
    cached_mouse_move_method = getattr(config, 'mouse_move_method', 'mouse_event')
    last_method_check_time = 0
    method_check_interval = 2.0  # 每2秒檢查一次方法變更

    while config.Running:
        current_time = time.time()
        
        # 真正的緩存：定期更新 PID 和方法配置
        if current_time - last_pid_update > pid_check_interval:
            pid_x.Kp, pid_x.Ki, pid_x.Kd = config.pid_kp_x, config.pid_ki_x, config.pid_kd_x
            pid_y.Kp, pid_y.Ki, pid_y.Kd = config.pid_kp_y, config.pid_ki_y, config.pid_kd_y
            last_pid_update = current_time
        
        # 檢查滑鼠移動方式變更（使用緩存）
        if current_time - last_method_check_time > method_check_interval:
            new_method = getattr(config, 'mouse_move_method', 'mouse_event')
            if new_method != cached_mouse_move_method:
                cached_mouse_move_method = new_method
                print(f"[配置更新] 滑鼠移動方式已更新為: {cached_mouse_move_method}")
            last_method_check_time = current_time
        
        # ddxoft 統計顯示（使用緩存的方法）
        if cached_mouse_move_method == 'ddxoft' and current_time - last_ddxoft_stats_time > ddxoft_stats_interval:
            stats = get_ddxoft_statistics()
            if stats['total_count'] > 0:
                print(f"[ddxoft] 運行狀態報告 - 成功: {stats['success_count']}, 失敗: {stats['failure_count']}, 成功率: {stats['success_rate']:.1f}%")
            last_ddxoft_stats_time = current_time
        
        # 更新十字準心位置
        if config.fov_follow_mouse:
            try:
                x, y = win32api.GetCursorPos()
                config.crosshairX, config.crosshairY = x, y
            except Exception:
                config.crosshairX, config.crosshairY = half_width, half_height
        else:
            config.crosshairX, config.crosshairY = half_width, half_height

        # 檢查是否正在瞄準
        is_aiming = any(is_key_pressed(k) for k in config.AimKeys)
        
        if not config.AimToggle or (not config.keep_detecting and not is_aiming):
            # 清空檢測隊列
            try:
                while not boxes_queue.empty():
                    boxes_queue.get_nowait()
                while not confidences_queue.empty():
                    confidences_queue.get_nowait()
            except queue.Empty:
                pass
            boxes_queue.put([])
            confidences_queue.put([])
            time.sleep(0.05)  # 非活動時降低CPU使用率
            continue
            
        fov_size = config.fov_size
        crosshair_x, crosshair_y = config.crosshairX, config.crosshairY

        # 修改：檢測以FOV中心為中心，邊長為螢幕高度的正方形區域
        detection_size = config.height  # 正方形邊長等於螢幕高度
        half_detection_size = detection_size // 2

        # 計算檢測區域的左上角座標
        region_left = max(0, crosshair_x - half_detection_size)
        region_top = max(0, crosshair_y - half_detection_size)

        # 計算檢測區域的寬度和高度，確保不超出螢幕邊界
        region_width = min(detection_size, config.width - region_left)
        region_height = min(detection_size, config.height - region_top)

        region = {
            "left": region_left,
            "top": region_top,
            "width": region_width,
            "height": region_height,
        }

        try:
            game_frame = np.array(screen_capture.grab(region))
        except Exception:
            continue
        if game_frame.size == 0: 
            continue
        
        # AI 模型推理
        boxes, confidences = [], []
        
        if model_type == 'onnx':
            input_tensor = preprocess_image(game_frame, config.model_input_size)
            try:
                outputs = model.run(None, {input_name: input_tensor})
                boxes, confidences = postprocess_outputs(outputs, region['width'], region['height'], config.model_input_size, config.min_confidence, region['left'], region['top'])
                boxes, confidences = non_max_suppression(boxes, confidences)
            except Exception as e:
                print(f"ONNX 推理錯誤: {e}")
                continue
        elif model_type == 'pt':
            game_frame_rgb = cv2.cvtColor(game_frame, cv2.COLOR_BGRA2RGB)
            try:
                device = getattr(config, 'torch_device', 'cpu')
                results = model(game_frame_rgb, device=device, verbose=False)
                high_conf_indices = results[0].boxes.conf >= config.min_confidence
                boxes_np = results[0].boxes.xyxy[high_conf_indices].cpu().numpy()
                confidences = results[0].boxes.conf[high_conf_indices].cpu().numpy().tolist()

                # 將相對於檢測區域的座標轉換為螢幕絕對座標
                boxes_np[:, 0] += region['left']  # x1
                boxes_np[:, 1] += region['top']   # y1
                boxes_np[:, 2] += region['left']  # x2
                boxes_np[:, 3] += region['top']   # y2

                boxes = boxes_np.tolist()
            except Exception as e:
                print(f"PyTorch 推理錯誤: {e}")
                continue

        # boxes 已經是螢幕絕對座標
        absolute_boxes = boxes[:]
        
        # FOV過濾：只保留與FOV框有交集的人物框
        if absolute_boxes:
            fov_half = fov_size // 2
            fov_left = crosshair_x - fov_half
            fov_top = crosshair_y - fov_half
            fov_right = crosshair_x + fov_half
            fov_bottom = crosshair_y + fov_half
            
            filtered_boxes = []
            filtered_confidences = []
            
            for i, box in enumerate(absolute_boxes):
                x1, y1, x2, y2 = box
                # 矩形交集檢測
                if (x1 < fov_right and x2 > fov_left and 
                    y1 < fov_bottom and y2 > fov_top):
                    filtered_boxes.append(box)
                    if i < len(confidences):
                        filtered_confidences.append(confidences[i])
            
            absolute_boxes = filtered_boxes
            confidences = filtered_confidences

        # 單目標模式 - 只保留離準心最近的一個目標
        if config.single_target_mode and absolute_boxes:
            crosshair_x, crosshair_y = config.crosshairX, config.crosshairY
            closest_box = None
            min_distance_sq = float('inf')  # 使用距離平方，避免不必要的開方運算
            closest_confidence = 0
            
            for i, box in enumerate(absolute_boxes):
                abs_x1, abs_y1, abs_x2, abs_y2 = box
                # 計算邊界框中心點到準心的距離平方
                box_center_x = (abs_x1 + abs_x2) * 0.5
                box_center_y = (abs_y1 + abs_y2) * 0.5
                dx = box_center_x - crosshair_x
                dy = box_center_y - crosshair_y
                distance_sq = dx * dx + dy * dy  # 比較時不需要開方
                
                if distance_sq < min_distance_sq:
                    min_distance_sq = distance_sq
                    closest_box = box
                    closest_confidence = confidences[i] if i < len(confidences) else 0.5
            
            # 只保留最近的一個目標
            if closest_box:
                absolute_boxes = [closest_box]
                confidences = [closest_confidence]
            else:
                absolute_boxes = []
                confidences = []

        # 音效提示系統 - 檢測準心是否在敵人框內
        if not config.single_target_mode or not absolute_boxes:
            crosshair_x, crosshair_y = config.crosshairX, config.crosshairY
        target_detected = False
        
        if config.enable_sound_alert and absolute_boxes:
            for box in absolute_boxes:
                abs_x1, abs_y1, abs_x2, abs_y2 = box
                # 檢查準心是否在敵人框內
                if abs_x1 <= crosshair_x <= abs_x2 and abs_y1 <= crosshair_y <= abs_y2:
                    target_detected = True
                    break
            
            # 音效播放邏輯
            if target_detected:
                # 檢查音效間隔，避免過於頻繁播放
                if current_time - last_sound_time >= config.sound_interval / 1000.0:
                    try:
                        # 異步播放音效，避免阻塞主線程
                        threading.Thread(
                            target=winsound.Beep, 
                            args=(config.sound_frequency, config.sound_duration),
                            daemon=True
                        ).start()
                        last_sound_time = current_time
                    except Exception as e:
                        pass  # 忽略音效播放錯誤

        if is_aiming and absolute_boxes:
            # 讀取瞄準參數
            aim_part = config.aim_part
            head_height_ratio = config.head_height_ratio
            head_width_ratio = config.head_width_ratio
            body_width_ratio = config.body_width_ratio
            
            valid_targets = []
            for box in absolute_boxes:
                abs_x1, abs_y1, abs_x2, abs_y2 = box
                box_w, box_h = abs_x2 - abs_x1, abs_y2 - abs_y1
                box_center_x = abs_x1 + box_w * 0.5
                
                # 計算瞄準點
                if aim_part == "head":
                    target_x = box_center_x
                    target_y = abs_y1 + box_h * head_height_ratio * 0.5
                else: # "body"
                    target_x = box_center_x
                    head_h = box_h * head_height_ratio
                    target_y = (abs_y1 + head_h + abs_y2) * 0.5

                moveX = target_x - crosshair_x
                moveY = target_y - crosshair_y
                distance_sq = moveX * moveX + moveY * moveY  # 使用距離平方進行排序
                valid_targets.append((distance_sq, moveX, moveY))

            if valid_targets:
                valid_targets.sort(key=lambda x: x[0])
                _, errorX, errorY = valid_targets[0]
                dx, dy = pid_x.update(errorX), pid_y.update(errorY)
                if abs(dx) > 0 or abs(dy) > 0:
                    # 使用緩存的滑鼠移動方式
                    send_mouse_move(int(dx), int(dy), method=cached_mouse_move_method)
            else:
                pid_x.reset()
                pid_y.reset()
        else:
            pid_x.reset()
            pid_y.reset()

        # 更新檢測結果隊列
        try:
            if boxes_queue.full():
                boxes_queue.get_nowait()
            if confidences_queue.full():
                confidences_queue.get_nowait()
        except queue.Empty:
            pass
            
        boxes_queue.put(absolute_boxes)
        confidences_queue.put(confidences)

        # 控制檢測頻率
        time.sleep(config.detect_interval)

def auto_fire_loop(config, boxes_queue):
    """自動開火功能的獨立循環"""
    # 設定線程優先級
    set_thread_priority = optimize_cpu_performance(config)
    if set_thread_priority:
        thread_priority = getattr(config, 'thread_priority', 'high')
        set_thread_priority(thread_priority)
    
    last_key_state = False
    delay_start_time = None
    last_fire_time = 0
    cached_boxes = []
    last_box_update = 0
    
    BOX_UPDATE_INTERVAL = 1 / 60  # 60Hz更新頻率
    
    # 緩存按鍵配置
    auto_fire_key = config.auto_fire_key
    auto_fire_key2 = getattr(config, 'auto_fire_key2', None)
    last_key_update = 0
    key_update_interval = 0.5  # 每0.5秒檢查一次按鍵配置變化
    
    while config.Running:
        current_time = time.time()
        
        # 定期更新按鍵配置
        if current_time - last_key_update > key_update_interval:
            auto_fire_key = config.auto_fire_key
            auto_fire_key2 = getattr(config, 'auto_fire_key2', None)
            last_key_update = current_time
        
        # 檢查按鍵狀態
        key_state = is_key_pressed(auto_fire_key)
        if auto_fire_key2:
            key_state = key_state or is_key_pressed(auto_fire_key2)

        # 處理按鍵狀態變化
        if key_state and not last_key_state:
            delay_start_time = current_time
        
        if key_state:
            # 檢查開鏡延遲
            if delay_start_time and (current_time - delay_start_time >= config.auto_fire_delay):
                # 檢查射擊冷卻時間
                if current_time - last_fire_time >= config.auto_fire_interval:
                    
                    # 更新檢測框緩存
                    if current_time - last_box_update >= BOX_UPDATE_INTERVAL:
                        try:
                            # 從隊列中獲取最新的檢測結果（不消耗隊列）
                            if not boxes_queue.empty():
                                cached_boxes = boxes_queue.queue[-1]
                                last_box_update = current_time
                        except IndexError:
                            # 隊列為空，使用舊的緩存
                            pass
                    
                    # 判斷是否應該開火
                    if cached_boxes:
                        crosshair_x, crosshair_y = config.crosshairX, config.crosshairY
                        target_part = config.auto_fire_target_part
                        head_height_ratio = config.head_height_ratio
                        head_width_ratio = config.head_width_ratio
                        body_width_ratio = config.body_width_ratio
                        
                        # 射擊判斷
                        should_fire = False
                        for box in cached_boxes:
                            x1, y1, x2, y2 = box
                            box_w, box_h = x2 - x1, y2 - y1
                            box_center_x = x1 + box_w * 0.5
                            
                            # 邊界檢查
                            if target_part == "head":
                                head_h = box_h * head_height_ratio
                                head_w = box_w * head_width_ratio
                                head_x1 = box_center_x - head_w * 0.5
                                head_x2 = box_center_x + head_w * 0.5
                                head_y2 = y1 + head_h
                                should_fire = (head_x1 <= crosshair_x <= head_x2 and y1 <= crosshair_y <= head_y2)
                            elif target_part == "body":
                                body_w = box_w * body_width_ratio
                                body_x1 = box_center_x - body_w * 0.5
                                body_x2 = box_center_x + body_w * 0.5
                                body_y1 = y1 + box_h * head_height_ratio
                                should_fire = (body_x1 <= crosshair_x <= body_x2 and body_y1 <= crosshair_y <= y2)
                            elif target_part == "both":
                                # 檢查頭部和身體區域
                                head_h = box_h * head_height_ratio
                                head_w = box_w * head_width_ratio
                                head_x1 = box_center_x - head_w * 0.5
                                head_x2 = box_center_x + head_w * 0.5
                                
                                is_in_head = (head_x1 <= crosshair_x <= head_x2 and y1 <= crosshair_y <= y1 + head_h)
                                
                                if not is_in_head:
                                    body_w = box_w * body_width_ratio
                                    body_x1 = box_center_x - body_w * 0.5
                                    body_x2 = box_center_x + body_w * 0.5
                                    body_y1 = y1 + head_h
                                    is_in_body = (body_x1 <= crosshair_x <= body_x2 and body_y1 <= crosshair_y <= y2)
                                    should_fire = is_in_body
                                else:
                                    should_fire = True

                            if should_fire:
                                # 執行射擊
                                mouse_click_method = getattr(config, 'mouse_click_method', 'mouse_event')
                                send_mouse_click(mouse_click_method)
                                last_fire_time = current_time
                                break
        else:
            delay_start_time = None
            if cached_boxes:
                cached_boxes = []

        last_key_state = key_state
        
        time.sleep(1 / 60)



def aim_toggle_key_listener(config, update_gui_callback=None):
    """持續監聽自動瞄準開關快捷鍵"""
    # 設定線程優先級
    set_thread_priority = optimize_cpu_performance(config)
    if set_thread_priority:
        thread_priority = getattr(config, 'thread_priority', 'high')
        set_thread_priority(thread_priority)
    
    last_state = False
    key_code = getattr(config, 'aim_toggle_key', 0x78)  # 默認 F9 鍵
    
    # 獲取按鍵名稱
    from win_utils import get_vk_name
    key_name = get_vk_name(key_code)
    
    sleep_interval = 0.03  # 30ms 檢查間隔
    
    
    while config.Running:
        try:
            # 重新獲取快捷鍵設置
            current_key_code = getattr(config, 'aim_toggle_key', 0x78)
            if current_key_code != key_code:
                key_code = current_key_code
                key_name = get_vk_name(key_code)
            
            # 檢測按鍵狀態
            state = bool(win32api.GetAsyncKeyState(key_code) & 0x8000)
            
            # 檢測按鍵按下事件
            if state and not last_state:
                old_state = config.AimToggle
                config.AimToggle = not config.AimToggle
                print(f"[快捷鍵] 自動瞄準: {old_state} → {config.AimToggle}")
                
                if update_gui_callback:
                    update_gui_callback(config.AimToggle)
            
            last_state = state
            
        except Exception as e:
            print(f"[快捷鍵監聽] 錯誤: {e}")
            import traceback
            traceback.print_exc()
        
        time.sleep(sleep_interval)

if __name__ == "__main__":
    # 檢查管理員權限
    check_and_request_admin()

    # Ensure ddxoft loads only after admin privileges are confirmed
    ensure_ddxoft_ready()
    
    # 在程序開始時檢測 Windows 縮放比例
    if not check_windows_scaling():
        sys.exit(1)
    
    config = Config()
    load_config(config)
    
    # 調試：顯示載入的滑鼠移動方式
    print(f"[配置載入] 滑鼠移動方式: {getattr(config, 'mouse_move_method', 'mouse_event')}")
    
    # 如果使用 ddxoft，進行功能測試
    if getattr(config, 'mouse_move_method', 'mouse_event') == 'ddxoft':
        test_ddxoft_functions()
    
    # 在程序開始時優化CPU性能
    optimize_cpu_performance(config)

    # 優化：使用配置中的隊列大小設置
    max_queue_size = getattr(config, 'max_queue_size', 3)
    boxes_queue = queue.Queue(maxsize=max_queue_size)
    confidences_queue = queue.Queue(maxsize=max_queue_size)

    def start_ai_threads(model_path):
        """由 GUI 呼叫，載入模型並啟動/重啟 AI 執行緒"""
        global ai_thread, auto_fire_thread, config
        
        # 停止現有線程
        if ai_thread is not None and ai_thread.is_alive():
            config.Running = False
            ai_thread.join()
            if auto_fire_thread is not None:
                auto_fire_thread.join()

        config.Running = True
        
        model, model_type = None, ''
        if model_path.endswith('.onnx'):
            model_type = 'onnx'
            try:
                # 嘗試使用GPU，如果失敗則回退到CPU
                providers = ['DmlExecutionProvider', 'CPUExecutionProvider']

                # 獲取優化的會話選項
                session_options = optimize_onnx_session(config)
                if session_options:
                    model = ort.InferenceSession(model_path, providers=providers, sess_options=session_options)
                else:
                    model = ort.InferenceSession(model_path, providers=providers)

                # 獲取實際使用的提供者
                actual_providers = model.get_providers()
                config.current_provider = actual_providers[0] if actual_providers else 'CPUExecutionProvider'
            except Exception as e:
                print(f"載入 ONNX 模型失敗: {e}"); return False
        elif model_path.endswith('.pt'):
            model_type = 'pt'
            try:
                cpu_device = 'cpu'
                model = YOLO(model_path)
                model.to(cpu_device)
                config.torch_device = cpu_device
                config.current_provider = 'CPU'
                with torch.no_grad():
                    model(np.zeros((640, 640, 3), dtype=np.uint8), verbose=False, device=cpu_device)  # 預熱
            except Exception as e:
                print(f"載入 PyTorch 模型失敗: {e}"); return False
        else:
            print(f"錯誤: 不支援的模型格式: {model_path}"); return False

        ai_thread = threading.Thread(target=ai_logic_loop, args=(config, model, model_type, boxes_queue, confidences_queue), daemon=True)
        auto_fire_thread = threading.Thread(target=auto_fire_loop, args=(config, boxes_queue), daemon=True)
        
        ai_thread.start()
        auto_fire_thread.start()
        return True

    # 啟動設置 GUI
    settings_thread = threading.Thread(target=create_settings_gui, args=(config, start_ai_threads), daemon=True)
    settings_thread.start()
    
    # 確保配置完全載入後再啟動快捷鍵監聽
    time.sleep(0.5)  # 等待 GUI 完全初始化
    
    # 啟動快捷鍵監聽（在 GUI 啟動後）
    toggle_thread = threading.Thread(target=aim_toggle_key_listener, args=(config,), daemon=True)
    toggle_thread.start()

    
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    
    # 建立並顯示主要的繪圖覆蓋層 (人物框, FOV)
    main_overlay = PyQtOverlay(boxes_queue, confidences_queue, config)
    main_overlay.show()

    # 建立並顯示新的狀態面板
    status_panel = StatusPanel(config)
    status_panel.show()
    
    # 啟動 PyQt 應用程式事件循環，這會管理所有 PyQt 視窗
    sys.exit(app.exec())
