from curl_cffi import requests
from urllib.parse import urljoin
import argparse, re, random, os
from datetime import datetime

BROWSERS = ['chrome110', 'chrome107', 'chrome104', 'chrome101', 'chrome100', 'chrome99', 
            'edge101', 'edge99', 'safari15_5', 'safari15_3', 'safari_ios']

def fetch_akamai_script(url, output='akamai_script.js'):
    os.makedirs('data', exist_ok=True)
    
    browser = random.choice(BROWSERS)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[+] {browser}")
    
    session = requests.Session()
    r = session.get(url, impersonate=browser, allow_redirects=True)
    
    html = r.text
    parts = html.split('</body>')
    before = parts[0] if parts else html
    
    scripts = re.findall(r'<script[^>]+src="([^"]+)"[^>]*></script>', before)
    if not scripts:
        print("[-] no scripts found")
        exit(1)
    
    script_path = scripts[-1]
    target = urljoin(r.url, script_path)
    print(f"[+] {script_path}")
    
    js = session.get(target, impersonate=random.choice(BROWSERS))
    with open(output, 'w') as f: f.write(js.text)
    
    with open('data/cookies.txt', 'a') as f:
        f.write(f"\n[{timestamp}] {browser}\n")
        for name, value in session.cookies.items():
            f.write(f"{name}={value}\n")
    
    with open('data/timestamps.txt', 'a') as f:
        f.write(f"{timestamp} | {browser} | {script_path} | {len(js.content)} bytes\n")
    
    print(f"[+] {len(js.content)} bytes -> {output}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--url', required=True)
    p.add_argument('--output', default='akamai_script.js')
    args = p.parse_args()
    fetch_akamai_script(args.url, args.output)
