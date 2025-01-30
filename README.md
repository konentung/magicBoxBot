# MagicBoxBot

MagicBoxBot 是一個 LINEBot，旨在為使用者帶來樂趣和實用功能。這個機器人包括各種小遊戲和功能，如 1A2B、猜拳、行事曆紀錄和 AI 問答。不管你是想玩個小遊戲打發時間，還是需要快速的 AI 助手，MagicBoxBot 都能滿足你的需求！

## 功能：
- **1A2B 遊戲**：一個帶有回饋的數字猜測遊戲，適合喜歡邏輯謎題的人。
- **猜拳遊戲**：經典的猜拳遊戲，可以和機器人來一場對決。
- **行事曆紀錄**：使用這個機器人的行事曆功能，輕鬆記錄重要的日期、提醒事項和事件。
- **AI 問答**：向機器人提問任何問題，它會使用內建的 AI 技術提供智慧的回答。

## 使用方法：

### 添加 MagicBoxBot:
你可以透過掃描下面的 QR 碼將 MagicBoxBot 加入你的 LINE 好友列表。一旦添加，你可以直接在聊天中使用所有可用的功能！

![QR Code](https://your-link-to-qr-code.com)  <!-- 請記得將此處的連結替換為實際的 QR 碼連結 -->

### 執行機器人：
MagicBoxBot 由 LINE Messaging API 驅動，並託管於雲端伺服器上。設定步驟如下：

1. 將此儲存庫克隆到你的本地機器或伺服器：
    ```bash
    git clone https://github.com/your-username/MagicBoxBot.git
    cd MagicBoxBot
    ```

2. 安裝所需的依賴項：
    ```bash
    pip install -r requirements.txt
    ```

3. 設定你的 LINE Messaging API 憑證。你需要創建一個 LINE Developers 帳號並獲得你的頻道 API 憑證（頻道密鑰和頻道存取令牌）。

4. 通過在 `.env` 文件中設定憑證的環境變數來配置機器人。

5. 使用以下命令運行機器人：
    ```bash
    python app.py
    ```

## 指令：
- **1A2B 遊戲**：通過向機器人發送 "1A2B" 開始遊戲。機器人會生成一個隨機數字，你需要猜出它。
- **猜拳遊戲**：發送 "rock"、"paper" 或 "scissors" 與機器人進行對戰。
- **行事曆紀錄**：使用 "add event" 指令，並加上事件詳情來保存提醒事項或事件。
- **AI 問答**：只需輸入任何問題，機器人就會給出智慧的回答。

## 安裝：
1. 克隆儲存庫：
    ```bash
    git clone https://github.com/your-username/MagicBoxBot.git
    cd MagicBoxBot
    ```

2. 安裝依賴項：
    ```bash
    pip install -r requirements.txt
    ```

3. 設定環境變數：
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN

4. 運行機器人：
    ```bash
    python app.py
    ```

## 授權：
此專案是開源的，並且以 MIT 授權條款發佈。
