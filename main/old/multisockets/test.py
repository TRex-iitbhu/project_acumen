global f
f = True
def function():
    global f
    f = False
    print f
print f

function()

print f
