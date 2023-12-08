import random

def generate_random_python_code(num_lines):
    """
    Generate random Python code with a given number of lines.
    The code is generated based on basic Python syntax and includes control structures.
    """
    def random_statement(indent_level):
        """
        Generate a random Python statement, including control structures.
        """
        statements = [
            "pass",
            "if condition:\n",
            "for _ in range(n):\n",
            "while condition:\n",
        ]
        return "    " * indent_level + random.choice(statements)

    indent_level = 0
    code = ""

    for _ in range(num_lines):
        # Randomly decide whether to increase, decrease, or maintain the indentation
        change_indent = random.choice(["increase", "decrease", "maintain"])
        if change_indent == "increase":
            indent_level += 1
        elif change_indent == "decrease" and indent_level > 0:
            indent_level -= 1

        # Create a line of code with the current indentation
        line = random_statement(indent_level)
        code += line

        # Adjust indentation for block structures
        if line.strip().endswith(':'):
            indent_level += 1

    return code

# Generate and save a random Python program
num_lines = random.randint(10, 300)  # Random number of lines between 10 and 30
random_code = generate_random_python_code(num_lines)

# Display the generated code
print(random_code)
