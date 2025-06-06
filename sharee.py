#!/usr/bin/env python3
# JL's Facebook Share Tool
# Interactive and User-Friendly Version

import requests, os, re, sys, json, time, random
from datetime import datetime
from time import sleep

# Session object
ses = requests.Session()

# Random user agents
ua_list = [
    "Mozilla/5.0 (Linux; Android 10; Wildfire E Lite Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36[FBAN/EMA;FBLC/en_US;FBAV/298.0.0.10.115;]",
    "Mozilla/5.0 (Linux; Android 11; KINGKONG 5 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36[FBAN/EMA;FBLC/fr_FR;FBAV/320.0.0.12.108;]",
    "Mozilla/5.0 (Linux; Android 11; G91 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.126 Mobile Safari/537.36[FBAN/EMA;FBLC/fr_FR;FBAV/325.0.1.4.108;]"
]
ua = random.choice(ua_list)

# Colored print helper
def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def banner():
    os.system("clear" if os.name == 'posix' else 'cls')
    print(color("""
     ██╗██████╗ 
     ██║██╔══██╗
     ██║██║  ██║
██   ██║██║  ██║
╚█████╔╝██████╔╝
 ╚════╝ ╚═════╝ 
""", '94'))  # Blue

    print(color("Author  : JL Magno", '96'))  # Cyan
    print(color("Facebook: https://facebook.com/jl.magno.2024", '96'))  # Cyan
    print(color("GitHub  : https://github.com/jl-magno/fb-spam-share-", '96'))  # Cyan
    print(color("-" * 50, '90'))  # Grey line
    print(color("Facebook Share Tool - Interactive Version", '95'))  # Purple
    print(color("-" * 50, '90'))  # Grey line

def login():
    banner()
    print(color("\nWelcome to JL's Facebook Share Tool!", '93'))  # Yellow
    print(color("Please follow these steps carefully:\n", '93'))
    
    print(color("1. Go to Facebook.com in your browser", '96'))
    print(color("2. Open Developer Tools (F12)", '96'))
    print(color("3. Go to Application > Cookies", '96'))
    print(color("4. Copy the entire cookie string\n", '96'))
    
    cookie_input = input(color("Please paste your Facebook cookie here: ", '92'))  # Green input

    if not cookie_input:
        print(color("\n❌ No cookie provided. Please try again.", '91'))
        time.sleep(2)
        return login()

    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookie_input.split("; ") if "=" in i}

    try:
        print(color("\n🔍 Verifying your cookie... Please wait...", '93'))
        data = ses.get("https://business.facebook.com/business_locations", headers={
            "user-agent": ua,
            "referer": "https://www.facebook.com/",
            "host": "business.facebook.com",
            "origin": "https://business.facebook.com",
            "upgrade-insecure-requests": "1",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "content-type": "text/html; charset=utf-8"
        }, cookies=cookies)

        find_token = re.search(r"(EAAG\w+)", data.text)
        if not find_token:
            print(color("\n❌ Token extraction failed. Please check your cookie and try again.", '91'))
            time.sleep(3)
            return login()

        token = find_token.group(1)
        with open("token.txt", "w") as f:
            f.write(token)
        with open("cookie.txt", "w") as f:
            f.write(cookie_input)

        print(color(f"\n✅ Success! Token extracted and saved.", '92'))  # Green
        print(color(f"Your access token: {token[:15]}...", '96'))  # Show partial token for security
        time.sleep(3)
        main_menu()

    except Exception as e:
        if os.path.exists("token.txt"): os.remove("token.txt")
        if os.path.exists("cookie.txt"): os.remove("cookie.txt")
        print(color("\n❌ Error: Cookie verification failed. Please get a fresh cookie.", '91'))  # Red
        print(color(f"Technical details: {str(e)}", '90'))  # Grey for error details
        time.sleep(3)
        login()

def main_menu():
    banner()
    print(color("\nMain Menu:", '95'))
    print(color("1. Start Sharing Posts", '96'))
    print(color("2. Check Saved Credentials", '96'))
    print(color("3. Delete Saved Credentials", '96'))
    print(color("4. Exit", '96'))
    
    choice = input(color("\nPlease choose an option (1-4): ", '92'))
    
    if choice == "1":
        start_sharing()
    elif choice == "2":
        check_credentials()
    elif choice == "3":
        delete_credentials()
    elif choice == "4":
        print(color("\nThank you for using JL's Facebook Share Tool!", '94'))
        exit()
    else:
        print(color("\nInvalid choice. Please try again.", '91'))
        time.sleep(2)
        main_menu()

