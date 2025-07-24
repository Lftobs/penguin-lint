import ast
from platform import node

code = """
import requests

def fetch_data(url):
    response = requests.get(url)
    print("Data fetched successfully!")
    for i in range(5):
        x = x * i
    return response.json()
def main():
    data = fetch_data("https://api.example.com/data")
    while isinstance(data, list):
        data = data[0] if data else None
    if data is None:
        raise ValueError("No data found!")
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
"""

class PrintVisitor(ast.NodeTransformer):
    def visit_Expr(self, node):
        # Check if this expression is a print call
        if (isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Name) and \
           node.value.func.id == 'print'
        ):
            return None  # Remove the entire expression
        
        if isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Attribute) and \
           node.value.func.attr == 'print':
            return None 
        # Keep other expressions
        return node

class NewlineInserter(ast.NodeTransformer):
    def visit_Module(self, node):
        node.body = self.process_block(node.body)
        ast.fix_missing_locations(node)
        return node

    def process_block(self, body):
        new_body = []
        assign_count = 0
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.For, ast.While, ast.If, ast.Try, ast.With)):
                if new_body:  # Avoid blank line at the start
                    marker = ast.Expr(value=ast.Constant(value=None))
                    ast.copy_location(marker, stmt)
                    new_body.append(marker)
                assign_count = 0
                new_body.append(stmt)
                if hasattr(stmt, 'body'):
                    stmt.body = self.process_block(stmt.body)
                continue
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):  # Handle both Assign and AnnAssign
                assign_count += 1
            else:
                assign_count = 0
            new_body.append(stmt)
            if assign_count == 4:
                marker = ast.Expr(value=ast.Constant(value=None))
                ast.copy_location(marker, stmt)  # Preserve location info
                new_body.append(marker)
                assign_count = 0
        return new_body

def main():
    tree = ast.parse(code)
    
    # Use the transformer correctly
    transformer = PrintVisitor()
    modified_tree = transformer.visit(tree)  

    inserter = NewlineInserter()
    modified_tree = inserter.visit(modified_tree)
    
    # Unparse the modified TREE
    new_code = ast.unparse(modified_tree)
    
    lines = new_code.split('\n')
    processed_lines = ['' if line.strip() == 'None' else line for line in lines]
    final_code = '\n'.join(processed_lines)
    
    print("Modified code:")
    print(final_code)


if __name__ == "__main__":
    main()
