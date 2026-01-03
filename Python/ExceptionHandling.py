x = 10 #input("Enter Number 1 :")
y = 5 #input("Enter Number 2 :")
d=0
try:
    d = int(x)/int(y)
except ZeroDivisionError as e:
    print("Division Error : ",e)
    d=-1
except ValueError as e:
    print("Value Error : ",e)
    d=-1
except:
    print("Unknown Error")
finally:
    print(d)

print(f"Division = {d}")



file_name="letter.txt"

try:
    f = open(file_name,"w")
    f.write("Love you my cute Cactus :)")
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(e)
finally:
    if f:
        f.close()
    print("file closed")
Balance=0
def deposit(amount):
    global Balance
    if amount > 0:
        Balance=Balance+amount
        print(f"Amount deposited {amount} , Total Balance : {Balance}")
    else:
        raise Exception("Invalid Amount :(")

def withdraw(amount):
    global Balance
    if amount > 0:
        if amount < Balance:
            Balance=Balance-amount
            print(f"Amount withdrawed {amount} , Total Balance : {Balance}")
        else:
            raise Exception("Insufficient Balance :(")
    else:
        raise ValueError("Negative Amount :(")
if __name__ == "__main__":
    deposit(100)
    try:
        withdraw(-1)
    except ValueError as e:
        print("Value Error : ",e)
