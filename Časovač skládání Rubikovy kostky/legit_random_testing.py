lst=[]
side_length=4
for i in range(side_length**2):
	lst.append(i+1)
print(lst)
square=list(zip(*[iter(lst)]*side_length))
rows=len(square)
columns=len(square[0])
c=columns*rows
print(c)


"""
for i in range(rows)
	for j in range(columns)
		square.append(rows|columns)
"""
set1=set([1,2,3,4,5])
set2=set([1,2,3,5,4])
print(set1==set2)
r="red"
b="blue"
o="orange"
g="green"

item1=["15F'"][0]
#item1=[]
item2=["15F"][0]

print(item1[:-1])
print(item2[:-1])
print(item1==item2[:-1])
print(item1[:-1]==item2)
a=list(range(10))
print(list(reversed(range(10))))
piece=11
side_length=7
layer=piece-(piece//side_length)*side_length+1
print(layer)