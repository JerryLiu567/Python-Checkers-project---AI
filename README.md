# ♟️ Python Checkers AI (西洋跳棋 AI)

> 這是我的高二自主學習專案：從零開始打造一個具備人工智慧的西洋跳棋遊戲。
> This is my self-directed learning project: Building a Checkers game with AI from scratch using Python.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Library-Pygame-green?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)

## 📖 專案簡介 (Introduction)

這個專案是利用 Python 的 **Pygame** 模組開發的視窗化西洋跳棋遊戲。除了基本的雙人對戰功能外，最大的特色是實作了基於 **Minimax 演算法** 與 **Alpha-Beta 剪枝** 的 AI 對手，讓玩家可以與電腦進行不同難度的對奕。

透過這個專案，我深入學習了：
- **物件導向程式設計 (OOP)**：管理棋盤 (Board)、棋子 (Piece) 與遊戲流程 (Game)。
- **演算法實作**：理解並撰寫遞迴 (Recursion) 與樹狀搜尋演算法。
- **使用者介面設計**：處理滑鼠事件、音效播放與畫面更新。

## ✨ 功能特色 (Features)

* **多種遊戲模式**：
    * 🆚 **PVP (Player vs Player)**：雙人本機對戰。
    * 🤖 **PVA (Player vs AI)**：與 AI 電腦對戰。
* **智慧型 AI 對手**：
    * 提供三種難度選擇：
        * **Easy**: 搜尋深度 2 層
        * **Medium**: 搜尋深度 4 層
        * **Hard**: 搜尋深度 5 層
    * 採用 **Alpha-Beta Pruning** 優化搜尋效率。
* **完整規則實作**：
    * ✅ **連環跳 (Multi-jump)**：支援連續吃子判定。
    * ✅ **國王升級 (King Promotion)**：到達底線自動升變，可反向移動。
    * ✅ **強迫吃子 (Forced Capture)**：若有吃子機會，系統會提示且必須執行。
* **優化體驗**：
    * 💡 **合法移動路徑提示**：滑鼠點擊棋子時，顯示綠色圓點提示可移動位置。
    * 🔊 **豐富音效**：包含移動、吃子、升變、勝利與和局的音效回饋。
    * 🎨 **精美介面**：包含主選單、難度選擇與遊戲結束畫面。

## 🛠️ 技術架構 (Tech Stack)

* **語言**：Python 3
* **核心函式庫**：`pygame`
* **專案結構**：
    * `main.py`: 程式入口，管理主迴圈 (Main Loop) 與視窗狀態切換。
    * `ui.py`: 負責繪製選單、按鈕、文字資訊與遊戲結束畫面。
    * `checkers/`: 遊戲核心邏輯模組。
        * `game.py`: 遊戲裁判，處理回合控制、勝負判定。
        * `board.py`: 棋盤資料結構，管理棋子位置與移動邏輯。
        * `piece.py`: 棋子物件，負責繪製與屬性管理。
    * `minmax/`: AI 引擎。
        * `algorithm.py`: 實作 Minimax 與 Alpha-Beta 演算法。
        * `evaluation.py`: 盤面評估函式，計算當前局勢分數。
    * `assets/`: 圖片與音效資源。

## 🚀 如何執行 (How to Run)

### 1. 安裝套件
確保你的電腦已安裝 Python，並執行以下指令安裝依賴套件：
```bash
pip install pygame
