potential_title = 'SummaryEvaluationwithandwithoutReferences'
lines = ['Summary Evaluation', 'with and without References']
res = ''
for line in lines:
    scan = line.strip()
    if(potential_title.find(scan)):
        res = res + line + ' '
print('res : ')
print(res)
        