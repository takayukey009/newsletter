import csv
import os

# Define file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, '配信先', 'BLASTMAIL_userdata_filtered_v5.csv')
output_file = os.path.join(base_dir, '配信先', 'music_industry_contacts.csv')

# Define keywords for filtering
music_keywords = [
    # ===== 音楽直接 =====
    # 音楽・レコード基本
    '音楽', 'Music', 'MUSIC', 'Records', 'レコーズ', 'A&R',
    # ラジオ・FM
    'FM', 'ラジオ', 'RADIO', 'Radio',
    # 音響・サウンド
    '音響', 'サウンド', 'Sound',
    # レコード会社・音楽プロダクション
    'ソニー', 'ユニバーサル', 'ワーナー', 'エイベックス', 'キングレコード', 'ポニーキャニオン',
    'テイチク', 'ドリーミュージック', 'バップ', '日本コロムビア', 'ビクター', 'ヤマハ',
    'ライジング', 'アミューズ', 'スターダスト', 'ホリプロ', 'トイズファクトリー', 'クラウンレコード',
    'A-Sketch', 'サンライズミュージック', 'エムオン・エンタテインメント',
    # 楽曲・配信・出版
    '楽曲', '音楽出版', 'USEN', 'musicvoice',
    # 音楽配信プラットフォーム
    'Spotify', 'Apple Music', 'Apple', 'Amazon Music', 'LINE MUSIC', 'AWA', 'KKBOX', 'Deezer', 'AbemaTV', 'Abema',
    # テレビ音楽番組関連
    'MUSIC STATION', 'Mステ', '音楽番組', 'タイアップ',
    'EIGHT-JAM', 'CDTV', 'うたコン', 'のど自慢',
    'FNS歌謡祭', '紅白', 'ベストヒット', 'カウントダウンTV',
    'ミュージックフェア', 'SONGS', 'シブヤノオト',
    # ライブ・コンサート・イベント
    'ライブ', 'コンサート', 'イベント', 'Live', 'Concert',
    # 音楽IP・エンタテインメント（音楽系）
    '音楽IP', 'ミュージック', 'DYミュージック',
    # シングル・配信
    'シングル', '配信', 'SP盤',
    # テレビ局のエンターテインメント部門（音楽に近い）
    'エンターテインメント部', 'エンターテインメント',
    # 舞台・ミュージカル（歌うタレントに関連）
    'ミュージカル', '舞台',

    # ===== タイアップ狙い：映画・ドラマ + CM + キャスティング =====
    # 映画・ドラマ制作（主題歌/挿入歌タイアップ）
    'ドラマ', '映画', 'ストーリー制作', 'ドラマ制作', '映画制作', '映画企画',
    '映画事業', 'ドラマ映画', 'FOD', '映像企画',
    # CM制作・広告代理店（CMソングタイアップ）
    'CMプランナー', 'CM', 'クリエイティブディレクター',
    '広告', '博報堂', '電通', 'ADK', '東急エージェンシー',
    # キャスティング（タレント起用窓口）
    'キャスティング', 'casting', 'Casting',

    # ===== PR・認知狙い：エンタメメディア + 宣伝 =====
    # エンタメ系メディア・出版
    'エンタテインメント!', 'オリコン', '編集部', '編集',
    '記者', '取材', 'ニュース',
    # 宣伝・プロモーション部門
    '宣伝', 'プロモーション', 'PR', '広報',
]

# Also match by email domain for known music companies
music_email_domains = [
    'sonymusic.co.jp', 'umusic.com', 'wmg.com', 'avex.co.jp',
    'j-wavemusic.co.jp', 'sunrise-music.co.jp', 'musicvoice.jp',
    'nack5.co.jp', 'interfm.co.jp', 'bayfm.jp', 'jfn.co.jp',
    'joqr.co.jp',  # 文化放送
    'vap.co.jp',
]

print(f"Reading from: {input_file}")

filtered_rows = []
header = []

try:
    with open(input_file, mode='r', encoding='utf-8', errors='replace') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read header
        
        # Verify column indices
        try:
            company_idx = header.index('会社名')
            dept_idx = header.index('所属部署')
            name_idx = header.index('氏名')
            email_idx = header.index('E-Mail')
        except ValueError as e:
            print(f"Error: Required columns not found. Header: {header}")
            exit(1)

        for row in reader:
            if len(row) <= max(company_idx, dept_idx, email_idx):
                continue # Skip malformed rows
            
            company = row[company_idx] if row[company_idx] else ""
            dept = row[dept_idx] if row[dept_idx] else ""
            email = row[email_idx] if row[email_idx] else ""
            
            # Check if any keyword matches in company or department
            is_match = False
            for keyword in music_keywords:
                if keyword in company or keyword in dept:
                    is_match = True
                    break
            
            # Check if email domain matches known music companies
            if not is_match:
                for domain in music_email_domains:
                    if domain in email:
                        is_match = True
                        break
            
            if is_match:
                filtered_rows.append(row)

    # Save to output file
    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(filtered_rows)

    print(f"Filtered {len(filtered_rows)} contacts related to music industry.")
    print(f"Saved to {output_file}")
    
    # Display top 10 for verification
    print("\nTop 10 entries:")
    print(f"{header[company_idx]} | {header[dept_idx]} | {header[name_idx]}")
    print("-" * 50)
    for i, row in enumerate(filtered_rows[:10]):
        print(f"{row[company_idx]} | {row[dept_idx]} | {row[name_idx]}")

except FileNotFoundError:
    print(f"Error: File not found at {input_file}")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
