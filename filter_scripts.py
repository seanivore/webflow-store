import re
import sys

# Read blob content as bytes
content = sys.stdin.buffer.read()
try:
    # Try decoding as UTF-8
    text_content = content.decode('utf-8')
except UnicodeDecodeError:
    # If not decodable text (e.g., an image), pass through unchanged
    sys.stdout.buffer.write(content)
    sys.exit(0)

# Regex for FB Pixel block - made more specific to avoid removing other scripts
# Matches the typical structure including the !function wrapper and the fbq calls
fb_pattern = re.compile(
    r'<script type="text/javascript">\s*'
    r'!function\(f,b,e,v,n,t,s\).*?'  # Start of the FB wrapper
    r'https://connect\.facebook\.net/en_US/fbevents\.js.*?' # The script src
    r'fbq\(\'init\',.*?\).*?' # fbq init call
    r'fbq\(\'track\',\s*\'PageView\'\);' # fbq track call
    r'\s*</script>', # Closing tag
    re.DOTALL | re.IGNORECASE
)

# Regex for GTag script tag using the src
gtag_src_pattern = re.compile(
    r'<script\s+async(?:="")?\s+src="https://www\.googletagmanager\.com/gtag/js.*?</script>',
    re.DOTALL | re.IGNORECASE
)

# Regex for the GTag config script block
# Matches the dataLayer init and the gtag('config', ...) call
gtag_config_pattern = re.compile(
    r'<script type="text/javascript">\s*'
    r'window\.dataLayer\s*=\s*window\.dataLayer.*?' # dataLayer init
    r'gtag\(\'config\',.*?\);' # gtag config call
    r'\s*</script>', # Closing tag
    re.DOTALL | re.IGNORECASE
)

# Remove the script blocks
text_content = fb_pattern.sub('', text_content)
text_content = gtag_src_pattern.sub('', text_content)
text_content = gtag_config_pattern.sub('', text_content)

# Write modified content back
sys.stdout.buffer.write(text_content.encode('utf-8'))