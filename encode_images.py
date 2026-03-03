import re
import urllib.parse

html_file = r'c:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\index.html'

def encode_url(match):
    url = match.group(1)
    # Only encode if it contains Japanese (non-ascii)
    try:
        url.encode('ascii')
        return f'src="{url}"' # No change needed
    except UnicodeEncodeError:
        # Split by / to encode segments specifically, or just quote the whole path if it's a simple file path
        # GitHub Pages handles encoded paths fine.
        # We need to preserve the protocol/domain if present, or just encode the path components.
        # Simple approach: quote the path part.
        
        # However, urllib.parse.quote will encode : and / if not careful.
        # safe chars: /:
        encoded_url = urllib.parse.quote(url, safe='/:?=&')
        return f'src="{encoded_url}"'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Configurable regex to match src="..."
# Matching src="([^"]+)"
new_content = re.sub(r'src="([^"]+)"', encode_url, content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated index.html with URL-encoded paths.")
