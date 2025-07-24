# Penguin Lint

Penguin Lint is a Python script that uses Abstract Syntax Trees (AST) to analyze and refactor Python code. It provides a simple framework for programmatically applying custom transformations to Python source code.
> created to undestand how ast works 

## Features

- **Remove Print Statements**: Automatically removes `print()` calls from your code.
- **Improve Formatting**: Inserts newlines to enforce a consistent style, such as adding blank lines before function and class definitions and breaking up long blocks of constant assignments.

## How It Works

The script leverages Python's built-in `ast` module to parse source code into a tree structure. It then traverses this tree and modifies it using custom `ast.NodeTransformer` classes:

- `PrintVisitor`: This transformer identifies and removes expressions that are `print()` calls.
- `NewlineInserter`: This transformer adds blank lines to improve code readability. It inserts newlines before function and class definitions and after every four consecutive constant assignments.

After applying these transformations, the script unparses the modified AST back into source code.

## Usage

To use the script, simply run `main.py`:

```bash
python main.py
```

The script contains a hardcoded example Python script. It will apply the transformations and print the refactored code to the console.

### Example

**Original Code:**

```python
import requests

def fetch_data(url):
    response = requests.get(url)
    print("Data fetched successfully!")
    return response.json()
def main():
    data = fetch_data("https://api.example.com/data")
    print(data)
    return data

def hello():
    print("Hello from main.py!")
    pass
def goodbye():
    print("Goodbye from main.py!")
    pass
lx = 10
ly = 20
py = 30
px = 40
zt = 50
ci = 60
ko = 70
```

**Expected Refactored Code:**

```python
import requests

def fetch_data(url):
    response = requests.get(url)
    return response.json()

def main():
    data = fetch_data('https://api.example.com/data')
    return data

def hello():
    pass

def goodbye():
    pass
lx = 10
ly = 20
py = 30
px = 40

zt = 50
ci = 60
ko = 70
```

