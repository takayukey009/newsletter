
import csv
import os

input_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_final.csv'
output_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_filtered_v2.csv'
candidates_file = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\agency_candidates.txt'

# 1. EXPLICIT REMOVAL LIST
remove_targets = [
    "狛江市",
    "ベルキッスコーポレーション",
    "吉本興業",
    "よしもとクリエイティブ",
    "エクセルホテル東急",
    "カシオ計算機",
    "ケイファイブ",
    "STARTO"
]

# 2. KEYWORDS FOR CANDIDATE LISTING
agency_keywords = [
    "芸能",
    "プロダクション",
    "エンターテインメント",
    "エンタテインメント", # Spelling variation
    "モデル",
    "タレント",
    "マネジメント",
    "レコード",
    "ミュージック",
    "キャスティング",
    "Casting",
    "Music",
    "Records",
    "Production",
    "Agency",
    "Entertainment",
    "Model",
    "Talent",
    "Management",
    "Group" # risky
]

def should_remove_explicitly(company):
    if not company:
        return False
    for target in remove_targets:
        if target in company:
            return True
    # Special check for STARTO/Yoshimoto variations just in case
    return False

def is_agency_candidate(company):
    if not company:
        return False
    for keyword in agency_keywords:
        if keyword in company:
            return True # Found a keyword
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

    print(f"Total rows before: {len(rows)}")

    kept_rows = []
    removed_explicitly = []
    candidates = []

    for row in rows:
        company = row.get("会社名", "").strip().replace("　", " ")
        name = row.get("氏名", "").strip().replace("　", " ")
        
        # 1. Explicit Removal
        if should_remove_explicitly(company):
            # Safe print for unicode
            try:
                msg = f"{company} ({name})"
                print(f"Removing: {msg}")
            except UnicodeEncodeError:
                msg = f"(Company with special char) ({name})"
                print(msg)
            
            removed_explicitly.append(msg)
            continue # Skip adding to kept_rows

        # 2. Candidate Identification (from kept rows)
        if is_agency_candidate(company):
            candidates.append(f"{company} ({name})")
        
        kept_rows.append(row)

    # Output Results
    print(f"Removed explicitly: {len(removed_explicitly)}")

    # 3. Filter Internal Emails (gate-agency.com)
    final_rows = []
    removed_internal = 0
    for row in kept_rows:
        email = row.get("E-Mail", "").strip()
        if "gate-agency.com" in email:
            removed_internal += 1
            # print(f"Removing internal email: {email}") # Optional: print removed emails
        else:
            final_rows.append(row)
            
    print(f"Removed internal emails (gate-agency.com): {removed_internal}")

    print(f"Candidates found: {len(candidates)}")
    
    # Save Candidates
    with open(candidates_file, mode='w', encoding='utf-8') as f:
        f.write("=== Potential Agency Candidates (Please review) ===\n")
        f.write("\n".join(sorted(candidates))) # Sort for easier reading
    print(f"Saved candidates to {candidates_file}")

    # Save Filtered CSV
    # V3 output for internal email filtering
    # V5 output: Match layout of BLASTMAIL_create.csv
    # Format: "氏名","会社名","E-Mail","所属部署" (All quoted)
    output_file_v5 = r'C:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\配信先\BLASTMAIL_userdata_filtered_v5.csv'
    
    # Exact column order from template
    target_fields = ["氏名", "会社名", "E-Mail", "所属部署"]
    
    with open(output_file_v5, mode='w', encoding='utf-8', newline='') as outfile:
        # quoting=csv.QUOTE_ALL to ensure all fields are quoted like the template
        writer = csv.DictWriter(outfile, fieldnames=target_fields, extrasaction='ignore', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(final_rows)
    print(f"Saved filtered CSV to {output_file_v5}")

if __name__ == "__main__":
    main()
