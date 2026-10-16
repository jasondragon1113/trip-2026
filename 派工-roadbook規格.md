# Roadbook 研究派工共用規格（每個目的地一個 agent，必讀）

## 旅客與條件
- 2 位成人（情侶），台灣出發；今天 2026-10-16。日期在 **2026/12/27–2027/1/5 之間選 4–5 天（3–4 晚）**，你要挑出最好的去回日（機票便宜、活動對得上）。
- 機場：台中 RMQ 優先，沒有就桃園 TPE；兩邊都有就都列。機票每人來回目標 ≤ NT$13,000（超過也列，標 `within_budget:false`）。偏好去程早班、回程下午或晚班。
- 兩人全包預算 NT$60,000–100,000。
- 兩人喜歡：**在地美食**（市場、小店、當地人吃的）、**挑戰型活動**（登山、溪降、潛水、鯨鯊、滑雪課、料理課…）、**自駕**（只在不下雪的地方；日本要駕照日文譯本、韓泰菲馬要國際駕照，查該地的規定與租車行情）、**特別體驗**（當地節慶、跨年、日出、夜市、溫泉）。
- 步調：chill，每天 3–5 個點，不要塞滿。

## 查法
- 主要用 WebSearch / WebFetch。找 **YouTube 影片**（你看不了影片，但能查標題、說明、留言摘要與整理文）、台灣／日本／韓國旅遊部落格、Tabelog／Naver／Google 評價、官方網站。每個推薦點要能說出「為什麼」（例如：某頻道的路線、評價分數、當地人推薦）。
- 餐廳與活動價格寫**兩人**新台幣，附來源連結與查詢日；查不到寫 null 並在 `note` 標「待確認」。
- Google Maps 連結用這個格式自己組：`https://www.google.com/maps/search/?api=1&query=` ＋ URL 編碼後的「店名 地址」（日文／韓文原名最準）。
- 機票與住宿：先讀本資料夾既有報告（研究-A～F），能沿用就沿用並註明「沿用研究-X」；只有你負責的目的地沒查過，才自己查。
- **不要登入、不要下單、不要填個資或付款資訊。** 內建瀏覽器只有派工單說「可用瀏覽器」的 agent 才能用，而且要先 tabs_create 開自己的分頁、每個動作帶 tabId。

## 產出：直接寫 JSON 檔 `data/<id>.json`（UTF-8，不要 BOM），結構如下，鍵名不能改
```json
{
  "id": "busan",
  "name": "釜山",
  "subtitle": "海邊跨年小旅行",
  "country": "韓國",
  "flag": "KR",
  "motif": "wave",
  "palette": {"primary": "#2B7FD1", "secondary": "#F6B73C", "soft": "#EAF4FF"},
  "tagline": "一句話（≤20 字）",
  "summary": "2–3 句白話，講這趟怎麼玩、為什麼適合他們",
  "dates": {"out": "12/28", "back": "1/1", "nights": 4, "why": "為什麼選這幾天"},
  "flights": [{"from": "RMQ", "to": "PUS", "airline": "", "out": "12/28 16:15→19:35", "back": "1/1 14:00→15:15", "price_pp_twd": 8668, "baggage": "不含托運，加購約 NT$…", "fits_time_pref": false, "within_budget": true, "verified": true, "source": "URL", "checked": "2026-10-16"}],
  "getting_around": {
    "mode": "自駕|大眾運輸|混合",
    "license": "需要什麼證件、哪裡辦、多少錢、幾天",
    "rental": {"company": "", "car": "", "days": 4, "price_total_twd": 0, "insurance": "", "pickup": "機場/市區", "source": "URL", "note": ""},
    "road_notes": ["12 月底路況、靠左靠右、停車、過路費、ETC…"],
    "public": ["不自駕時的交通卡、票券、價格"]
  },
  "stays": [{"name": "", "area": "", "nights": 4, "price_night_for2_twd": 0, "availability": "有空房|滿房|未知", "url": "", "map_url": "", "why": ""}],
  "days": [
    {"day": 1, "date": "12/28", "weekday": "一", "title": "4–8 字的一天標題", "area": "", "drive_km": null, "drive_time": null, "summary": "一句",
     "stops": [
       {"time": "09:00", "name": "", "kind": "sight|food|activity|challenge|stay|transport|shop|night", "stay_min": 90, "desc": "1–2 句", "price_for2_twd": 0, "booking": "需預約|建議預約|免預約", "booking_url": "", "map_url": "", "site_url": "", "address": "", "tip": "一句提醒（可空）"}
     ]}
  ],
  "food": [{"name": "", "dish": "", "price_for2_twd": 0, "area": "", "map_url": "", "why": "誰推薦／評價", "source": ""}],
  "challenges": [{"name": "", "what": "", "price_for2_twd": 0, "duration": "", "booking": "", "season_ok": true, "url": "", "map_url": "", "note": ""}],
  "budget": {"flights_for2": 0, "stay_for2": 0, "food_for2": [0, 0], "transport_for2": [0, 0], "activities_for2": [0, 0], "total_for2": [0, 0], "note": "估算依據"},
  "weather": {"high_c": 0, "low_c": 0, "conditions": "", "sunrise": "", "sunset": "", "wear": ""},
  "events": [{"date": "12/31", "name": "", "note": "", "url": ""}],
  "prep": [{"item": "要先辦／先訂的事", "when": "幾月幾號前", "url": ""}],
  "risks": [""],
  "sketch": {"days": [{"title": "第一天：…（≤10 字）", "icons": ["plane", "ramen", "beach"], "caption": "≤12 字"}]},
  "youtube_refs": [{"title": "", "channel": "", "url": "", "takeaway": "從它拿了什麼"}],
  "sources": ["URL"],
  "checked": "2026-10-16"
}
```
- `motif` 從這裡選一個：onsen, snow, tower, wave, leaf, lantern, car, whale, mountain, market, castle, coffee。
- `sketch.days[].icons` 每天 2–4 個，只能用：plane, train, bus, car, ferry, temple, castle, tower, market, ramen, sushi, bbq, seafood, coffee, dessert, beer, onsen, beach, whale, fish, mountain, hike, snow, ski, lantern, fireworks, sunrise, night, shopping, massage, camera, bike, boat, cave, waterfall, elephant, bridge, museum, park, hotel。
- `palette` 選跟當地有關、**明亮可愛**的顏色（例：沖繩＝海藍＋珊瑚橘；清邁＝金黃＋橄欖綠），`soft` 是很淡的底色。
- 每天 stops 3–6 個；至少 1 個 food、整趟至少 2 個 challenge 或 activity。
- 所有 `map_url` 必填；`price_for2_twd` 查不到寫 null。

