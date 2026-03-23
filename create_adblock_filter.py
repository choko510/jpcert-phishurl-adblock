import os
import csv
from urllib.parse import urlparse
from datetime import datetime

def create_filters():
    input_dir = "jpcert_phishurl_csvs"
    adblock_file = "adblock_filter.txt"
    domains_file = "domains.txt"
    hosts_file = "hosts_filter.txt"
    
    domains = set()

    print("CSVファイルからURLを抽出し、ドメインを解析しています...")
    
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
                                # URLスキームがない場合は補完して正しくパースできるようにする
                                if not url.startswith(('http://', 'https://')):
                                    url = 'http://' + url
                                
                                try:
                                    parsed = urlparse(url)
                                    domain = parsed.netloc
                                    # ポート番号が含まれている場合は除外
                                    if ':' in domain:
                                        domain = domain.split(':')[0]
                                    
                                    # IPアドレスやドメインとして有効な文字列か簡易チェック
                                    if domain and '.' in domain:
                                        domains.add(domain)
                                except Exception:
                                    pass

    print(f"解析完了。重複を除いて {len(domains)} 件のドメインを抽出しました。")
    print("各種形式のフィルターを保存中...")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Adblock形式 (uBlock Origin, AdGuardなど)
    with open(adblock_file, 'w', encoding='utf-8') as f:
        f.write("! Title: JPCERT Phishing URL Adblock Filter\n")
        f.write("! Description: Converted from JPCERTCC/phishurl-list\n")
        f.write(f"! Updated: {current_time}\n")
        f.write("! Expires: 1 days\n")
        for domain in sorted(domains):
            f.write(f"||{domain}^\n")

    # 2. ドメイン名のみのリスト (Pi-hole, NextDNS, 独自ツール用など)
    with open(domains_file, 'w', encoding='utf-8') as f:
        f.write(f"# JPCERT Phishing URL Domains List\n")
        f.write(f"# Updated: {current_time}\n")
        for domain in sorted(domains):
            f.write(f"{domain}\n")

    # 3. hostsファイル形式 (Windows, Mac, Linux OS標準用)
    with open(hosts_file, 'w', encoding='utf-8') as f:
        f.write(f"# JPCERT Phishing URL Hosts Filter\n")
        f.write(f"# Updated: {current_time}\n")
        for domain in sorted(domains):
            f.write(f"0.0.0.0 {domain}\n")

    print(f"変換が完了しました。以下のファイルを生成しました:\n- {adblock_file}\n- {domains_file}\n- {hosts_file}")

if __name__ == "__main__":
    create_filters()
