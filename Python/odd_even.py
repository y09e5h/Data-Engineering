num=int(input("enter the number : "))
if num%2==0:
    print("even number")
else:
    print("odd number")

message=f"{num} is even" if num%2==0 else f"{num} is odd"
print(message)

