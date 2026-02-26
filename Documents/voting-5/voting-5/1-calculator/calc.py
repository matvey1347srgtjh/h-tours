def add(a,b): return a + b
def substract(a,b): return a - b
def multiply(a,b): return a * b
def divide(a,b):
    if b == 0:
        raise ValueError("на ноль делить нельзя")
    return a / b

def main():
    print("--TOP калькулятор--")

    num1 = float(input("первое число: "))
    operation = input("действие (+, -, *, /): ")
    num2 = float(input("второе число: "))

    if operation == '+':
        result = num1 + num2

    elif operation == '-':
        result = num1 - num2

    elif operation == '*':
        result = num1 * num2

    elif operation == '/':

        if num2 == 0:
            print("на 0 делить нельзя")
    else:
        result = divide(num1, num2)
        # return "не верная операция"
    
    print(f"рузультат: {result}")

if __name__ == '__main__': main()
