<div align="center">
   
[![GitHub stars](https://img.shields.io/github/stars/iishong0w0/Axiom-AI?style=social)](https://github.com/iishong0w0/Axiom-AI/stargazers)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-PolyForm--Noncommercial%201.0.0-blueviolet.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/iishong0w0/Axiom-AI)
![Repo Size](https://img.shields.io/github/repo-size/iishong0w0/Axiom-AI)

# [**>> Download Latest Release <<**](https://github.com/iishong0w0/Axiom-AI/releases/latest)
# [Discord Community](https://discord.gg/h4dEh3b8Bt)  

![Control Panel](https://raw.githubusercontent.com/iisHong0w0/Axiom-AI/refs/heads/main/%E9%9D%A2%E6%9D%BF.png)

# **If this project helps you, please give us a ⭐ Star!**

[English](#english) | [中文](#中文)

</div>

---

# English

## 🎯 Overview

**Axiom AI** is a sophisticated computer vision application designed for real-time object detection and interaction. Built with advanced AI technology and optimized for high-performance operation, Axiom AI provides intelligent assistance to enhance gaming experiences for users who need it most.

### 🌟 Who Is Axiom For?

Axiom is designed for gamers who are at a disadvantage compared to regular players, including but not limited to:
- Players with **physical disabilities** (hand tremors, Parkinson's disease, neurological disorders, paralysis)
- Players with **visual impairments** (colorblindness, poor vision, nystagmus, blind players)
- Players with **cognitive challenges** (ADHD, autism, anxiety disorders, spatial perception disorders)
- Players with **medical conditions** (chronic fatigue syndrome, brain injury sequelae, sleep deprivation)
- Players with **hardware limitations** (poor FPS performance, low-quality peripherals, cloud gaming)
- Players with **environmental constraints** (no air conditioning, limited mouse space, poor ergonomics)
- **Beginners** and untrained players who want to learn and improve
- Players grieving from parental loss or experiencing emotional challenges

**⚠️ Important Notice**: This software is licensed under the PolyForm Noncommercial License 1.0.0. **Commercial use is strictly prohibited.**

---

## ✨ Key Features

### 🤖 AI-Powered Detection
- **YOLO-based object detection** with ONNX and PyTorch (.pt) model support
- **Real-time inference** with DirectML acceleration
- **Customizable confidence threshold** for detection accuracy
- **Single target mode** to focus on the nearest enemy

### 🎯 Intelligent Targeting System
- **PID controller** for smooth and accurate mouse movement
- **Separate X/Y axis tuning** for precise control
- **Multiple aiming modes**: Head, body, or both
- **FOV (Field of View) system** with mouse tracking
- **Adjustable detection region** based on screen center

### 🖱️ Advanced Mouse Control
- **Multiple mouse movement methods**: `mouse_event`, `ddxoft`
- **Multiple mouse click methods** for compatibility
- **Auto-fire functionality** with configurable delay and interval
- **Customizable hotkeys** for all actions

### 🎨 Visual Feedback
- **PyQt6-based overlay** showing detection boxes
- **FOV indicator** for visual reference
- **Confidence score display** for detected objects
- **Real-time status panel** with FPS and detection info
- **Color-coded target markers** for different aim parts

### ⚡ Performance Optimization
- **CPU optimization** with adjustable process/thread priority
- **Multi-core support** with CPU affinity settings
- **Optimized ONNX runtime** configuration
- **Minimal latency** detection pipeline
- **Performance mode** for maximum responsiveness

### 🔊 Additional Features
- **Sound alerts** when target is detected
- **Keep detecting mode** for continuous operation
- **Configurable detection interval**
- **Automatic Windows scaling detection**
- **Multi-language support** (English, 中文)

---

## 🧠 Tech Stack

- **Programming Language**: Python 3.11+
- **GUI Framework**: PyQt6
- **Computer Vision**: Ultralytics YOLOv8, ONNX Runtime (DirectML), OpenCV
- **Screen Capture**: MSS (Multiple Screen Shots)
- **Numerical Computing**: NumPy, PyTorch (CPU)
- **System Integration**: pywin32, psutil, custom `ddxoft.dll`
- **Packaging & Distribution**: PyInstaller (optional), Windows batch launcher

Additional dependencies are listed in [`requirements.txt`](requirements.txt).

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit) or higher
- **Python**: 3.11 or higher
- **RAM**: 16GB
- **Graphics**: GTX 1060 / RX 580 or equivalent
- **Storage**: 500MB free space

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **Python**: 3.11+
- **RAM**: 32GB or higher
- **Graphics**: RTX 3060 or better
- **Storage**: 1GB free space

---

## 🚀 Installation Guide

### Option 1: Quick Install (Recommended for Beginners)

1. **Download the Latest Release**
   - Visit the [Releases page](https://github.com/iishong0w0/Axiom-AI/releases/latest)
   - Download the latest ZIP file

2. **Install Python**
   - Run the included `python-3.11.0-amd64.exe` installer
   - ⚠️ **IMPORTANT**: Check "Add python.exe to PATH" during installation
   - Complete the installation wizard

3. **Launch Axiom AI**
   - Extract the downloaded ZIP file to a folder
   - Double-click `啟動Launcher.bat` to start the application
   - The launcher will automatically install dependencies on first run

### Option 2: Manual Installation (For Developers)

```bash
# Clone the repository
git clone https://github.com/iishong0w0/Axiom-AI.git
cd Axiom-AI

# Create a virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to src directory and run
cd src
python main.py
```

### Verify Installation

After installation, you should see:
- ✅ Main GUI window with control panel
- ✅ Status panel showing FPS and detection info
- ✅ No error messages in the console

If you encounter issues, see the [Troubleshooting](#troubleshooting) section.

---

## 🎮 Quick Start Guide

### Basic Usage

1. **Launch the Application**
   ```bash
   # From the src directory
   python main.py
   ```

2. **Initial Setup**
   - The application will automatically detect your screen resolution
   - A settings GUI will appear with default configurations
   - The overlay will start showing FOV and detection boxes

3. **Configure Your Model**
   - Click on the model dropdown in the settings panel
   - Select your desired AI model (`.onnx` or `.pt` files from the `模型` folder)
   - Default model: `Roblox.onnx` (640x640 input size)

4. **Adjust Detection Settings**
   - **FOV Size**: Adjust the field of view (default: 222px)
   - **Confidence Threshold**: Set minimum detection confidence (default: 0.11)
   - **Aim Part**: Choose target area (head/body/both)
   - **Single Target Mode**: Enable to track only the closest enemy

5. **Configure Hotkeys**
   - **Aim Keys**: Mouse buttons to activate aiming (default: Left Click, Right Click, X2 Button)
   - **Toggle Key**: Press `Insert` to enable/disable the system
   - **Auto-Fire Key**: Configure automatic shooting (default: X2 Button)

6. **Start Detection**
   - Press `Insert` to toggle the AI detection on/off
   - Hold one of the configured aim keys to activate targeting
   - Visual feedback will appear showing detected objects and FOV

### Advanced Configuration

#### PID Controller Tuning

Fine-tune mouse movement smoothness:

```
Kp (Proportional): Controls response speed (default: 0.26)
Ki (Integral):     Corrects steady-state error (default: 0.0)
Kd (Derivative):   Reduces overshoot and oscillation (default: 0.0)
```

- **Higher Kp**: Faster response, may cause overshoot
- **Higher Ki**: Better accuracy, may cause instability
- **Higher Kd**: Smoother movement, may reduce responsiveness

#### Performance Optimization

Enable high-performance mode:
- Set **Process Priority** to "High" or "Realtime"
- Set **Thread Priority** to "High"
- Enable **CPU Optimization**
- Reduce **Detection Interval** (minimum: 1ms)

#### Mouse Control Methods

- **mouse_event**: Standard Windows API (compatible with most games)
- **ddxoft**: Hardware-level mouse driver (requires admin rights)

---

## ⚙️ Configuration Reference

### Main Configuration File: `config.json`

The application saves all settings to `src/config.json`. Here are the key parameters:

```json
{
  "fov_size": 222,                    // Field of view size in pixels
  "min_confidence": 0.11,             // Minimum detection confidence (0.0-1.0)
  "aim_part": "head",                 // Target part: "head", "body", "both"
  "single_target_mode": true,         // Track only closest target
  "keep_detecting": true,             // Always detect (even when not aiming)
  "fov_follow_mouse": true,           // FOV follows mouse cursor
  
  // PID Controller (X-axis)
  "pid_kp_x": 0.26,
  "pid_ki_x": 0.0,
  "pid_kd_x": 0.0,
  
  // PID Controller (Y-axis)
  "pid_kp_y": 0.26,
  "pid_ki_y": 0.0,
  "pid_kd_y": 0.0,
  
  // Hotkeys (Virtual Key Codes)
  "AimKeys": [1, 6, 2],               // 0x01=Left Click, 0x06=X2, 0x02=Right Click
  "aim_toggle_key": 45,               // Insert key
  "auto_fire_key": 6,                 // X2 button
  "auto_fire_key2": 4,                // Middle mouse button
  
  // Auto-Fire Settings
  "auto_fire_delay": 0.0,             // Delay before shooting (seconds)
  "auto_fire_interval": 0.08,         // Time between shots (seconds)
  "auto_fire_target_part": "both",    // Auto-fire target preference
  
  // Performance Settings
  "detect_interval": 0.01,            // Detection loop delay (seconds)
  "cpu_optimization": true,           // Enable CPU optimizations
  "process_priority": "high",         // "normal", "high", "realtime"
  "thread_priority": "high",          // Thread priority level
  
  // Sound Alerts
  "enable_sound_alert": false,        // Enable beep on target detection
  "sound_frequency": 1000,            // Beep frequency (Hz)
  "sound_duration": 100,              // Beep duration (ms)
  "sound_interval": 200,              // Minimum time between beeps (ms)
  
  // Visual Settings
  "show_fov": true,                   // Show FOV circle
  "show_boxes": true,                 // Show detection boxes
  "show_confidence": true,            // Show confidence scores
  "show_status_panel": true,          // Show status overlay
  
  // Target Area Ratios
  "head_width_ratio": 0.38,           // Head region width (0.0-1.0)
  "head_height_ratio": 0.26,          // Head region height (0.0-1.0)
  "body_width_ratio": 0.87,           // Body region width (0.0-1.0)
  
  // Mouse Control
  "mouse_move_method": "mouse_event", // "mouse_event" or "ddxoft"
  "mouse_click_method": "ddxoft"      // Mouse click method
}
```

### Environment Variables

No environment variables are required. All configuration is done through `config.json` and the settings GUI.

---

## 📁 Project Structure

```
Axiom-AI_Aimbot/
├── src/                          # Source code directory
│   ├── main.py                   # Main application entry point
│   ├── config.py                 # Configuration class and management
│   ├── config.json               # User settings file
│   ├── inference.py              # AI inference and preprocessing
│   ├── win_utils.py              # Windows API utilities
│   ├── overlay.py                # PyQt6 overlay for visual feedback
│   ├── settings_gui.py           # Settings GUI interface
│   ├── status_panel.py           # Status panel overlay
│   ├── about.py                  # About dialog
│   ├── preset_manager.py         # Configuration preset manager
│   ├── config_manager.py         # Advanced configuration management
│   ├── language_manager.py       # Multi-language support
│   ├── language_data.py          # Language strings database
│   ├── scaling_warning_dialog.py # Windows scaling detection
│   ├── ddxoft.dll                # Hardware mouse driver library
│   ├── logo.ico                  # Application icon
│   └── 模型/                     # AI models directory
│       └── *.onnx, *.pt          # YOLO models
├── requirements.txt              # Python dependencies
├── LICENSE                       # PolyForm Noncommercial License
├── README.md                     # This file
├── 啟動Launcher.bat              # Windows launcher script
├── 常見問題FAQ.txt               # Frequently Asked Questions
├── 面板.png                      # Screenshot for documentation
├── python-3.11.0-amd64.exe       # Python installer (bundled)
└── index.html                    # Web interface (optional)
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### ❌ Application Won't Start

**Problem**: Double-clicking launcher does nothing or shows errors.

**Solutions**:
1. Ensure Python 3.11+ is installed
2. Verify "Add python.exe to PATH" was checked during installation
3. Reinstall Python with correct options
4. Try running from command line: `cd src && python main.py`

#### ❌ ModuleNotFoundError

**Problem**: Missing Python package errors.

**Solution**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

#### ❌ No Detection / Low FPS

**Problem**: AI detection not working or very slow.

**Solutions**:
1. Check if model file exists in `src/模型/` directory
2. Lower FOV size for better performance
3. Increase `detect_interval` (e.g., 0.02 or 0.03)
4. Close other resource-intensive applications
5. Ensure GPU drivers are up to date
6. Try switching to a smaller model file

#### ❌ Mouse Not Moving

**Problem**: Detection works but mouse doesn't move.

**Solutions**:
1. Check if aim keys are properly configured
2. Verify anti-cheat software isn't blocking input
3. Try switching `mouse_move_method` to "ddxoft"
4. Run application as Administrator (required for some games)
5. Increase PID Kp value for more aggressive movement

#### ❌ Access Denied / Permission Errors

**Problem**: Application requires administrator rights.

**Solution**:
- Right-click launcher or `main.py` and select "Run as Administrator"
- Some mouse control methods require elevated privileges

#### ❌ Overlay Not Visible

**Problem**: FOV and boxes not showing.

**Solutions**:
1. Check `show_fov` and `show_boxes` settings
2. Ensure game is in Windowed or Borderless mode (not Fullscreen)
3. Try Alt+Tab to refresh overlay
4. Disable Windows Game Bar and overlays

#### ❌ High CPU Usage

**Problem**: Application uses too much CPU.

**Solutions**:
1. Increase `detect_interval` (default: 0.01 → 0.03)
2. Reduce FOV size
3. Disable `keep_detecting` mode
4. Close status panel (set `show_status_panel: false`)

---

## 🤝 Contributing

We welcome contributions to improve Axiom AI! Here's how you can help:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Axiom-AI.git
cd Axiom-AI

# Create a branch for your feature
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt

# Make your changes and test thoroughly

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### Contribution Guidelines

- **Code Style**: Follow existing Python conventions (PEP 8)
- **Documentation**: Update README if adding new features
- **Testing**: Test on multiple Windows versions and hardware
- **Language**: Support both English and Chinese in UI elements
- **Performance**: Ensure changes don't negatively impact FPS
- **License**: All contributions must comply with PolyForm Noncommercial License

### Areas for Contribution

- 🐛 Bug fixes and stability improvements
- ⚡ Performance optimizations
- 🎨 UI/UX enhancements
- 📚 Documentation and tutorials
- 🌐 Translations to other languages
- 🤖 New AI models and training data
- 🎮 Game-specific profiles and presets

---

## 📄 License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**.

### Key Restrictions:

- ❌ **No Commercial Use**: This software cannot be used for any commercial purpose
- ❌ **No Selling**: Cannot sell or charge for the software or services using it
- ❌ **No Business Use**: Cannot use in connection with any business activity
- ✅ **Personal Use**: Free for personal, educational, and research purposes
- ✅ **Modification**: You may modify and distribute the software
- ✅ **Attribution**: Must include original license and copyright notice

### What Counts as Commercial Use?

- Using the software to provide paid services
- Using the software as part of a commercial product
- Using the software to generate revenue (directly or indirectly)
- Using the software in any business, even if you don't charge for it

### What Is Allowed?

- Personal gaming and entertainment
- Educational purposes and learning
- Research and development
- Sharing with friends (non-commercial)

For full license details, see [LICENSE](LICENSE) or visit [PolyForm Noncommercial License](https://polyformproject.org/licenses/noncommercial/1.0.0/).

---

## 📞 Contact & Support

### Support Channels

- **Discord Server**: [Join our community](https://discord.gg/h4dEh3b8Bt) - For general support, discussions, and community help
- **GitHub Issues**: [Report bugs](https://github.com/iishong0w0/Axiom-AI/issues) - For bug reports and feature requests
- **Email**: [iis20160512@gmail.com](mailto:iis20160512@gmail.com) - For direct communication with the developer

### Links

- **GitHub**: [@iishong0w0](https://github.com/iishong0w0)
- **Repository**: [Axiom-AI](https://github.com/iishong0w0/Axiom-AI)
- **Releases**: [Latest Version](https://github.com/iishong0w0/Axiom-AI/releases/latest)

---

## 📝 Frequently Asked Questions (FAQ)

**Q: Is this a cheat/hack?**  
A: Axiom AI is an accessibility tool designed to help players with disabilities. Use responsibly and in accordance with game terms of service.

**Q: Will I get banned for using this?**  
A: We cannot guarantee safety in any online game. Use at your own risk and follow game rules.

**Q: Can I use this for competitive play?**  
A: This tool is intended for casual play and accessibility. Competitive use may violate tournament rules.

**Q: Which games are supported?**  
A: Axiom AI is model-agnostic and can work with any game if you have a trained YOLO model. Default model is for Roblox.

**Q: How do I train my own model?**  
A: You'll need to create a dataset and train a YOLOv8 model. See [Ultralytics documentation](https://docs.ultralytics.com) for details.

**Q: Why is detection slow on my system?**  
A: Try reducing FOV size, increasing detection interval, or closing background applications. Ensure you meet minimum system requirements.

**Q: Can I run this on Linux/Mac?**  
A: Currently, Axiom AI is Windows-only due to Windows-specific APIs. Linux/Mac support may come in the future.

**Q: How can I improve accuracy?**  
A: Adjust confidence threshold, tune PID parameters, use a better trained model, or increase FOV size.

---

## ⚠️ Disclaimer

**This software is provided "as is" without warranty of any kind.** Use at your own risk. The developers are not responsible for:
- Any consequences of using this software
- Bans or penalties in online games
- Hardware or software damage
- Violation of terms of service

**Users are solely responsible for ensuring their use complies with applicable laws and game terms of service.**

---

## 🙏 Acknowledgments

- **Ultralytics YOLOv8**: For the amazing object detection framework
- **ONNX Runtime**: For optimized model inference
- **PyQt6**: For the overlay system
- **Community Contributors**: For bug reports, suggestions, and support

---

**Copyright © 2025 iisHong0w0. All rights reserved.**

---
---

# 中文

## 🎯 項目概述

**Axiom AI** 是一款先進的計算機視覺應用程序，專為實時對象檢測和交互而設計。基於先進的 AI 技術並針對高性能運行進行優化，Axiom AI 為最需要幫助的用戶提供智能輔助，以增強遊戲體驗。

### 🌟 Axiom 適合誰使用？

Axiom 專為相比普通玩家處於劣勢的遊戲玩家設計，包括但不限於：
- **身體殘疾**的玩家（手部顫抖、帕金森病、神經系統疾病、癱瘓）
- **視覺障礙**的玩家（色盲、視力不佳、眼球震顫、失明玩家）
- **認知挑戰**的玩家（ADHD、自閉症、焦慮症、空間感知障礙）
- **醫療狀況**的玩家（慢性疲勞綜合症、腦損傷後遺症、睡眠不足）
- **硬件限制**的玩家（FPS 性能差、低質量外設、雲遊戲）
- **環境限制**的玩家（無空調、鼠標空間有限、人體工學不佳）
- 想要學習和提高的**新手**和未經訓練的玩家
- 因失去親人而悲傷或遇到情緒挑戰的玩家

**⚠️ 重要提示**：本軟件採用 PolyForm 非商業許可證 1.0.0。**嚴禁商業使用。**

---

## ✨ 主要功能

### 🤖 AI 驅動檢測
- **基於 YOLO 的對象檢測**，支持 ONNX 和 PyTorch (.pt) 模型
- **實時推理**，支持 DirectML 加速
- **可自定義置信度閾值**以提高檢測準確度
- **單目標模式**專注於最近的敵人

### 🎯 智能瞄準系統
- **PID 控制器**實現平滑準確的鼠標移動
- **獨立 X/Y 軸調整**實現精確控制
- **多種瞄準模式**：頭部、身體或兩者
- **FOV（視野）系統**帶鼠標跟踪
- 基於屏幕中心的**可調整檢測區域**

### 🖱️ 高級鼠標控制
- **多種鼠標移動方法**：`mouse_event`、`ddxoft`
- **多種鼠標點擊方法**以實現兼容性
- **自動射擊功能**，可配置延遲和間隔
- 所有操作的**可自定義熱鍵**

### 🎨 視覺反饋
- **基於 PyQt6 的覆蓋層**顯示檢測框
- **FOV 指示器**提供視覺參考
- 檢測對象的**置信度分數顯示**
- 帶 FPS 和檢測信息的**實時狀態面板**
- 不同瞄準部位的**彩色目標標記**

### ⚡ 性能優化
- **CPU 優化**，可調整進程/線程優先級
- **多核支持**，帶 CPU 親和性設置
- **優化的 ONNX 運行時**配置
- **最小延遲**檢測管道
- **性能模式**實現最大響應速度

### 🔊 附加功能
- 檢測到目標時的**聲音警報**
- **持續檢測模式**用於連續操作
- **可配置的檢測間隔**
- **自動 Windows 縮放檢測**
- **多語言支持**（English、中文）

---

## 🧠 技術棧

- **編程語言**：Python 3.11+
- **GUI 框架**：PyQt6
- **計算機視覺**：Ultralytics YOLOv8、ONNX Runtime（DirectML）、OpenCV
- **屏幕捕獲**：MSS（Multiple Screen Shots）
- **數值計算**：NumPy、PyTorch（CPU）
- **系統集成**：pywin32、psutil、自定義 `ddxoft.dll`
- **打包與分發**：PyInstaller（可選）、Windows 批處理啟動器

其他依賴項列在 [`requirements.txt`](requirements.txt) 中。

---

## 💻 系統要求

### 最低要求
- **操作系統**：Windows 10（64 位）或更高版本
- **Python**：3.11 或更高版本
- **內存**：16GB
- **顯卡**：GTX 1060 / RX 580 或同等級別
- **存儲空間**：500MB 可用空間

### 推薦配置
- **操作系統**：Windows 11（64 位）
- **Python**：3.11+
- **內存**：32GB 或更高
- **顯卡**：RTX 3060 或更好
- **存儲空間**：1GB 可用空間

---

## 🚀 安裝指南

### 方式 1：快速安裝（推薦新手使用）

1. **下載最新版本**
   - 訪問[發布頁面](https://github.com/iishong0w0/Axiom-AI/releases/latest)
   - 下載最新的 ZIP 文件

2. **安裝 Python**
   - 運行附帶的 `python-3.11.0-amd64.exe` 安裝程序
   - ⚠️ **重要**：安裝過程中勾選「Add python.exe to PATH」
   - 完成安裝向導

3. **啟動 Axiom AI**
   - 將下載的 ZIP 文件解壓到一個文件夾
   - 雙擊 `啟動Launcher.bat` 啟動應用程序
   - 啟動器會在首次運行時自動安裝依賴項

### 方式 2：手動安裝（開發者使用）

```bash
# 克隆存儲庫
git clone https://github.com/iishong0w0/Axiom-AI.git
cd Axiom-AI

# 創建虛擬環境（推薦）
python -m venv .venv

# 激活虛擬環境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安裝依賴項
pip install -r requirements.txt

# 進入 src 目錄並運行
cd src
python main.py
```

### 驗證安裝

安裝後，您應該看到：
- ✅ 帶控制面板的主 GUI 窗口
- ✅ 顯示 FPS 和檢測信息的狀態面板
- ✅ 控制台中沒有錯誤消息

如果遇到問題，請參閱[故障排除](#故障排除)部分。

---

## 🎮 快速開始指南

### 基本使用

1. **啟動應用程序**
   ```bash
   # 從 src 目錄
   python main.py
   ```

2. **初始設置**
   - 應用程序會自動檢測您的屏幕分辨率
   - 將出現帶有默認配置的設置 GUI
   - 覆蓋層將開始顯示 FOV 和檢測框

3. **配置您的模型**
   - 點擊設置面板中的模型下拉菜單
   - 從 `模型` 文件夾中選擇您想要的 AI 模型（`.onnx` 或 `.pt` 文件）
   - 默認模型：`Roblox.onnx`（640x640 輸入大小）

4. **調整檢測設置**
   - **FOV 大小**：調整視野範圍（默認：222px）
   - **置信度閾值**：設置最小檢測置信度（默認：0.11）
   - **瞄準部位**：選擇目標區域（頭部/身體/兩者）
   - **單目標模式**：啟用以僅跟踪最近的敵人

5. **配置熱鍵**
   - **瞄準鍵**：激活瞄準的鼠標按鈕（默認：左鍵、右鍵、X2 按鈕）
   - **切換鍵**：按 `Insert` 啟用/禁用系統
   - **自動射擊鍵**：配置自動射擊（默認：X2 按鈕）

6. **開始檢測**
   - 按 `Insert` 切換 AI 檢測開/關
   - 按住其中一個配置的瞄準鍵以激活目標定位
   - 將出現顯示檢測到的對象和 FOV 的視覺反饋

### 高級配置

#### PID 控制器調整

微調鼠標移動平滑度：

```
Kp（比例）：控制響應速度（默認：0.26）
Ki（積分）：修正穩態誤差（默認：0.0）
Kd（微分）：減少過衝和振盪（默認：0.0）
```

- **更高的 Kp**：更快的響應，可能導致過衝
- **更高的 Ki**：更好的精度，可能導致不穩定
- **更高的 Kd**：更平滑的移動，可能降低響應速度

#### 性能優化

啟用高性能模式：
- 將**進程優先級**設置為「High」或「Realtime」
- 將**線程優先級**設置為「High」
- 啟用 **CPU 優化**
- 減少**檢測間隔**（最小值：1ms）

#### 鼠標控制方法

- **mouse_event**：標準 Windows API（兼容大多數遊戲）
- **ddxoft**：硬件級鼠標驅動（需要管理員權限）

---

## ⚙️ 配置參考

### 主配置文件：`config.json`

應用程序將所有設置保存到 `src/config.json`。以下是關鍵參數：

```json
{
  "fov_size": 222,                    // 視野大小（像素）
  "min_confidence": 0.11,             // 最小檢測置信度（0.0-1.0）
  "aim_part": "head",                 // 目標部位："head"、"body"、"both"
  "single_target_mode": true,         // 僅跟踪最近的目標
  "keep_detecting": true,             // 始終檢測（即使不瞄準時）
  "fov_follow_mouse": true,           // FOV 跟隨鼠標光標
  
  // PID 控制器（X 軸）
  "pid_kp_x": 0.26,
  "pid_ki_x": 0.0,
  "pid_kd_x": 0.0,
  
  // PID 控制器（Y 軸）
  "pid_kp_y": 0.26,
  "pid_ki_y": 0.0,
  "pid_kd_y": 0.0,
  
  // 熱鍵（虛擬鍵代碼）
  "AimKeys": [1, 6, 2],               // 0x01=左鍵, 0x06=X2, 0x02=右鍵
  "aim_toggle_key": 45,               // Insert 鍵
  "auto_fire_key": 6,                 // X2 按鈕
  "auto_fire_key2": 4,                // 中鍵
  
  // 自動射擊設置
  "auto_fire_delay": 0.0,             // 射擊前延遲（秒）
  "auto_fire_interval": 0.08,         // 射擊間隔（秒）
  "auto_fire_target_part": "both",    // 自動射擊目標偏好
  
  // 性能設置
  "detect_interval": 0.01,            // 檢測循環延遲（秒）
  "cpu_optimization": true,           // 啟用 CPU 優化
  "process_priority": "high",         // "normal"、"high"、"realtime"
  "thread_priority": "high",          // 線程優先級
  
  // 聲音警報
  "enable_sound_alert": false,        // 檢測到目標時啟用蜂鳴聲
  "sound_frequency": 1000,            // 蜂鳴頻率（Hz）
  "sound_duration": 100,              // 蜂鳴持續時間（ms）
  "sound_interval": 200,              // 蜂鳴之間的最小時間（ms）
  
  // 視覺設置
  "show_fov": true,                   // 顯示 FOV 圓圈
  "show_boxes": true,                 // 顯示檢測框
  "show_confidence": true,            // 顯示置信度分數
  "show_status_panel": true,          // 顯示狀態覆蓋層
  
  // 目標區域比例
  "head_width_ratio": 0.38,           // 頭部區域寬度（0.0-1.0）
  "head_height_ratio": 0.26,          // 頭部區域高度（0.0-1.0）
  "body_width_ratio": 0.87,           // 身體區域寬度（0.0-1.0）
  
  // 鼠標控制
  "mouse_move_method": "mouse_event", // "mouse_event" 或 "ddxoft"
  "mouse_click_method": "ddxoft"      // 鼠標點擊方法
}
```

### 環境變量

不需要環境變量。所有配置都通過 `config.json` 和設置 GUI 完成。

---

## 📁 項目結構

```
Axiom-AI_Aimbot/
├── src/                          # 源代碼目錄
│   ├── main.py                   # 主應用程序入口
│   ├── config.py                 # 配置類和管理
│   ├── config.json               # 用戶設置文件
│   ├── inference.py              # AI 推理和預處理
│   ├── win_utils.py              # Windows API 工具
│   ├── overlay.py                # PyQt6 視覺反饋覆蓋層
│   ├── settings_gui.py           # 設置 GUI 界面
│   ├── status_panel.py           # 狀態面板覆蓋層
│   ├── about.py                  # 關於對話框
│   ├── preset_manager.py         # 配置預設管理器
│   ├── config_manager.py         # 高級配置管理
│   ├── language_manager.py       # 多語言支持
│   ├── language_data.py          # 語言字符串數據庫
│   ├── scaling_warning_dialog.py # Windows 縮放檢測
│   ├── ddxoft.dll                # 硬件鼠標驅動庫
│   ├── logo.ico                  # 應用程序圖標
│   └── 模型/                     # AI 模型目錄
│       └── *.onnx, *.pt          # YOLO 模型
├── requirements.txt              # Python 依賴項
├── LICENSE                       # PolyForm 非商業許可證
├── README.md                     # 本文件
├── 啟動Launcher.bat              # Windows 啟動腳本
├── 常見問題FAQ.txt               # 常見問題解答
├── 面板.png                      # 文檔截圖
├── python-3.11.0-amd64.exe       # Python 安裝程序（捆綁）
└── index.html                    # Web 界面（可選）
```

---

## 🛠️ 故障排除

### 常見問題和解決方案

#### ❌ 應用程序無法啟動

**問題**：雙擊啟動器沒有反應或顯示錯誤。

**解決方案**：
1. 確保已安裝 Python 3.11+
2. 驗證安裝期間勾選了「Add python.exe to PATH」
3. 使用正確選項重新安裝 Python
4. 嘗試從命令行運行：`cd src && python main.py`

#### ❌ ModuleNotFoundError

**問題**：缺少 Python 包錯誤。

**解決方案**：
```bash
# 重新安裝所有依賴項
pip install -r requirements.txt --upgrade
```

#### ❌ 無檢測 / 低 FPS

**問題**：AI 檢測不工作或非常慢。

**解決方案**：
1. 檢查模型文件是否存在於 `src/模型/` 目錄中
2. 降低 FOV 大小以獲得更好的性能
3. 增加 `detect_interval`（例如 0.02 或 0.03）
4. 關閉其他資源密集型應用程序
5. 確保 GPU 驅動程序是最新的
6. 嘗試切換到更小的模型文件

#### ❌ 鼠標不移動

**問題**：檢測有效但鼠標不移動。

**解決方案**：
1. 檢查瞄準鍵是否正確配置
2. 驗證反作弊軟件是否阻止輸入
3. 嘗試將 `mouse_move_method` 切換為「ddxoft」
4. 以管理員身份運行應用程序（某些遊戲需要）
5. 增加 PID Kp 值以實現更激進的移動

#### ❌ 訪問被拒絕 / 權限錯誤

**問題**：應用程序需要管理員權限。

**解決方案**：
- 右鍵單擊啟動器或 `main.py` 並選擇「以管理員身份運行」
- 某些鼠標控制方法需要提升的權限

#### ❌ 覆蓋層不可見

**問題**：FOV 和框不顯示。

**解決方案**：
1. 檢查 `show_fov` 和 `show_boxes` 設置
2. 確保遊戲處於窗口或無邊框模式（不是全屏）
3. 嘗試 Alt+Tab 刷新覆蓋層
4. 禁用 Windows Game Bar 和覆蓋層

#### ❌ CPU 使用率高

**問題**：應用程序使用過多 CPU。

**解決方案**：
1. 增加 `detect_interval`（默認：0.01 → 0.03）
2. 減小 FOV 大小
3. 禁用 `keep_detecting` 模式
4. 關閉狀態面板（設置 `show_status_panel: false`）

---

## 🤝 貢獻

我們歡迎貢獻以改進 Axiom AI！以下是您可以幫助的方式：

### 開發設置

```bash
# Fork 並克隆存儲庫
git clone https://github.com/YOUR_USERNAME/Axiom-AI.git
cd Axiom-AI

# 為您的功能創建分支
git checkout -b feature/your-feature-name

# 安裝開發依賴項
pip install -r requirements.txt

# 進行更改並徹底測試

# 提交並推送
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### 貢獻指南

- **代碼風格**：遵循現有的 Python 約定（PEP 8）
- **文檔**：添加新功能時更新 README
- **測試**：在多個 Windows 版本和硬件上測試
- **語言**：在 UI 元素中支持英語和中文
- **性能**：確保更改不會對 FPS 產生負面影響
- **許可證**：所有貢獻必須符合 PolyForm 非商業許可證

### 貢獻領域

- 🐛 錯誤修復和穩定性改進
- ⚡ 性能優化
- 🎨 UI/UX 增強
- 📚 文檔和教程
- 🌐 翻譯成其他語言
- 🤖 新的 AI 模型和訓練數據
- 🎮 遊戲特定配置文件和預設

---

## 📄 許可證

本項目採用 **PolyForm 非商業許可證 1.0.0**。

### 主要限制：

- ❌ **禁止商業使用**：本軟件不能用於任何商業目的
- ❌ **禁止銷售**：不能銷售或對使用它的軟件或服務收費
- ❌ **禁止商業活動**：不能用於與任何商業活動相關的用途
- ✅ **個人使用**：免費用於個人、教育和研究目的
- ✅ **修改**：您可以修改和分發軟件
- ✅ **署名**：必須包含原始許可證和版權聲明

### 什麼算作商業使用？

- 使用軟件提供付費服務
- 將軟件作為商業產品的一部分使用
- 使用軟件產生收入（直接或間接）
- 在任何業務中使用軟件，即使您不收費

### 允許什麼？

- 個人遊戲和娛樂
- 教育目的和學習
- 研究和開發
- 與朋友分享（非商業）

有關完整的許可證詳細信息，請參閱 [LICENSE](LICENSE) 或訪問 [PolyForm 非商業許可證](https://polyformproject.org/licenses/noncommercial/1.0.0/)。

---

## 📞 聯繫與支持

### 支持渠道

- **Discord 服務器**：[加入我們的社區](https://discord.gg/h4dEh3b8Bt) - 用於一般支持、討論和社區幫助
- **GitHub Issues**：[報告錯誤](https://github.com/iishong0w0/Axiom-AI/issues) - 用於錯誤報告和功能請求
- **電子郵件**：[iis20160512@gmail.com](mailto:iis20160512@gmail.com) - 用於與開發者直接溝通

### 鏈接

- **GitHub**：[@iishong0w0](https://github.com/iishong0w0)
- **存儲庫**：[Axiom-AI](https://github.com/iishong0w0/Axiom-AI)
- **發布**：[最新版本](https://github.com/iishong0w0/Axiom-AI/releases/latest)

---

## 📝 常見問題解答（FAQ）

**問：這是作弊/外掛嗎？**  
答：Axiom AI 是一款旨在幫助殘疾玩家的輔助工具。請負責任地使用並遵守遊戲服務條款。

**問：使用這個會被封號嗎？**  
答：我們無法保證在任何在線遊戲中的安全性。使用風險自負並遵守遊戲規則。

**問：我可以在競技比賽中使用嗎？**  
答：此工具旨在用於休閒遊戲和輔助功能。競技使用可能違反錦標賽規則。

**問：支持哪些遊戲？**  
答：Axiom AI 與模型無關，如果您有訓練好的 YOLO 模型，可以與任何遊戲配合使用。默認模型適用於 Roblox。

**問：如何訓練自己的模型？**  
答：您需要創建數據集並訓練 YOLOv8 模型。詳情請參閱 [Ultralytics 文檔](https://docs.ultralytics.com)。

**問：為什麼我的系統檢測速度慢？**  
答：嘗試減小 FOV 大小、增加檢測間隔或關閉後台應用程序。確保您滿足最低系統要求。

**問：可以在 Linux/Mac 上運行嗎？**  
答：目前，Axiom AI 僅支持 Windows，因為使用了 Windows 特定的 API。未來可能會支持 Linux/Mac。

**問：如何提高準確度？**  
答：調整置信度閾值、調整 PID 參數、使用更好訓練的模型或增加 FOV 大小。

---

## ⚠️ 免責聲明

**本軟件按「原樣」提供，不提供任何形式的保證。** 使用風險自負。開發者不對以下內容負責：
- 使用本軟件的任何後果
- 在線遊戲中的封號或處罰
- 硬件或軟件損壞
- 違反服務條款

**用戶有全部責任確保其使用符合適用法律和遊戲服務條款。**

---

## 🙏 致謝

- **Ultralytics YOLOv8**：提供出色的對象檢測框架
- **ONNX Runtime**：提供優化的模型推理
- **PyQt6**：提供覆蓋層系統
- **社區貢獻者**：提供錯誤報告、建議和支持

---

**版權所有 © 2025 iisHong0w0。保留所有權利。**
