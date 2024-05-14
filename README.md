This skiplist is a dynamic unordered list type data structure that supports efficient access, insertion and deletion at arbitrary indices.<br>
The operations supported are similar to those supported by the ordinary python list.
Examples:
```python
xs = SkipList()
xs.append(1)
xs.append(5)
xs.append(3)
xs.insert(0, 2)
#xs is now [2, 1, 5, 3]
print(len(xs)) #prints 4
del xs[1] #deletes element at index 1
for x in xs:
  print(x, end=' ')
#above code prints 2 5 3
