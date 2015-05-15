def dfs(elem, pair, result):
    children = elem.getchildren()

    if pair in elem.items():
        result.append(elem)
    else:
        for c in children:
            dfs(c, pair, result)


import xml.etree.ElementTree as ET

with open('raw_data.xml') as f:
    text = f.read()

text = ' '.join(text.split('\n'))

tree = ET.parse('raw_data.xml')
root = tree.getroot()

results = []

pairs = {('class', 'network'), ('class', 'storage')}

for p in pairs:
    dfs(root, p, results)

for n in results:
    print n

    for c in n.getchildren():
        print c
