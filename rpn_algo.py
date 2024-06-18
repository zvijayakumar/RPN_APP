def evaluate_rpn(expression):
    stack = []
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }
    
    for token in expression.split():
        print("token",token)
        if token in operators:
            y, x = stack.pop(), stack.pop()
            result = operators[token](x, y)
            stack.append(result)
        else:
            stack.append(float(token))
    
    return stack[0] if stack else None
# Sample RPN expressions
expressions = [
    "3 4 +",       # 3 + 4 = 7
    "10 2 /",      # 10 / 2 = 5
    "5 1 2 + 4 * + 3 -",  
    "10 6 9 3 + -11 * / * 17 + 5 +"
]

# Evaluate each expression
for expr in expressions:
    result = evaluate_rpn(expr)
    print(f"Expression: {expr}, Result: {result}")

#Start the app
# uvicorn main:app --reload
#docker-cmd
# docker-compose up --build