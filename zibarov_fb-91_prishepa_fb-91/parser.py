from pyparsing import alphas, nums, Word, Optional, Suppress

s = 'CREATE popa (popochka [INDEXED], one_more, two_more [INDEXED]);'
i = 0
command = Word(alphas)
name = Word(alphas + nums + '_')
INDEXED = Optional(Suppress('[') + 'INDEXED' + Suppress(']'))
parse_module = command + name + Suppress('(') + name + INDEXED

while i < s.count(','):
    parse_module = parse_module + Suppress(',') + name + INDEXED
    i = i + 1
i = 0

parse_module + parse_module + ')' + Suppress(';')
parsed = parse_module.parseString(s).asList()

parsed[0] = parsed[0].lower()
print(len(parsed))
while i < len(parsed):
    if parsed[i].lower() == 'indexed':
        parsed[i] = parsed[i].lower()
    i = i + 1


print(parsed)
