import os
import urllib.request
import json

def download_csvs():
    print("リポジトリのツリー情報を取得中...")
    tree_url = "https://api.github.com/repos/JPCERTCC/phishurl-list/git/trees/main?recursive=1"
    
    try:
        req = urllib.request.Request(tree_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            tree_data = json.loads(response.read().decode())
    except Exception as e:
        print(f"ツリー情報の取得に失敗しました: {e}")
        return

    csv_files = [item for item in tree_data.get('tree', []) if item['type'] == 'blob' and item['path'].endswith('.csv')]
    
    if not csv_files:
        print("CSVファイルが見つかりませんでした。")
        return
        
    print(f"{len(csv_files)}個のCSVファイルが見つかりました。ダウンロードを開始します...")
    
    output_dir = "jpcert_phishurl_csvs"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, item in enumerate(csv_files, 1):
        path = item['path']
        raw_url = f"https://raw.githubusercontent.com/JPCERTCC/phishurl-list/main/{path}"
        
        # ディレクトリ構造を維持するためにパスを作成します
        local_path = os.path.join(output_dir, path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        print(f"[{i}/{len(csv_files)}] ダウンロード中: {path}...")
        try:
            req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(local_path, 'wb') as f:
                    f.write(response.read())
        except Exception as e:
            print(f"{path} のダウンロードに失敗しました: {e}")

    print("すべてのダウンロードが完了しました！")
    print(f"保存先: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    download_csvs()
