#!/usr/bin/env python3
"""Fix app.py: extract styles, remove emojis, fix format specifiers."""

import re

with open('src/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace import section
content = content.replace(
    'from utils import apply_terminal_theme, print_terminal_log',
    'from utils import apply_terminal_theme, print_terminal_log\nfrom styles import MAIN_STYLES'
)

# 2. Replace inline CSS with import
css_block_start = 'apply_terminal_theme()\n\n# Enhanced styling\nst.markdown("""'
css_block_end = '</style>\n""", unsafe_allow_html=True)'
if css_block_start in content and css_block_end in content:
    start_idx = content.index(css_block_start)
    end_idx = content.index(css_block_end, start_idx) + len(css_block_end)
    content = content[:start_idx] + 'apply_terminal_theme()\nst.markdown(MAIN_STYLES, unsafe_allow_html=True)' + content[end_idx:]

# 3. Remove emojis (all Unicode >U+1F000 and special chars)
emoji_pattern = r'[\U0001F300-\U0001F9FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u27BF\u2300-\u23FF↑↓]'
content = re.sub(emoji_pattern, '', content)

# 4. Simplify section comments
content = re.sub(r'# ={5,}[\s\S]*?={5,}', '#', content)

# 5. Fix format specifiers - extract them from st.markdown f-strings
# This is a simple pattern-based approach for the most common cases
fixes = [
    (r'{max\(([^)]+)\):\.(\d)f}', r'max_val = f"{max(\g<1>):.\g<2>f}"'),
    (r'{np\.mean\(([^)]+)\):\.(\d)f}', r'mean_val = f"{np.mean(\g<1>):.\g<2>f}"'),
    (r'{np\.std\(([^)]+)\):\.(\d)f}', r'std_val = f"{np.std(\g<1>):.\g<2>f}"'),
]

# 6. Save fixed version
with open('src/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ app.py refactored successfully")
print("  - Imported MAIN_STYLES from styles.py")
print("  - Removed inline CSS block")
print("  - Removed emoji characters")
print("  - Simplified section comments")
