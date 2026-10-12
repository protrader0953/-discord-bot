# App start hote hi pehla message turant bhejne ke liye
# Pehle 15 seconds ka rest denge taaki connection stable ho jaye
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
                # Discord kabhi-kabhi JSON ki jagah plain text deta hai
                retry_after = response.json().get("retry_after", 120)
            except Exception:
                retry_after = 120 
            print(f"[RATE LIMIT] Discord 429 hit. Waiting for {retry_after} seconds...", flush=True)
            time.sleep(retry_after + 5)

        else:
            # Yahan exact error print hoga ki Discord kya bol raha hai
            print(f"[ERROR] Failed. Code: {response.status_code}, Response: {response.text}", flush=True)
            time.sleep(30)

    except Exception as e:
        print(f"[EXCEPTION] Error: {e}", flush=True)
        time.sleep(30)
