import time
import random
import requests
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ----------------- 1. DUMMY HTTP SERVER FOR RENDER ----------------- #
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is Running 24/7!")

    def log_message(self, format, *args):
        return

def start_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# ----------------- 2. DISCORD BOT LOGIC ----------------- #
# Render environment variable se Bot Token uthayega
BOT_TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("USER_TOKEN")
CHANNEL_ID = "1410924658840178738"

paragraphs = [
    (
        "Order flow analysis gives advanced traders a deeper look into the actual buying and selling "
        "transactions taking place in real time across the market order book. By closely observing "
        "aggressive market orders versus passive limit orders, participants can identify true institutional "
        "accumulation, absorption zones, and sudden shifts in market sentiment before they reflect clearly on standard charts."
    ),
    (
        "Volume spread analysis (VSA) focuses extensively on the complex relationship between price spread, "
        "trading volume, and the final closing price of individual bars or candlesticks. This methodology "
        "helps uncover hidden market anomalies, such as professional smart money trapping retail breakout traders "
        "or shaking out weak hands prior to a major sustained directional move."
    ),
    (
        "Fibonacci retracement and extension levels serve as mathematical reference points derived from natural "
        "mathematical sequences that frequently act as inflection points during market pullbacks. When combined "
        "with structural support and resistance zones, these ratios help traders locate high-probability areas "
        "to manage risk and optimize their reward-to-risk ratios."
    ),
    (
        "Moving averages remain among the most popular and reliable trend-following technical tools because they "
        "effectively smooth out erratic price fluctuations and noise. Utilizing multiple timeframe moving average "
        "confluences allows participants to instantly gauge the overarching market bias, filtering out minor counter-trend "
        "corrections and keeping them aligned with major institutional trends."
    ),
    (
        "Momentum divergence is a powerful warning sign that occurs when price action prints a new extreme high or low "
        "while an underlying oscillator fails to confirm the move. This underlying loss of momentum often hints at "
        "waning participant interest, warning traders of potential trend exhaustion and an impending reversal or deep correction."
    ),
    (
        "Volatility squeezes develop during extended periods of market consolidation and tight range-bound trading "
        "where price compression reaches historical extremes. As Bollinger Bands contract inside Keltner Channels, "
        "it signals that explosive energy is building up, typically preceding a massive high-velocity breakout move "
        "in either direction."
    ),
    (
        "Dynamic trailing stop-loss orders allow active traders to continuously protect accumulated floating profits "
        "while giving winning positions enough breathing room to capture extended macro trends. Properly managing "
        "trailing stops ensures that successful trades are never allowed to turn into losing positions, safeguarding overall portfolio equity."
    ),
    (
        "Fixed fractional position sizing is a disciplined risk management framework where a trader risks the exact "
        "same percentage of total account equity on every single setup. This mathematical approach guarantees "
        "survival through inevitable losing streaks, preventing emotional decision-making from eroding trading capital."
    ),
    (
        "Mental capital and psychological resilience are just as important as financial capital for active market participants. "
        "Maintaining absolute emotional control during high-volatility events, accepting losses without revenge trading, "
        "and sticking strictly to a well-tested trading plan separate consistently profitable professionals from retail novices."
    )
]

url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": f"Bot {BOT_TOKEN}",  # Official Bot Token ke liye 'Bot ' prefix zaroori hai
    "Content-Type": "application/json"
}

available_paragraphs = paragraphs.copy()
random.shuffle(available_paragraphs)
msg_count = 0

print("[+] Official Bot Auto-Poster Started!", flush=True)

print("[INFO] Bot starting up, waiting 15 seconds before first message...", flush=True)
time.sleep(15)

while True:
    try:
        if not available_paragraphs:
            available_paragraphs = paragraphs.copy()
            random.shuffle(available_paragraphs)
            print("[INFO] Reshuffled paragraphs.", flush=True)

        message = available_paragraphs.pop()
        data = {"content": message}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code in (200, 201):
            msg_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Message #{msg_count} Sent Successfully!", flush=True)
            
            # Har 5 minute (300 seconds) ka gap
            wait_time = 300 
            print(f"[WAIT] Next message in {wait_time // 60} minutes ({wait_time} seconds)...", flush=True)
            time.sleep(wait_time)

        elif response.status_code == 429:
            try:
                retry_after = response.json().get("retry_after", 120)
            except Exception:
                retry_after = 120 
            print(f"[RATE LIMIT] Waiting for {retry_after} seconds...", flush=True)
            time.sleep(retry_after + 5)

        else:
            print(f"[ERROR] Failed. Code: {response.status_code}, Response: {response.text}", flush=True)
            time.sleep(30)

    except Exception as e:
        print(f"[EXCEPTION] Error: {e}", flush=True)
        time.sleep(30)
