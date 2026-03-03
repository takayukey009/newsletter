import re

html_file = r'c:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\index.html'

def display_img_src(html_content):
    img_tags = re.findall(r'<img src="([^"]+)"', html_content)
    # Check if they look encoded
    for src in img_tags:
        print(f"Image Source: {src}")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

display_img_src(content)
