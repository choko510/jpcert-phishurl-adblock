# JPCERT Phishing URL Adblock Filter

JPCERT/CC が公開している「[フィッシングサイトURLリスト (JPCERTCC/phishurl-list)](https://github.com/JPCERTCC/phishurl-list)」に基づいて、広告ブロック機能やDNSシンクホールで使用できるフォーマットに自動変換したフィルターリストを提供しています。

このリポジトリのフィルターは、**毎月自動的に**最新のデータを取り込んで更新されます。

## 提供しているフィルター形式

使用しているツールに合わせて以下のいずれかの RAW URL を設定・購読してください。

### 1. Adblock 拡張機能向け (uBlock Origin, AdGuard など)
- **ファイル名**: `adblock_filter.txt`
- **形式**: `||domain.com^`
- **購読用URL**: `https://raw.githubusercontent.com/choko510/jpcert-phishurl-adblock/main/adblock_filter.txt`

### 2. 生のドメインリスト (Pi-hole, NextDNS, 自作スクリプト向け)
- **ファイル名**: `domains.txt`
- **形式**: ホスト名/ドメイン名のみ (1行1件)
- **購読用URL**: `https://raw.githubusercontent.com/choko510/jpcert-phishurl-adblock/main/domains.txt`

### 3. hosts ファイル形式 (Windows, Mac, Linux の OS標準設定など)
- **ファイル名**: `hosts_filter.txt`
- **形式**: `0.0.0.0 domain.com`
- **購読用URL**: `https://raw.githubusercontent.com/choko510/jpcert-phishurl-adblock/main/hosts_filter.txt`

## 免責事項

本リポジトリは [JPCERTCC/phishurl-list](https://github.com/JPCERTCC/phishurl-list) のデータを利用して非公式に自動構築されるものであり、提供されるドメインリストの正確性や、これによる特定の通信障害（正常なサイトが見られなくなるなど）について、当リポジトリの管理者は一切の責任を負いません。
