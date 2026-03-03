import re

f = r'c:\Users\togawa_takayuki\.gemini\antigravity\若手メルマガ\index.html'

with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Add class='talent-col' to td elements with width='48%' valign='top'
content = content.replace('width="48%" valign="top"', 'class="talent-col" width="48%" valign="top"')

# Also add class to main container table
content = content.replace(
    'style="background-color:#ffffff;max-width:600px;width:100%;"',
    'class="main-container" style="background-color:#ffffff;max-width:600px;width:100%;"'
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(content)

count = content.count('class="talent-col"')
print(f'Added talent-col class to {count} elements')
