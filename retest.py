import re
import requests


return_data=requests.get(f"https://dict.youdao.com/example/blng/eng/tutor/#keyfrom=dict.main.moreblng")
html=return_data.text
pattern=re.compile(r'<div id="bilingual" class="trans-container  tab-content" style="display:block">(.*?)</div>',re.S)
sentence_pattern=re.findall(pattern, html)
print(sentence_pattern)