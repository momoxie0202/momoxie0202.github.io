#!/usr/bin/env python3
"""產生 SyncMirror 官網各語系靜態頁（/apps/syncmirror/<語系>/index.html）。

每個語言一個網址、HTML 直接寫該語言（Google 不執行 JS 換字也看得到），互相 hreflang，
FAQ 結構化資料與頁面上看得到的問答同一份來源。改文案改這裡，再跑：

    python3 _tools/build_syncmirror.py

底線開頭的資料夾 GitHub Pages（Jekyll）不會發布。
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://momoxie0202.github.io/apps/syncmirror/"
APP_STORE = "https://apps.apple.com/app/apple-store/id6755509268?pt=128309367&amp;ct={ct}&amp;mt=8"
PLAY = ("https://play.google.com/store/apps/details?id=com.syncmirror.syncmirror_plus_android"
        "&amp;referrer=utm_source%3Dsyncmirror.app%26utm_medium%3Dwebsite%26utm_campaign%3D{ct}")

# 頁面事實（改 App 時一起確認）：iOS 15.0 以上；變速 0.25x–2.0x；鏡像、變速、AB 循環免費；
# 錄影比對、合併匯出有每日免費次數（後台可調，頁面不寫數字）；PRO 無限、無浮水印、無廣告。
# 評分：台灣 App Store 4.88（75 則，2026-10-17 iTunes lookup）。評論是台灣真實評論，其他語系標「翻譯」。

LOCALES = [
    # (資料夾, html lang, hreflang, 選單名稱)
    ("", "en", "en", "English"),
    ("zh-tw/", "zh-Hant-TW", "zh-TW", "繁體中文（台灣）"),
    ("zh-hk/", "zh-Hant-HK", "zh-HK", "繁體中文（香港）"),
    ("ko/", "ko", "ko", "한국어"),
    ("ja/", "ja", "ja", "日本語"),
]

# 頁首按鈕用的短名稱：台灣與香港都是繁中，要分得出來
SHORT_NAME = {"": "EN", "zh-tw/": "繁中・台灣", "zh-hk/": "繁中・香港", "ko/": "한국어", "ja/": "日本語"}

FONT_EXTRA = {
    "zh-tw/": "Noto+Sans+TC:wght@400;500;600;700",
    "zh-hk/": "Noto+Sans+HK:wght@400;500;600;700",
    "ko/": "Noto+Sans+KR:wght@400;500;600;700",
    "ja/": "Noto+Sans+JP:wght@400;500;600;700",
}
FONT_FAMILY = {
    "zh-tw/": "'Noto Sans TC'",
    "zh-hk/": "'Noto Sans HK'",
    "ko/": "'Noto Sans KR'",
    "ja/": "'Noto Sans JP'",
}

T = {}

T[""] = dict(
    title="SyncMirror – K-pop Dance Practice App: Mirror, Slow-Mo AB Loop, Record & Compare",
    desc="Practice dance covers on iPhone and Android: mirror the video, slow it down to 0.25x, loop the hard part, then record yourself and compare side by side with the original.",
    keywords="dance practice app, kpop dance practice, dance cover, mirror video, flip video, slow motion dance, AB loop, compare dance video side by side, choreography practice",
    og_title="SyncMirror – Mirror, slow down, loop, record and compare your dance",
    download="Download",
    badge="Rated 4.9 on the App Store in Taiwan",
    h1_html='Learn the choreo.<br><span class="gold">See exactly where you’re off.</span>',
    hero_p="Import any dance video. Mirror it, slow it down, loop the hard eight-count, then record yourself and compare side by side with the original.",
    cta_how="See how it works",
    how_label="How it works",
    how_title="Three steps to a cleaner cover",
    how_desc="No account, no setup. Open the app and start practicing.",
    steps=[
        ("Import a video", "Pick a dance practice video or tutorial from your photo library or Files."),
        ("Mirror, slow down, loop", "Flip it so left is left, drop to 0.25x, and loop just the part you keep missing."),
        ("Record and compare", "Record yourself while the music plays, then watch your take next to the original."),
    ],
    feat_label="Features",
    feat_title="Built for real practice, not just playback",
    feat_desc="Everything you need to go from “almost” to “clean”.",
    features=[
        ("Speed control", "0.25x to 2.0x. Break moves down in slow motion, or speed up to drill stamina."),
        ("AB loop", "Mark a start and end point and repeat that section endlessly — no more dragging the timeline."),
        ("Sync recording", "The reference music plays while you record, so your take is already on beat."),
        ("Side-by-side compare", "Your recording and the original play together. Nudge the offset to line them up frame by frame."),
        ("Mirror mode", "Flip the video horizontally so it matches you, like dancing in front of a studio mirror."),
        ("Picture-in-picture", "Keep the video in a floating window while you check lyrics or other apps."),
    ],
    use_label="Who it’s for",
    use_title="Dance covers and anything you learn by copying",
    use_desc="Built for dancers, used for any skill where you watch and repeat.",
    uses=["K-pop dance covers", "Choreography classes", "Random play dance", "Fitness / workouts", "Yoga / posture", "Martial arts", "Golf swing", "Physical therapy"],
    rev_label="Reviews",
    rev_title="What dancers say on the App Store",
    reviews=[
        ("“The A-B loop is the most important thing for dancers besides slow-down. After downloading this app I deleted all the others.”", "App Store review, Taiwan · Feb 2026 (translated)"),
        ("“It really helped my own practice — especially the record-and-compare feature, it’s amazing.”", "App Store review, Taiwan · Jun 2026 (translated)"),
        ("“I’m new to dance and couldn’t keep up. Mirroring and slowing the video down let me follow along little by little.”", "App Store review, Taiwan · Jan 2026 (translated)"),
    ],
    faq_label="FAQ",
    faq_title="Common questions",
    faqs=[
        ("How do I mirror a dance video on my phone?", "Import the video into SyncMirror and tap the mirror button in the player. The picture flips horizontally, so when the dancer moves to their right you move to your right, like following a studio mirror. Mirroring is free."),
        ("How do I slow down and loop one part of a dance?", "Set the speed anywhere from 0.25x to 2.0x, then use AB loop to mark the start and end of the section. SyncMirror repeats just that part until you stop it. Both are free."),
        ("How can I compare my dance with the original video?", "Tap record: SyncMirror plays the reference music while the camera records you. Afterwards both videos play side by side, you can fine-tune the timing offset, and you can merge them into one side-by-side video to save or share."),
        ("Is SyncMirror free?", "Yes. Importing videos, mirror, speed control and AB loop are free. Recording, comparing and merging include a daily free allowance. PRO removes the daily limits, the watermark and ads."),
        ("Which devices are supported?", "iPhone and iPad with iOS 15.0 or later, and Android phones."),
        ("Is it only for K-pop dance?", "No. Any dance style works, and people also use it for workouts, yoga, martial arts, golf and rehab exercises — anything you learn by watching and copying."),
    ],
    final_title_html='Stop guessing. <span class="gold">Start seeing your progress.</span>',
    final_desc="Free to download. No account needed.",
    privacy="Privacy Policy",
    terms="Terms of Use",
    suggest="This page is available in English",
    lang_label="Language",
    home_label="SyncMirror home",
)

T["zh-tw/"] = dict(
    title="SyncMirror 練舞神器｜韓舞翻跳練習 App：鏡像、慢速、AB 循環、錄影比對",
    desc="手機練舞 App：影片鏡像翻轉、0.25 倍慢速、AB 區間重複練卡住的段落，跟著音樂錄下自己，和原影片並排比對，動作差在哪一眼就知道。",
    keywords="練舞 App, 練舞神器, 韓舞, 翻跳, kpop 練舞, 鏡像 影片, 影片 左右翻轉, 慢速播放, AB 循環, 區間重複, 舞蹈練習, 錄影比對",
    og_title="SyncMirror 練舞神器：鏡像、慢速、循環、錄影比對",
    download="下載",
    badge="台灣 App Store 評分 4.9",
    h1_html='練舞不用再靠感覺。<br><span class="gold">差在哪，一眼看出來。</span>',
    hero_p="匯入任何舞蹈影片：鏡像翻轉、放慢、把卡住的八拍抓出來循環，再跟著音樂錄下自己，和原影片並排比對。",
    cta_how="看看怎麼用",
    how_label="使用方式",
    how_title="三步驟，把翻跳練到乾淨",
    how_desc="不用註冊、不用設定，打開就能練。",
    steps=[
        ("匯入影片", "從相簿或「檔案」選練習室版、教學影片都可以。"),
        ("鏡像＋慢速＋循環", "畫面左右翻轉跟著跳不會反，放慢到 0.25 倍，只循環一直跳錯的那段。"),
        ("錄影＋比對", "跟著音樂錄下自己，錄完直接和原影片並排看。"),
    ],
    feat_label="功能介紹",
    feat_title="為「真的在練」設計，不只是播放器",
    feat_desc="從「差不多」練到「整齊」需要的工具都在這裡。",
    features=[
        ("變速播放", "0.25x～2.0x。細節慢慢拆，熟了再加快練體力。"),
        ("AB 循環", "設好起點和終點，那一段無限重播，不用一直拉時間軸。"),
        ("同步錄影", "錄影時同步播放原曲，錄出來就是對著拍子的。"),
        ("並排比對", "你的錄影和原影片一起播，可以微調時間差，一格一格對齊。"),
        ("鏡像模式", "畫面左右翻轉，像在舞蹈教室對著鏡子跳。"),
        ("子母畫面", "影片縮成小視窗，一邊看歌詞或用其他 App 一邊練。"),
    ],
    use_label="適用對象",
    use_title="翻跳，和所有「看了跟著做」的技能",
    use_desc="為舞者設計，任何需要看示範、反覆模仿的練習都能用。",
    uses=["韓舞翻跳", "舞蹈課複習", "隨機舞蹈", "健身／重訓", "瑜伽／體態", "武術", "高爾夫揮桿", "復健動作"],
    rev_label="用戶評價",
    rev_title="App Store 上的真實評論",
    reviews=[
        ("「尤其是 A B 循環，對練舞的人來說除了慢速之外這點超重要的。自從我下載了這個 App 之後，我把其他的都刪掉了。」", "App Store 評論（台灣）· 2026 年 2 月"),
        ("「真心感謝有這個 app，真的幫助了我自己練習，尤其是錄影比對功能真的神好用。」", "App Store 評論（台灣）· 2026 年 6 月"),
        ("「剛學舞動作都跟不上……這個 App 可以轉鏡面跟調慢，然後就慢慢跟得上了。」", "App Store 評論（台灣）· 2026 年 1 月"),
    ],
    faq_label="常見問題",
    faq_title="常見問題",
    faqs=[
        ("手機要怎麼把舞蹈影片鏡像（左右翻轉）？", "把影片匯入 SyncMirror，在播放器點鏡像按鈕，畫面就會左右翻轉。示範的人往他的右邊，你也往你的右邊，像對著教室的鏡子跳。鏡像免費。"),
        ("怎麼把某一段放慢、重複播放？", "速度可以調到 0.25x～2.0x，再用 AB 循環設好起點和終點，SyncMirror 就只重播那一段，直到你停下來。兩個功能都免費。"),
        ("怎麼把自己跳的和原影片比對？", "按錄影後，SyncMirror 會播放原曲，同時用相機錄下你。錄完兩支影片並排播放，可以微調時間差，也能合併成一支左右並排的影片存起來或分享。"),
        ("SyncMirror 免費嗎？", "免費。匯入影片、鏡像、變速、AB 循環都免費；錄影比對和合併匯出每天有免費次數。升級 PRO 沒有每日上限、沒有浮水印，也沒有廣告。"),
        ("支援哪些裝置？", "iPhone、iPad（iOS 15.0 以上）和 Android 手機。"),
        ("只能練韓舞嗎？", "不是。任何舞風都可以，也有人拿來練健身、瑜伽、武術、高爾夫和復健動作，只要是看示範跟著做的都適用。"),
    ],
    final_title_html='別再靠感覺練了。<span class="gold">讓進步看得見。</span>',
    final_desc="免費下載，不用註冊。",
    privacy="隱私政策",
    terms="使用條款",
    suggest="這個頁面有繁體中文版",
    lang_label="語言",
    home_label="SyncMirror 首頁",
)

# 香港：書面語為主、用香港慣用詞（水印、畫中畫、手機、免費下載），標題帶少量口語
T["zh-hk/"] = dict(
    title="SyncMirror 練舞神器｜Kpop 翻跳練習 App：鏡像、慢速、AB 重播、錄影對比",
    desc="用手機練舞：影片鏡像反轉、0.25 倍慢速、AB 段落重播練熟難位，跟住音樂錄低自己，再同原片左右對比，邊度唔夠準一睇就知。",
    keywords="練舞 App, 練舞神器, Kpop 翻跳, cover dance, 跳舞 App, 鏡像 影片, 影片 左右反轉, 慢速播放, AB 重播, 錄影對比, 舞蹈練習",
    og_title="SyncMirror 練舞神器：鏡像、慢速、重播、錄影對比",
    download="下載",
    badge="台灣 App Store 評分 4.9",
    h1_html='練舞唔使再靠估。<br><span class="gold">邊度唔準，一睇就知。</span>',
    hero_p="匯入任何舞蹈影片：鏡像反轉、放慢、將卡住的八拍抽出來重播，再跟住音樂錄低自己，同原片並排對比。",
    cta_how="睇睇點用",
    how_label="使用方法",
    how_title="三個步驟，將翻跳練到整齊",
    how_desc="毋須登記、毋須設定，打開就可以練。",
    steps=[
        ("匯入影片", "由相簿或「檔案」揀練習室版、教學片都得。"),
        ("鏡像＋慢速＋重播", "畫面左右反轉，跟住跳唔會左右調轉；放慢到 0.25 倍，淨係重播成日跳錯嗰段。"),
        ("錄影＋對比", "跟住音樂錄低自己，錄完即刻同原片並排睇。"),
    ],
    feat_label="功能",
    feat_title="為認真練習而設，唔只係播放器",
    feat_desc="由「差唔多」練到「整齊」需要的工具，全部都有。",
    features=[
        ("變速播放", "0.25x 至 2.0x。慢慢拆細節，熟咗再加快練體力。"),
        ("AB 重播", "設定起點同終點，嗰段無限重播，唔使成日拉時間軸。"),
        ("同步錄影", "錄影時同步播放原曲，錄出來已經對準拍子。"),
        ("並排對比", "你的錄影同原片一齊播，可以微調時間差，逐格對齊。"),
        ("鏡像模式", "畫面左右反轉，好似喺舞室對住鏡跳。"),
        ("畫中畫", "影片縮成小視窗，一邊睇歌詞或用其他 App 一邊練。"),
    ],
    use_label="適合邊個",
    use_title="翻跳，同所有「睇完跟住做」的技能",
    use_desc="為跳舞人而設，任何要睇示範、反覆模仿的練習都用得著。",
    uses=["Kpop 翻跳", "舞蹈班溫習", "Random Play Dance", "健身／重訓", "瑜伽／體態", "武術", "高爾夫揮桿", "物理治療"],
    rev_label="用家評價",
    rev_title="App Store 上的真實評論",
    reviews=[
        ("「尤其是 A B 循環，對練舞的人來說除了慢速之外這點超重要的。自從我下載了這個 App 之後，我把其他的都刪掉了。」", "App Store 評論（台灣）· 2026 年 2 月"),
        ("「真心感謝有這個 app，真的幫助了我自己練習，尤其是錄影比對功能真的神好用。」", "App Store 評論（台灣）· 2026 年 6 月"),
        ("「剛學舞動作都跟不上……這個 App 可以轉鏡面跟調慢，然後就慢慢跟得上了。」", "App Store 評論（台灣）· 2026 年 1 月"),
    ],
    faq_label="常見問題",
    faq_title="常見問題",
    faqs=[
        ("點樣用手機將舞蹈影片鏡像（左右反轉）？", "將影片匯入 SyncMirror，在播放器按鏡像按鈕，畫面就會左右反轉。示範的人向佢右邊，你都向你右邊，好似對住舞室塊鏡跳。鏡像功能免費。"),
        ("點樣將某一段放慢同重複播放？", "速度可以調到 0.25x 至 2.0x，再用 AB 重播設定起點同終點，SyncMirror 就只會重播嗰段，直到你停為止。兩個功能都免費。"),
        ("點樣將自己跳的同原片對比？", "按錄影後，SyncMirror 會播放原曲，同時用鏡頭錄低你。錄完兩段影片並排播放，可以微調時間差，亦可以合併成一段左右並排的影片儲存或分享。"),
        ("SyncMirror 係咪免費？", "係。匯入影片、鏡像、變速、AB 重播全部免費；錄影對比同合併匯出每日有免費次數。升級 PRO 冇每日上限、冇水印，亦冇廣告。"),
        ("支援咩裝置？", "iPhone、iPad（iOS 15.0 或以上）同 Android 手機。"),
        ("係咪只可以練 Kpop？", "唔係。任何舞種都得，亦有人用嚟練健身、瑜伽、武術、高爾夫同物理治療動作，只要係睇示範跟住做都適用。"),
    ],
    final_title_html='唔好再靠估。<span class="gold">進步，睇得到。</span>',
    final_desc="免費下載，毋須登記。",
    privacy="私隱政策",
    terms="使用條款",
    suggest="此頁面有香港繁體中文版",
    lang_label="語言",
    home_label="SyncMirror 主頁",
)

# 韓國：해요체、커뮤니티 용어（안무, 커버댄스, 거울 모드, 구간 반복, 배속, 랜플）
T["ko/"] = dict(
    title="SyncMirror – 안무 연습 앱 | 거울 모드·배속·구간 반복·녹화 비교",
    desc="커버댄스 안무 연습 필수 앱. 영상 좌우반전(거울 모드), 0.25배속 느리게, 어려운 구간만 반복하고, 노래에 맞춰 내 춤을 찍어 원본 영상과 나란히 비교해요.",
    keywords="안무 연습 앱, 커버댄스, 케이팝 안무, 거울 모드, 영상 좌우반전, 배속 조절, 구간 반복, 춤 연습, 댄스 연습, 안무 비교, 랜덤플레이댄스",
    og_title="SyncMirror – 거울 모드·배속·구간 반복·녹화 비교",
    download="다운로드",
    badge="대만 App Store 평점 4.9",
    h1_html='안무, 감으로 따지 마세요.<br><span class="gold">어디가 다른지 바로 보여요.</span>',
    hero_p="안무 영상을 불러와 거울 모드로 뒤집고, 느리게 돌리고, 막히는 에잇카운트만 반복하세요. 노래에 맞춰 내 춤을 찍어 원본과 나란히 비교할 수 있어요.",
    cta_how="사용법 보기",
    how_label="사용법",
    how_title="세 단계로 깔끔한 커버 완성",
    how_desc="회원가입도, 설정도 필요 없어요. 열면 바로 연습 시작.",
    steps=[
        ("영상 불러오기", "사진 앨범이나 ‘파일’에서 안무 연습 영상이나 튜토리얼을 골라요."),
        ("거울 모드·배속·구간 반복", "좌우를 뒤집어 방향 헷갈림 없이, 0.25배속으로 느리게, 자꾸 틀리는 구간만 반복해요."),
        ("녹화하고 비교", "노래가 나오는 동안 내 춤을 찍고, 바로 원본과 나란히 봐요."),
    ],
    feat_label="기능",
    feat_title="그냥 플레이어가 아닌, 연습을 위한 앱",
    feat_desc="‘거의 다 됐다’에서 ‘칼군무’까지 필요한 기능을 모두 담았어요.",
    features=[
        ("배속 조절", "0.25배속부터 2배속까지. 느리게 쪼개 보고, 익숙해지면 빠르게 체력 연습."),
        ("구간 반복", "시작점과 끝점을 찍으면 그 구간만 계속 반복돼요. 타임라인을 계속 끌 필요 없어요."),
        ("싱크 녹화", "녹화하는 동안 원곡이 함께 재생돼서 박자에 맞춰 찍을 수 있어요."),
        ("나란히 비교", "내 녹화본과 원본이 동시에 재생돼요. 싱크를 미세 조정해 프레임 단위로 맞춰 봐요."),
        ("거울 모드", "영상을 좌우반전해서 연습실 거울 앞에서 추는 것처럼 따라 할 수 있어요."),
        ("PIP 모드", "영상을 작은 창으로 띄워 두고 가사나 다른 앱을 보면서 연습해요."),
    ],
    use_label="이런 분께",
    use_title="커버댄스, 그리고 보고 따라 하는 모든 연습",
    use_desc="댄서를 위해 만들었지만, 보고 따라 하는 연습이라면 무엇이든 OK.",
    uses=["케이팝 커버댄스", "댄스 학원 복습", "랜덤플레이댄스", "홈트·헬스", "요가·자세 교정", "태권도·무술", "골프 스윙", "재활 운동"],
    rev_label="리뷰",
    rev_title="App Store 실제 리뷰",
    reviews=[
        ("“댄서에게는 느리게 재생 다음으로 A-B 반복이 제일 중요해요. 이 앱을 받고 나서 다른 앱은 다 지웠어요.”", "App Store 리뷰(대만) · 2026년 2월 · 번역"),
        ("“혼자 연습할 때 정말 큰 도움이 됐어요. 특히 녹화 비교 기능이 최고예요.”", "App Store 리뷰(대만) · 2026년 6월 · 번역"),
        ("“춤을 막 배우기 시작해서 동작을 못 따라갔는데, 거울 모드랑 느리게 재생으로 조금씩 따라갈 수 있게 됐어요.”", "App Store 리뷰(대만) · 2026년 1월 · 번역"),
    ],
    faq_label="자주 묻는 질문",
    faq_title="자주 묻는 질문",
    faqs=[
        ("휴대폰에서 안무 영상을 거울 모드(좌우반전)로 보려면?", "영상을 SyncMirror로 불러온 뒤 플레이어에서 거울 버튼을 누르면 화면이 좌우로 뒤집혀요. 영상 속 댄서가 오른쪽으로 가면 나도 내 오른쪽으로 가면 돼서, 연습실 거울을 보는 것처럼 따라 할 수 있어요. 거울 모드는 무료예요."),
        ("특정 구간만 느리게 반복하려면?", "속도를 0.25배속부터 2배속까지 바꾸고, 구간 반복으로 시작점과 끝점을 정하면 그 부분만 계속 반복돼요. 두 기능 모두 무료예요."),
        ("내 춤과 원본 영상을 비교하려면?", "녹화를 누르면 원곡이 재생되면서 카메라로 내 모습을 찍어요. 녹화가 끝나면 두 영상이 나란히 재생되고, 싱크를 미세 조정하거나 한 영상으로 합쳐 저장·공유할 수 있어요."),
        ("SyncMirror는 무료인가요?", "네. 영상 불러오기, 거울 모드, 배속, 구간 반복은 무료예요. 녹화 비교와 합치기는 매일 무료 횟수가 있고, PRO로 업그레이드하면 일일 제한·워터마크·광고가 없어져요."),
        ("어떤 기기에서 쓸 수 있나요?", "iOS 15.0 이상의 iPhone·iPad와 Android 폰에서 쓸 수 있어요."),
        ("케이팝 안무 연습에만 쓸 수 있나요?", "아니요. 어떤 장르의 춤이든 되고, 홈트, 요가, 무술, 골프, 재활 운동처럼 보고 따라 하는 연습이라면 모두 쓸 수 있어요."),
    ],
    final_title_html='감으로 연습하지 마세요. <span class="gold">실력이 느는 게 보여요.</span>',
    final_desc="무료 다운로드, 회원가입 필요 없어요.",
    privacy="개인정보 처리방침",
    terms="이용약관",
    suggest="이 페이지는 한국어로도 볼 수 있어요",
    lang_label="언어",
    home_label="SyncMirror 홈",
)

# 日本：です・ます調、コミュニティ用語（振り入れ、踊ってみた、左右反転、区間リピート、スロー再生）
T["ja/"] = dict(
    title="SyncMirror – ダンス練習アプリ｜左右反転・スロー再生・区間リピート・撮って比較",
    desc="踊ってみた・K-POPカバーの振り入れに。動画を左右反転（ミラー）、0.25倍スロー再生、苦手なパートだけ区間リピート。曲に合わせて自分を撮影し、お手本と並べて比較できます。",
    keywords="ダンス練習 アプリ, 振り入れ, 踊ってみた, K-POP ダンス, カバーダンス, 左右反転, ミラー 動画, スロー再生, 区間リピート, ABリピート, 撮って比較",
    og_title="SyncMirror – 左右反転・スロー・区間リピート・撮って比較",
    download="ダウンロード",
    badge="台湾 App Store 評価 4.9",
    h1_html='振り入れを、感覚だけにしない。<br><span class="gold">ズレがひと目でわかる。</span>',
    hero_p="ダンス動画を読み込んで、左右反転・スロー再生・つまずく8カウントだけリピート。曲に合わせて自分を撮影し、お手本と並べて比較できます。",
    cta_how="使い方を見る",
    how_label="使い方",
    how_title="3ステップで、きれいに踊れる",
    how_desc="アカウント登録も設定も不要。開いてすぐ練習できます。",
    steps=[
        ("動画を読み込む", "写真ライブラリや「ファイル」から、練習用動画やレッスン動画を選びます。"),
        ("反転・スロー・リピート", "左右反転で向きを合わせ、0.25倍まで落として、間違えるパートだけ繰り返します。"),
        ("撮って比較", "曲を流しながら自分を撮影し、そのままお手本と並べて見られます。"),
    ],
    feat_label="機能",
    feat_title="ただのプレーヤーではなく、練習のためのアプリ",
    feat_desc="「なんとなく踊れる」から「揃って踊れる」まで、必要な機能がそろっています。",
    features=[
        ("再生速度の変更", "0.25倍〜2.0倍。スローで細かく確認し、慣れたら速めて体力づくり。"),
        ("区間リピート（ABリピート）", "始点と終点を決めると、その区間だけをくり返し再生。シークバーを何度も動かす必要はありません。"),
        ("同時録画", "撮影中はお手本の曲が流れるので、最初からリズムに合った動画が撮れます。"),
        ("並べて比較", "自分の動画とお手本を同時に再生。タイミングを微調整して、コマ単位で合わせられます。"),
        ("左右反転（ミラー）", "動画を左右反転して、スタジオの鏡の前で踊るように練習できます。"),
        ("ピクチャ・イン・ピクチャ", "動画を小窓にして、歌詞やほかのアプリを見ながら練習できます。"),
    ],
    use_label="こんな方に",
    use_title="踊ってみた、そして「見てまねる」すべての練習に",
    use_desc="ダンサーのために作りましたが、見てまねて覚える練習なら何にでも使えます。",
    uses=["K-POPカバーダンス", "踊ってみた", "ダンス教室の復習", "ランダムプレイダンス", "筋トレ・フィットネス", "ヨガ・姿勢", "ゴルフスイング", "リハビリ"],
    rev_label="レビュー",
    rev_title="App Store に届いた実際のレビュー",
    reviews=[
        ("「ダンスをする人にとって、スロー再生の次に大事なのが A-B リピート。このアプリを入れてから、ほかのアプリは全部消しました。」", "App Store レビュー（台湾）· 2026年2月 · 翻訳"),
        ("「自主練に本当に役立っています。特に撮って比較する機能が最高です。」", "App Store レビュー（台湾）· 2026年6月 · 翻訳"),
        ("「ダンスを始めたばかりで振りについていけなかったけど、反転とスロー再生で少しずつ追いつけるようになりました。」", "App Store レビュー（台湾）· 2026年1月 · 翻訳"),
    ],
    faq_label="よくある質問",
    faq_title="よくある質問",
    faqs=[
        ("スマホでダンス動画を左右反転（ミラー）するには？", "動画を SyncMirror に読み込み、プレーヤーの反転ボタンをタップすると左右が反転します。お手本が右に動いたら自分も右に動けばよいので、スタジオの鏡を見ているように振り入れできます。左右反転は無料です。"),
        ("一部分だけをスローでくり返し再生するには？", "再生速度を 0.25倍〜2.0倍で変え、区間リピートで始点と終点を決めると、その部分だけがくり返し再生されます。どちらも無料です。"),
        ("自分のダンスとお手本動画を比較するには？", "録画をタップすると、お手本の曲を流しながらカメラで自分を撮影します。撮影後は 2 本の動画が並んで再生され、タイミングの微調整や、横並びの 1 本の動画への書き出し・シェアもできます。"),
        ("SyncMirror は無料ですか？", "はい。動画の読み込み、左右反転、速度変更、区間リピートは無料です。撮って比較と動画の書き出しは毎日の無料回数があり、PRO にアップグレードすると回数制限・透かし・広告がなくなります。"),
        ("対応端末は？", "iOS 15.0 以降の iPhone・iPad と、Android スマートフォンに対応しています。"),
        ("K-POP ダンス専用ですか？", "いいえ。どんなジャンルのダンスでも使え、筋トレ、ヨガ、武道、ゴルフ、リハビリなど、見てまねて覚える練習にも使われています。"),
    ],
    final_title_html='感覚だけの練習は、もう終わり。<span class="gold">上達が目に見える。</span>',
    final_desc="無料ダウンロード。アカウント登録は不要です。",
    privacy="プライバシーポリシー",
    terms="利用規約",
    suggest="このページは日本語でもご覧いただけます",
    lang_label="言語",
    home_label="SyncMirror ホーム",
)

APPLE_SVG = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>'
PLAY_SVG = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.61 1.814L13.793 12 3.61 22.186a.996.996 0 0 1-.61-.92V2.734a1 1 0 0 1 .61-.92zm1.377-.47L15.98 7.076l-2.87 2.87L5.418 2.253l-.431-.909zm0 21.312l-.43-.909 7.69-7.693 2.87 2.87L4.988 22.656zM21.434 10.88l-3.678 2.074-3.192-3.192 3.192-3.192 3.678 2.074a1.235 1.235 0 0 1 0 2.236z"/></svg>'

STEP_ICONS = [
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFD117" stroke-width="2" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    '<img src="/abloop.png" alt="" width="22" height="22">',
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="7" stroke="#FFD117" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="#FF3B30"/></svg>',
]
FEATURE_ICONS = [
    '<img src="/play.png" alt="" width="22" height="22">',
    '<img src="/abloop.png" alt="" width="22" height="22">',
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFD117" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/><circle cx="17" cy="5" r="3" fill="#FF3B30" stroke="none"/></svg>',
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFD117" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="9" height="18" rx="1"/><rect x="14" y="3" width="9" height="18" rx="1"/></svg>',
    '<img src="/mirror.png" alt="" width="22" height="22">',
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFD117" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="22" height="18" rx="2"/><rect x="12" y="11" width="10" height="9" rx="1" fill="var(--gold-dim)"/></svg>',
]


def e(s):
    return html.escape(s, quote=True)


def campaign(slug, place):
    """App Store ct／Play utm_campaign：英文頁沿用舊值，其他語系加語系後綴，GA／ASC 可分語系看。"""
    return f"website_{place}" if not slug else f"website_{place}_{slug.strip('/').replace('-', '')}"


def store_buttons(slug, place, cls, size, t):
    return (
        f'<a href="{APP_STORE.format(ct=campaign(slug, place))}" class="{cls}">{APPLE_SVG.format(s=size)}<span>App Store</span></a>\n'
        f'          <a href="{PLAY.format(ct=campaign(slug, place))}" class="{cls}">{PLAY_SVG.format(s=size)}<span>Google Play</span></a>'
    )


def build(slug, lang, hreflang, menu_name):
    t = T[slug]
    url = BASE + slug
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{h}" href="{BASE + s}">' for s, _, h, _ in LOCALES
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{BASE}">'
    og_locales = {"": "en_US", "zh-tw/": "zh_TW", "zh-hk/": "zh_HK", "ko/": "ko_KR", "ja/": "ja_JP"}
    og_alt = "\n".join(
        f'  <meta property="og:locale:alternate" content="{og_locales[s]}">' for s, *_ in LOCALES if s != slug
    )
    fonts = "family=Inter:wght@400;500;600;700"
    if slug in FONT_EXTRA:
        fonts += "&family=" + FONT_EXTRA[slug]
    font_style = ""
    if slug in FONT_FAMILY:
        font_style = f"\n  <style>body {{ font-family: 'Inter', {FONT_FAMILY[slug]}, -apple-system, BlinkMacSystemFont, sans-serif; }}"
        # 日文沒有空格，預設會在詞中間斷行；auto-phrase 讓標題依詞組換行（不支援的瀏覽器照舊）
        if slug == "ja/":
            font_style += " h1, h2, h3 { word-break: auto-phrase; }"
        font_style += "</style>"

    app_ld = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "SyncMirror",
        "description": t["desc"],
        "url": url,
        "inLanguage": hreflang,
        "applicationCategory": "MultimediaApplication",
        "operatingSystem": "iOS 15.0+, Android",
        "downloadUrl": [
            "https://apps.apple.com/app/id6755509268",
            "https://play.google.com/store/apps/details?id=com.syncmirror.syncmirror_plus_android",
        ],
        "featureList": [f[0] for f in t["features"]],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": hreflang,
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t["faqs"]
        ],
    }
    ld = lambda o: json.dumps(o, ensure_ascii=False, indent=2).replace("</", "<\\/")

    menu = "\n".join(
        f'            <li><a href="{BASE + s}" hreflang="{h}" lang="{h}"'
        + (' aria-current="page"' if s == slug else "")
        + f">{e(n)}</a></li>"
        for s, _, h, n in LOCALES
    )
    steps = "\n".join(
        f'''          <article class="step">
            <div class="step-icon">{STEP_ICONS[i]}</div>
            <h3>{e(a)}</h3>
            <p>{e(b)}</p>
          </article>''' for i, (a, b) in enumerate(t["steps"])
    )
    features = "\n".join(
        f'''          <article class="feature-card">
            <div class="feature-icon">{FEATURE_ICONS[i]}</div>
            <h3>{e(a)}</h3>
            <p>{e(b)}</p>
          </article>''' for i, (a, b) in enumerate(t["features"])
    )
    uses = "\n".join(f'          <span class="use-case-tag">{e(u)}</span>' for u in t["uses"])
    reviews = "\n".join(
        f'''          <article class="testimonial">
            <div class="testimonial-stars" aria-label="5/5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <blockquote>{e(q)}</blockquote>
            <cite>{e(c)}</cite>
          </article>''' for q, c in t["reviews"]
    )
    faqs = "\n".join(
        f'''          <details class="faq-item">
            <summary>{e(q)}</summary>
            <div class="faq-answer">{e(a)}</div>
          </details>''' for q, a in t["faqs"]
    )
    # 依瀏覽器語言提示另一個語系頁（不自動轉址：Google 不建議依語言自動轉址，爬蟲會只看到一種語言）
    suggest_map = {h: {"url": BASE + s, "text": T[s]["suggest"], "name": n} for s, _, h, n in LOCALES}
    suggest_js = json.dumps(suggest_map, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(t["title"])}</title>
  <meta name="description" content="{e(t["desc"])}">
  <meta name="keywords" content="{e(t["keywords"])}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">
{alternates}

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="SyncMirror">
  <meta property="og:locale" content="{og_locales[slug]}">
{og_alt}
  <meta property="og:title" content="{e(t["og_title"])}">
  <meta property="og:description" content="{e(t["desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}og-image.png">
  <meta property="og:image:width" content="1024">
  <meta property="og:image:height" content="500">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(t["og_title"])}">
  <meta name="twitter:description" content="{e(t["desc"])}">
  <meta name="twitter:image" content="{BASE}og-image.png">

  <meta name="apple-itunes-app" content="app-id=6755509268">
  <link rel="apple-touch-icon" href="/icon.png">
  <link rel="icon" type="image/png" href="/icon.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
  <link rel="stylesheet" href="/apps/syncmirror/style.css">{font_style}

  <script type="application/ld+json">
{ld(app_ld)}
  </script>
  <script type="application/ld+json">
{ld(faq_ld)}
  </script>
</head>
<body>

  <header>
    <div class="container header-inner">
      <a href="{url}" class="logo" aria-label="{e(t["home_label"])}">
        <img src="/icon.png" alt="SyncMirror" class="logo-icon" width="34" height="34">
        <span class="logo-text">SyncMirror</span>
      </a>
      <div class="header-right">
        <details class="lang-menu">
          <summary aria-label="{e(t["lang_label"])}">🌐 {e(SHORT_NAME[slug])}</summary>
          <ul>
{menu}
          </ul>
        </details>
        <div class="header-dl-group">
          <a href="{APP_STORE.format(ct=campaign(slug, "header"))}" class="header-cta">{APPLE_SVG.format(s=16)}<span>{e(t["download"])}</span></a>
          <a href="{PLAY.format(ct=campaign(slug, "header"))}" class="header-cta">{PLAY_SVG.format(s=16)}<span>{e(t["download"])}</span></a>
        </div>
      </div>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <span>{e(t["badge"])}</span>
        </div>
        <h1>{t["h1_html"]}</h1>
        <p>{e(t["hero_p"])}</p>
        <div class="cta-group">
          {store_buttons(slug, "hero", "cta-primary", 20, t)}
          <a href="#how-it-works" class="cta-secondary">{e(t["cta_how"])}</a>
        </div>
      </div>
    </section>

    <section id="how-it-works">
      <div class="container text-center">
        <p class="section-label">{e(t["how_label"])}</p>
        <h2 class="section-title">{e(t["how_title"])}</h2>
        <p class="section-desc center">{e(t["how_desc"])}</p>
        <div class="steps">
{steps}
        </div>
      </div>
    </section>

    <section id="features">
      <div class="container text-center">
        <p class="section-label">{e(t["feat_label"])}</p>
        <h2 class="section-title">{e(t["feat_title"])}</h2>
        <p class="section-desc center">{e(t["feat_desc"])}</p>
        <div class="features-grid">
{features}
        </div>
      </div>
    </section>

    <section id="use-cases">
      <div class="container text-center">
        <p class="section-label">{e(t["use_label"])}</p>
        <h2 class="section-title">{e(t["use_title"])}</h2>
        <p class="section-desc center">{e(t["use_desc"])}</p>
        <div class="use-cases">
{uses}
        </div>
      </div>
    </section>

    <section id="reviews">
      <div class="container text-center">
        <p class="section-label">{e(t["rev_label"])}</p>
        <h2 class="section-title">{e(t["rev_title"])}</h2>
        <div class="testimonials">
{reviews}
        </div>
      </div>
    </section>

    <section id="faq">
      <div class="container text-center">
        <p class="section-label">{e(t["faq_label"])}</p>
        <h2 class="section-title">{e(t["faq_title"])}</h2>
        <div class="faq-list">
{faqs}
        </div>
      </div>
    </section>

    <section class="final-cta">
      <div class="container">
        <h2>{t["final_title_html"]}</h2>
        <p>{e(t["final_desc"])}</p>
        <div class="cta-group">
          {store_buttons(slug, "footer", "cta-primary", 20, t)}
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container footer-inner">
      <div class="footer-left">&copy; 2026 SyncMirror</div>
      <nav class="footer-links" aria-label="Footer">
        <a href="https://momoxie0202.github.io/">{e(t["privacy"])}</a>
        <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">{e(t["terms"])}</a>
      </nav>
    </div>
  </footer>

  <div class="lang-suggest" id="lang-suggest" role="region" aria-live="polite"></div>

  <script>
    (function () {{
      var PAGES = {suggest_js};
      var CURRENT = "{hreflang}";
      function pick(tag) {{
        tag = (tag || "").toLowerCase();
        if (/^zh-(hk|mo)|^zh-hant-(hk|mo)|^yue/.test(tag)) return "zh-HK";
        if (/^zh/.test(tag)) return "zh-TW";
        if (/^ko/.test(tag)) return "ko";
        if (/^ja/.test(tag)) return "ja";
        if (/^en/.test(tag)) return "en";
        return null;
      }}
      try {{ if (localStorage.getItem("syncmirror_lang_dismiss")) return; }} catch (e) {{}}
      var want = pick(navigator.language || "");
      if (!want || want === CURRENT || !PAGES[want]) return;
      var p = PAGES[want], box = document.getElementById("lang-suggest");
      var a = document.createElement("a");
      a.href = p.url; a.lang = want; a.hreflang = want; a.textContent = p.text + " →";
      var x = document.createElement("button");
      x.type = "button"; x.setAttribute("aria-label", "close"); x.textContent = "×";
      x.onclick = function () {{
        box.classList.remove("show");
        try {{ localStorage.setItem("syncmirror_lang_dismiss", "1"); }} catch (e) {{}}
      }};
      box.appendChild(a); box.appendChild(x); box.classList.add("show");
    }})();
  </script>
</body>
</html>
'''


def main():
    for slug, lang, hreflang, name in LOCALES:
        out = ROOT / "apps" / "syncmirror" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(slug, lang, hreflang, name), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
