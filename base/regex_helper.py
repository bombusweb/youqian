import re
QUESTION_REGEX = re.compile('[age|income|consume|property|term]')
QUESTION_REGEX = re.compile('age|income|consume')
name='consum'
match=QUESTION_REGEX.match(name)
if match:
    print match.group()