## 另寫一份短報告 `研究-R-<id>.md`（≤40 行）
一句話結論、推薦日期與理由、機票與住宿怎麼來的、自駕可行性、3 個最值得的體驗、待確認清單、來源。

## 回報給派工者（≤15 行）
- `data/<id>.json` 路徑＋`python3 -c "import json;json.load(open('data/<id>.json'))"` 通過與否
- 推薦日期、兩人總額區間、交通方式、3 個亮點各一行
- 待確認項目
- commit hash：N/A

## 2026-10-16 04:10 追加（使用者新要求，所有目的地都要）
1. **每個 stop、每個 food 都要配一張真實照片** `"photo": {"url": "", "credit": "", "license": ""}`：
   - 只能用 **Wikimedia Commons**（`https://upload.wikimedia.org/wikipedia/commons/...` 直接檔案連結，寬度 ≥ 800px；用 Commons 檔案頁的「原始檔案」連結，或 `Special:FilePath/<檔名>?width=1200`）或官方觀光局明寫可自由使用的圖；寫作者與授權（例 CC BY-SA 4.0 / CC0 / Public domain）。
   - 找法：WebSearch `site:commons.wikimedia.org <地名或料理名>`，或 WebFetch `https://commons.wikimedia.org/w/index.php?search=<關鍵字>&ns6=1`。
   - 找不到就寫 `null`，不要亂貼。
2. **每天最後一個 stop 是酒吧**（`"kind": "bar"`）：店名、類型（精釀／雞尾酒／居酒屋／屋台／酒吧街）、兩人預算、地圖、評價來源。整趟至少 1 間在 YouTube 或部落格被推薦的特色酒吧。
3. **韓國目的地（釜山、首爾、濟州）必排女友的清單**：韓式烤肉、生章魚（산낙지）、生牛肉（육회）、泡菜豆腐鍋、炸醬麵——每樣至少一間店，進 `food` 與 `days.stops`。
4. **每個 stop、每個 food、每個 challenge 加介紹連結** `"links": [{"type": "youtube|ig|blog|official", "title": "", "url": ""}]`，0–3 條：YouTube 影片、Instagram 貼文／帳號、旅遊部落格或旅遊網站（Klook／KKday 活動頁也算 official）。連結要真的存在（WebFetch 或搜尋結果看到的網址），不要猜。
5. **美食的 `links` 以 Instagram 為主**（女友愛看 IG）：每個 food 至少 1 條 `type:"ig"`（店家官方帳號、或美食帳號介紹該店的貼文／Reels），找法：WebSearch `"<店名>" instagram` 或 `site:instagram.com <店名>`。找不到 IG 再用 YouTube／部落格。
6. **搜尋額度**：每個 agent 的 WebSearch 大約只有 200 次，照片與 IG 驗證請直接 WebFetch Commons API（`https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<關鍵字>&srnamespace=6&format=json`）與 `https://www.instagram.com/<帳號>/`，不要用搜尋查照片。機票：Google Flights 動態頁 WebFetch 讀不到——先沿用研究-A～F 的價格；沒有的標 verified:false，之後會有專門的 agent 用瀏覽器核價。
7. **WebSearch 額度是整個 session 共用的 200 次，現在已經用完**（2026-10-16 05:00 起）。改用：①已知網址直接 WebFetch；②需要搜尋時用**內建瀏覽器**：先 `tabs_create` 開自己的分頁，之後每個動作都帶自己的 tabId，用 Google 搜尋、Instagram、Commons；③scratchpad 下的腳本放自己的子目錄 `scratchpad/<id>/`，不要放根目錄（會被別的 agent 覆寫）。

## 2026-10-16 長途版（雪梨、紐約）差異
- 日期：12/28（一）出發 → 1/3（日）回台灣落地前後，約 6 晚；要在當地跨年。可前後挪 1 天找更好的直飛班次（仍在 12/27–1/5）。
- **只算直飛**（使用者指示）：台中 RMQ 有直飛就列，沒有就桃園 TPE。轉機的不列入預算（可以列一筆 kind:"transfer" 當參考）。
- 預算不設上限，照實算兩人全包；`within_budget` 一律依「每人 ≤13,000」照實標（會是 false）。
- 搜尋：WebSearch 已用完。用內建瀏覽器（先 tabs_create 開自己的分頁、每個動作帶 tabId）；分頁不夠時可改用 Chrome 擴充功能，限唯讀：不登入、不填表、不下單，用完關分頁。照片用 Commons API（curl，間隔 2 秒），YouTube 可 curl 搜尋頁抓 ytInitialData。腳本放 `scratchpad/<id>/`。
- 其他（photo、每晚酒吧、links 以 IG 為主、JSON 結構）全部照前面 1–7 點。
