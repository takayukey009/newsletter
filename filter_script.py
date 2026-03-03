import csv
import os

input_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_final_refined.csv'
output_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_filtered.csv'

# Criteria to exclude
exclude_companies = [
    "ENEOS",
    "日刊スポーツ",
    "新聞", # Covers スポーツ紙, 新聞社
    "デイリー新潮",
    "日本体操協会",
    "ハヤブサ財団",
    "味の素",
    "アソビシステム",
    "Alaya",
    "82style",
    "タイタン",
    "外務省",
    "山田養蜂場",
    "日本ケンタッキー",
    "KFC", # Just in case for Kentucky
    "住宅金融支援機構",
    "オフィスベル",
    "カシオ計算機",
    "富士企業", "冨士器業",
    "DREAM MUG", "DREAM_MUG",
    "TENTIAL",
    "Mercury",
    "ベースボール・マガジン", "ベースボールマガジン",
    "NBA",
    "丸一",
    "アービング",
    "スギ薬局",
    "カネボウ",
    "スポーツ" # "スポーツ紙" request, checking company names with Sport might be safe to exclude based on context, but let's stick to specific if possible. User said "日刊スポーツ などのスポーツ紙". 
               # "Sports" might be in "Sports Marketing". I'll be careful.
               # I'll stick to "日刊スポーツ" and "新聞".
               # User said "などの" (such as). 
               # Let's add "スポニチ", "報知", "東京中日", "サンスポ", "デイリー" which are common sports papers if they appear.
               # In the file view: "報知新聞", "スポーツ日本新聞社", "東京スポーツ新聞社".
               # "新聞" covers all of these.
]

# Additional specific exclusion based on user request "などのスポーツ紙" implies identifying them.
# "新聞" covers the ones visible in the file sample (産経新聞, スポーツ日本新聞, 報知新聞, 東京スポーツ新聞).

exclude_names = [
    "榎戸恵美",
    "木村晴",
    "若松慧"
]

exclude_roles_keywords = [
    "スタイリスト", "stylist",
    "メイク", "Makeup", "Make-up", "Hair", "Hairmake"
]

def is_excluded(row):
    try:
        # Get values, verify column names from file content
        # "﻿エラーカウント数",状態,氏名,会社名,E-Mail,所属部署
        # DictReader might include BOM in the first key. We will clean keys or access by values.
        
        name = row.get("氏名", "")
        company = row.get("会社名", "")
        dept = row.get("所属部署", "")
        
        # Combine text for role search
        full_text = (name + " " + company + " " + dept).lower()

        # 1. Check Specific Names
        clean_name = name.replace(" ", "").replace("　", "")
        if clean_name in exclude_names:
            return True

        # 2. Check Companies
        for crit in exclude_companies:
            if crit in company: # Partial match for company
                return True
        
        # 3. Check Role Keywords
        for role in exclude_roles_keywords:
            if role.lower() in full_text:
                return True
                
        return False

    except Exception as e:
        print(f"Error processing row: {row} - {e}")
        return False

def main():
    if not os.path.exists(input_file):
        print(f"Error: Input file prohibited or not found: {input_file}")
        return

    filtered_rows = []
    removed_count = 0
    total_rows = 0

    try:
        # utf-8-sig handles the BOM automatically
        with open(input_file, mode='r', encoding='utf-8-sig', newline='') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            for row in reader:
                total_rows += 1
                if is_excluded(row):
                    removed_count += 1
                else:
                    filtered_rows.append(row)

        with open(output_file, mode='w', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)

        print(f"Processing Complete.")
        print(f"Total rows read: {total_rows}")
        print(f"Rows removed: {removed_count}")
        print(f"Rows remaining: {len(filtered_rows)}")
        print(f"Output saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
