# 連接 R528 MIBOX-X1 開發板（串口與聯網）
\[ [English](../../en/contest_hk_2026/mibox_x1_connect_guide.md) | [简体中文](./mibox_x1_connect_guide.md) | 繁體中文 \]

> 本文介紹燒錄固件之後，怎樣用 Windows 電腦通過串口連上 R528 MIBOX-X1 開發板，確認系統已經啟動，並讓開發板連上 Wi-Fi。串口工具以 MobaXterm 為例。燒錄固件的步驟見[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)第四節。

## 一、準備

### 1、硬件和接線

- 一塊 R528 MIBOX-X1 開發板，已經燒錄好固件。
- 一根 USB Type-A 轉 Type-C 線，一頭接電腦，另一頭接開發板的 **12 號接口（UART0 調試串口）**。12 號口和燒錄用的 11 號口（USB-D）都在板子右上角，12 號在左，11 號在右，不要接反。接口位置見[接口圖](images/mibox_x1_interfaces.png)。
- 把撥碼開關 **DIP4 撥到 ON**。DIP4 在 OFF 時，這組引腳用作 SD 卡，串口裏不會有任何輸出。

### 2、安裝 CH340 驅動

開發板用 CH340 芯片把串口轉成 USB，電腦需要安裝對應的驅動。

1. 解壓工具包裏的 `CH341SER_Windows.zip`。
2. 用管理員權限運行 `SETUP.EXE`，點擊「安裝」。
3. 裝好後，插上串口線，打開「設備管理器」，在「端口（COM 和 LPT）」下應該能看到 `USB-SERIAL CH340 (COMx)`，其中 `COMx` 是端口號（例如 COM6），記下它。

端口號會因電腦和 USB 口不同而變化。看不到這一項，説明驅動沒裝好，或者線沒有接在 12 號口。

## 二、用 MobaXterm 連接串口

1. 先關閉所有可能佔用這個 COM 口的程序（其他串口工具等）。一個 COM 口同一時間只能被一個程序打開。
2. 打開 MobaXterm，點擊左上角的 **Session**，選擇 **Serial**。
3. 按下表設置：

   | 設置項 | 取值 |
   | ------ | ---- |
   | Serial port | 上一步記下的 COM 口，例如 `COM6 (USB-SERIAL CH340 (COM6))` |
   | Speed (bps) | `1500000` |
   | Data bits | 8 |
   | Stop bits | 1 |
   | Parity | None |
   | Flow control | None |

   Speed 下拉列表裏不一定有 1500000，直接在輸入框裏輸入即可。Data bits、Stop bits、Parity 和 Flow control 在 **Advanced Serial settings** 頁籤裏。
4. 點擊 **OK**，會話就打開了。
5. 按開發板上的 RESET 鍵（SW1，接口圖 13 號），窗口裏會滾動出開機日誌。沒有日誌時，先在窗口裏按一下回車。

Flow control 請選 None（不使用流控）。

## 三、確認系統啟動成功

開機日誌裏最後會出現 `Boot nsh ok`，隨後是 NuttShell 的提示符 `nsh>`。下面是一段真實開發板的日誌節選，具體行數、進程號和時間會因固件版本而不同：

```text
Started the NTP daemon as PID=26
lvgldemo &
...
echo "Boot nsh ok"
Boot nsh ok

NuttShell (NSH)
nsh>
```

在這之前的日誌裏還能看到這些信息，可以用來判斷各個部分是否正常：

| 日誌內容 | 説明 |
| -------- | ---- |
| `lv_nuttx_fbdev` 相關行，含 `480 at 130dpi` | 屏幕驅動已啟動，板子的屏幕上應有畫面 |
| `touchscreen /dev/input0 opening success` | 觸摸設備已打開，用手指點屏幕應有反應 |
| `lvgl fb loop start OK`、`lvgl input loop start OK` | LVGL 界面已運行 |
| `bluetoothd` 啟動，`A2DP-Sink`、`GATTC`、`GATTS` 等服務 `register success` | 藍牙協議棧已啟動 |

注意：

- `nsh>` 之後，LVGL 和藍牙的日誌可能還在繼續輸出，把提示符衝到上面去。按一下回車，就會得到一個乾淨的 `nsh>`。
- 沒有聯網時，系統時間顯示為 1970 年（日誌前面的 `70/01/1`），這不是故障。

看到 `nsh>` 之後，可以先輸入下面兩條命令試一試：

```text
nsh> help
nsh> uname -a
```

`help` 列出可用的命令，`uname -a` 顯示內核信息。

## 四、連接 Wi-Fi

開發板的 Wi-Fi 模組是 RTL8733BS，支持 2.4 GHz 和 5 GHz。下面的步驟讓開發板作為客户端（STA）連接路由器或手機熱點。以下命令在 `nsh>` 提示符下執行。

```text
nsh> ifup wlan0
nsh> wapi mode wlan0 2
nsh> wapi psk wlan0 <PSK> 3
nsh> wapi essid wlan0 <SSID> 1
nsh> renew wlan0
```

- `<PSK>` 換成 Wi-Fi 密碼，`<SSID>` 換成 Wi-Fi 名稱。
- `renew wlan0` 執行後會向路由器申請地址。
- 命令請一條一條輸入。一次粘貼多行時，串口偶爾會丟字符。

連接成功後，用 `ping` 檢查網絡，可以 ping 路由器的網關地址，也可以 ping 外網地址：

```text
nsh> ping 8.8.8.8
```

收到回覆就説明聯網成功了。

按上面的命令連接後，重新上電需要把命令再輸入一遍。開機腳本會檢查 `/data/etc/wifi/wapi.conf`，這個文件存在時會自動啟動 Wi-Fi，但怎樣生成這個文件我們還沒有驗證，請先用上面的手動方式。5 GHz 網絡也還沒有在開發板上測試過，請先用 2.4 GHz 的網絡。Wi-Fi 密碼屬於私人信息，在截圖或日誌裏發給別人之前，請先把它遮住。

開發板也可以作為熱點（AP 模式），命令見[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)第五節的 Wi-Fi 部分。

## 五、常見問題

| 現象 | 先檢查 |
| ---- | ------ |
| 設備管理器裏沒有 CH340，MobaXterm 的下拉列表裏也沒有 COM 口 | CH340 驅動是否已安裝；線是否接在 12 號口；換一根線或換一個 USB 口 |
| 提示端口打不開或拒絕訪問 | COM 口被其他程序佔用，先關閉它們 |
| 窗口裏有輸出，但全是亂碼 | Speed 是否是 `1500000`，數據位 8、停止位 1、校驗 None |
| 窗口裏沒有任何輸出 | DIP4 是否在 ON；線是否接在 12 號口；先按一下回車；再按 RESET 鍵 |
| 鍵盤輸入沒有反應，輸出停住不動 | Flow control 是否是 None；按 RESET 鍵重新啟動，再看日誌 |
| 燒錄完成後開發板起不來 | 燒寫線（11 號口）是否已經拔掉，見[開發板使用指南](./mibox_x1_board_guide_zh-hk.md)第四節 |

## 六、使用其他串口工具

串口參數與上面相同（1500000、8 位數據位、無校驗、1 位停止位、無流控），所以 PuTTY、picocom 等工具也可以使用，只需要選對 COM 口或設備名。我們在 Windows 上實際使用並驗證過的是 MobaXterm。
