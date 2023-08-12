for key in ['master', 'sde', 'ml', 'industry', 'research']:
    if key not in globals():
        if key in ['industry', 'research']:
            globals()[key] = True
        else:
            globals()[key] = False

if master:
    sde = True
    ml = True

outFile.writelines([
    r'\newcommand{\role}{}',
    r'\newif\ifroleset',
    r'\rolesetfalse',
])

if sde:
    outFile.writeLines([
        r'\renewcommand{\role}{Software Developer}',
        r'\rolesettrue'
    ])
