import csv
import os

input_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_filtered.csv'
output_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_final.csv'

# 1. CUT LIST (Name, Optional Company)
# If Company is None, remove by Name only.
remove_targets = [
    ("炭𥧄友和", "株式会社ソイソーズ"),
    ("白島まな", None),
    ("嶋岡隆", "Office Shimarl"),
    ("吉岡詩織", "株式会社マッシュビューティーラボ"),
    ("杉春芳", "アソビシステム株式会社"),
    ("彩蘭弥", "Alaya"),
    ("永田彩子", None),
    ("佐伯エミー", None),
    ("水谷繭子", "株式会社82style"),
    ("Tomoko Asano", "NZ NETWORK"),
    ("小池藍", "GO FUND, LLP"),
    ("加藤豊紀", "エイベックス・クリエイター・エージェンシー株式会社"),
    ("加藤信介", "エイベックス・クリエイター・エージェンシー株式会社"),
    ("名越恵里奈", "株式会社マッシュ"),
    ("永田純子", "株式会社マッシュ"),
    ("石栗由佳", "株式会社東京ドーム"),
    ("西見敬一郎", "株式会社東京ドーム"),
    ("三浦剛", "GOMIURA"),
    ("穂満律子", "株式会社パルコ"),
    ("菊野長正", "狛江市"),
    ("Ayako Miura", "tulsa"), # "Ayako Miura tulsa"
    ("佐藤桜", "アンファー株式会社"),
    ("勝木拓郎", "株式会社MONSTER DIVE"),
    ("塚本美穂", "Seed&Flower合同会社"),
    ("重野謙介", "サントリー株式会社"),
    ("武藤新二", "株式会社George P .Johnson")
]

def should_remove(row):
    name = row.get("氏名", "").strip().replace("　", " ")
    company = row.get("会社名", "").strip().replace("　", " ")
    
    for target_name, target_company in remove_targets:
        # Normalize target name too
        target_name_clean = target_name.replace("　", " ")
        
        if target_name_clean == name:
            if target_company is None:
                return True
            # Partial match for company can be safer if there are slight variations
            if target_company in company or company in target_company:
                return True
    return False

def main():
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return

    rows = []
    with open(input_file, mode='r', encoding='utf-8-sig', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    print(f"Total rows before refinement: {len(rows)}")

    # 1. REMOVE
    kept_rows = []
    removed_count = 0
    for row in rows:
        if should_remove(row):
            removed_count += 1
            try:
                print(f"Removing: {row['氏名']} ({row['会社名']})")
            except UnicodeEncodeError:
                print(f"Removing: (Name with special char) ({row['会社名']})")
        else:
            kept_rows.append(row)
    
    print(f"Removed {removed_count} rows based on cut list.")

    # 2. MODIFY
    # 山邉博文　関西テレビ放送株式会社 -> 株式会社ギークサイト
    modified_count = 0
    for row in kept_rows:
        name = row.get("氏名", "").strip().replace("　", " ")
        company = row.get("会社名", "").strip()
        
        if name == "山邉博文" and "関西テレビ放送株式会社" in company:
            row["会社名"] = "株式会社ギークサイト"
            modified_count += 1
            print(f"Modified: {name} company updated to 株式会社ギークサイト")

    # 3. DEDUPLICATE
    # 久下右京　株式会社AOI Pro.
    # Logic: Keep the one with status '配信中' (delivering) or if both same, keep first.
    # Looking at data: 
    # Line 13: 配信中, ... ukyo...
    # Line 41: エラー停止, ... ykuo... (typo in duplicate)
    
    final_rows = []
    kuge_seen = False
    
    # We will do a generic dedupe or specific? User asked for specific "久下右京".
    # But usually dedupe implies keeping valid email.
    
    for row in kept_rows:
        name = row.get("氏名", "").strip().replace("　", " ")
        company = row.get("会社名", "").strip()
        
        if name == "久下右京" and "AOI Pro." in company:
            if kuge_seen:
                print(f"Removing duplicate for: {name}")
                continue # Skip this duplicate
            else:
                # If this is the "Error" one, we might want to wait for the "Good" one?
                # But lists are usually ordered. Line 13 comes before Line 41.
                # Line 13 is "配信中" (Good). Line 41 is "エラー停止" (Error).
                # So if we keep the first one we find, we keep the Good one.
                kuge_seen = True
                final_rows.append(row)
        else:
            final_rows.append(row)

    print(f"Total rows after refinement: {len(final_rows)}")

    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)
        
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
