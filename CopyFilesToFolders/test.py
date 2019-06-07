
csv_list  = ['STUDYID', 1,2,3,4,5,6,7,8,9,0,]
moved_list = [3,4,5,6,7,10,11]

if 'STUDYID' in csv_list:
    csv_list.remove('STUDYID')
csv_set = set(csv_list)
moved_list = set(moved_list)

diff = csv_set.difference(moved_list)

print(diff)

unable = []
for i in diff:
    unable.append(i)

print(unable)
