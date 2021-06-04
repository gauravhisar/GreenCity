def func(one,two):
    print(one,two)

s = {"one":"1","two":"2"}
print(*s)     
func(**s)
print(isinstance(5.0,float))
print("demo.some"[5:])
print('%04d' % 20000)