import os
import csv
from urllib.parse import urlparse

def create_adblock_filter():
    input_dir = "jpcert_phishurl_csvs"
    output_file = "adblock_filter.txt"
    domains = set()

    print("CSVファイルからURLを抽出し、ドメインを解析しています...")
    
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
    print("Adblockフィルター形式で保存中...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("! Title: JPCERT Phishing URL Adblock Filter\n")
        f.write("! Description: Converted from JPCERTCC/phishurl-list\n")
        f.write("! Expires: 1 days\n")
        for domain in sorted(domains):
            f.write(f"||{domain}^\n")

    print(f"変換が完了しました。フィルターファイル: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    create_adblock_filter()