def check_credentials():
    banner()
    print(color("\nSaved Credentials:", '95'))
    
    try:
        with open("token.txt", "r") as f:
            token = f.read()
            print(color(f"Access Token: {token[:15]}...", '96'))
    except:
        print(color("No saved token found.", '91'))
    
    try:
        with open("cookie.txt", "r") as f:
            cookie = f.read()
            print(color(f"Cookie: {cookie[:30]}...", '96'))
    except:
        print(color("No saved cookie found.", '91'))
    
    input(color("\nPress Enter to return to main menu...", '90'))
    main_menu()

def delete_credentials():
    banner()
    print(color("\nDelete Credentials:", '95'))
    
    if os.path.exists("token.txt"):
        os.remove("token.txt")
        print(color("Token file deleted.", '92'))
    else:
        print(color("No token file to delete.", '91'))
    
    if os.path.exists("cookie.txt"):
        os.remove("cookie.txt")
        print(color("Cookie file deleted.", '92'))
    else:
        print(color("No cookie file to delete.", '91'))
    
    input(color("\nPress Enter to return to main menu...", '90'))
    main_menu()

def start_sharing():
    banner()
    print(color("\nPost Sharing Tool", '95'))
    
    try:
        token = open("token.txt", "r").read()
        raw_cookie = open("cookie.txt", "r").read()
        cookie = {i.split("=")[0]: i.split("=")[1] for i in raw_cookie.split("; ") if "=" in i}
    except:
        if os.path.exists("token.txt"): os.remove("token.txt")
        if os.path.exists("cookie.txt"): os.remove("cookie.txt")
        print(color("\n❌ Error: No valid credentials found. Please login again.", '91'))
        time.sleep(3)
        return login()

    print(color("\nPlease enter the Facebook post URL you want to share.", '93'))
    print(color("Example: https://www.facebook.com/username/posts/123456789", '90'))
    link = input(color("\nPost URL: ", '96'))  # Cyan
    
    if not link.startswith(("http://", "https://")):
        print(color("\n❌ Invalid URL. Please include http:// or https://", '91'))
        time.sleep(2)
        return start_sharing()
    
    try:
        limit = int(input(color("\nNumber of shares to perform: ", '96')))  # Cyan
        if limit <= 0:
            print(color("\n❌ Please enter a positive number.", '91'))
            time.sleep(2)
            return start_sharing()
    except ValueError:
        print(color("\n❌ Please enter a valid number.", '91'))
        time.sleep(2)
        return start_sharing()

    print(color("\n🚀 Starting sharing process... Please wait...", '93'))
    start_time = datetime.now()
    success_count = 0

    try:
        for n in range(1, limit + 1):
            post = ses.post(
                f"https://graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}",
                headers={
                    "authority": "graph.facebook.com",
                    "cache-control": "max-age=0",
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": ua
                }, cookies=cookie
            ).text

            data = json.loads(post)
            if "id" in data:
                success_count += 1
                elapsed = str(datetime.now() - start_time).split('.')[0]
                print(color(f"✅ Share {n}/{limit} successful! (Elapsed: {elapsed})", '92'))  # Green
                # Add small delay between shares to avoid rate limiting
                time.sleep(random.uniform(1, 3))
            else:
                print(color(f"❌ Share {n} failed. Response: {data}", '91'))  # Red
                if data.get("error", {}).get("code") == 190:  # Invalid token error
                    print(color("⚠️ Your access token may have expired. Please login again.", '91'))
                    break

    except requests.exceptions.ConnectionError:
        print(color("\n❌ Network error. Please check your internet connection.", '91'))
    except Exception as e:
        print(color(f"\n❌ An error occurred: {str(e)}", '91'))
    
    print(color("\nSharing process completed!", '95'))
    print(color(f"Total shares attempted: {limit}", '96'))
    print(color(f"Successful shares: {success_count}", '92' if success_count > 0 else '91'))
    print(color(f"Elapsed time: {str(datetime.now() - start_time).split('.')[0]}", '96'))
    
    input(color("\nPress Enter to return to main menu...", '90'))
    main_menu()

if __name__ == "__main__":
    login()
