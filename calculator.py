first_number = input("Enter the first number: ")
operation = input("Enter the operation (+, -, *, /): ")
second_number = input("Enter the second number: ")


def calculate(first_number, operation, second_number):
    try:

        first_number = float(first_number)
        second_number = float(second_number)

        if operation == '+':
            return first_number + second_number
        elif operation == '-':
            return first_number - second_number
        elif operation == '*':
            return first_number * second_number
        elif operation == '/':
            if second_number == 0:
                return "Error: Division by zero is not allowed."
            return first_number / second_number
        else:
            return "Error: Invalid operation. Please use +, -, *, or /."
    except ValueError:
        return "Error: Invalid input. Please enter numeric values."
    
result = calculate(first_number, operation, second_number)
print("Result:", result)