import os
import csv
from urllib.parse import urlparse
from datetime import datetime

def create_filters():
    input_dir = "jpcert_phishurl_csvs"
    adblock_file = "adblock_filter.txt"
    domains_file = "domains.txt"
    hosts_file = "hosts_filter.txt"
    
    adblock_rules = set()
    domains_set = set()
    
    # 誤検知を防ぐためのホワイトリスト（著名なリダイレクトや短縮URL事業者など）
    whitelist = {
        'www.google.com', 'google.com', 'translate.google.com', 'translate.goog',
        't.co', 'bit.ly', 'tinyurl.com', 'ow.ly', 'is.gd', 'goo.gl',
        'bing.com', 'www.bing.com', 'yahoo.co.jp', 'search.yahoo.co.jp',
        'youtube.com', 'www.youtube.com', 'facebook.com', 'www.facebook.com',
        'instagram.com', 'twitter.com', 'x.com', 'line.me'
    }

    print("CSVファイルからURLを抽出し、解析しています...")
    
    # フォルダ内を探索してCSVを読み込む
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.csv'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                    reader = csv.reader(f)
                    try:
                        next(reader) # ヘッダーをスキップ
                    except StopIteration:
                        continue
                    
                    for row in reader:
                        if len(row) >= 2:
                            url = row[1].strip().replace('\ufeff', '').replace('\u200b', '')
                            if url:
                                # URLスキームがない場合は補完
                                if not url.startswith(('http://', 'https://')):
                                    url = 'http://' + url
                                
                                try:
                                    parsed = urlparse(url)
                                    domain = parsed.netloc
                                    if ':' in domain:
                                        domain = domain.split(':')[0]
                                    domain = domain.lower()
                                    
                                    if domain and '.' in domain:
                                        # ドメインリストやHosts用にはドメインのみを登録（ホワイトリストは除外）
                                        if domain not in whitelist:
                                            domains_set.add(domain)
                                        
                                        # Adblock用のルール作成
                                        if (parsed.path == "" or parsed.path == "/") and not parsed.query and not parsed.fragment:
                                            # ホストのみの場合
                                            if domain not in whitelist:
                                                adblock_rules.add(f"||{domain}^")
                                        else:
                                            # フルURLの場合 (パスやクエリあり)
                                            url_no_scheme = url.split('://', 1)[-1]
                                            adblock_rules.add(f"||{url_no_scheme}")
                                except Exception:
                                    pass

    print(f"解析完了。対象ドメイン: {len(domains_set)} 件、Adblockルール: {len(adblock_rules)} 件")
    print("各種形式のフィルターを保存中...")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Adblock形式 (uBlock Origin, AdGuardなど)
    with open(adblock_file, 'w', encoding='utf-8') as f:
        f.write("! Title: JPCERT Phishing URL Adblock Filter\n")
        f.write("! Description: Converted from JPCERTCC/phishurl-list\n")
        f.write(f"! Updated: {current_time}\n")
        f.write("! Expires: 1 days\n")
        for rule in sorted(adblock_rules):
            f.write(f"{rule}\n")

    # 2. ドメイン名のみのリスト (Pi-hole, NextDNS, 独自ツール用など)
    with open(domains_file, 'w', encoding='utf-8') as f:
        f.write(f"# JPCERT Phishing Domains List\n")
        f.write(f"# Updated: {current_time}\n")
        for domain in sorted(domains_set):
            f.write(f"{domain}\n")

    # 3. hostsファイル形式 (Windows, Mac, Linux OS標準用)
    with open(hosts_file, 'w', encoding='utf-8') as f:
        f.write(f"# JPCERT Phishing Hosts Filter\n")
        f.write(f"# Updated: {current_time}\n")
        for domain in sorted(domains_set):
            f.write(f"0.0.0.0 {domain}\n")

    print(f"変換が完了しました。以下のファイルを生成しました:\n- {adblock_file}\n- {domains_file}\n- {hosts_file}")

if __name__ == "__main__":
    create_filters()
