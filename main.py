import ast
from platform import node

code = """
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
    def __init__(self):
        super().__init__()
        self.previous_end_line = None

    def visit_Module(self, node):
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def visit_FunctionDef(self, node):
        node = self.add_newline_if_needed(node)
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def visit_ClassDef(self, node):
        node = self.add_newline_if_needed(node)
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def visit_For(self, node):
        node = self.add_newline_if_needed(node)
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def visit_While(self, node):
        node = self.add_newline_if_needed(node)
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def visit_AsyncFunctionDef(self, node):
        node = self.add_newline_if_needed(node)
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def visit_AsyncFor(self, node):
        node = self.add_newline_if_needed(node)
        self.previous_end_line = None
        node.body = self.process_block(node.body)
        return node

    def add_newline_if_needed(self, node):
        if self.previous_end_line is not None and node.lineno - self.previous_end_line < 2:
            # Create a marker node that will become an empty line
            marker = ast.Expr(value=ast.Constant(value=""))
            ast.copy_location(marker, node)
            return [marker, node]
        return node

    def process_block(self, body):
        new_body = []
        self.previous_end_line = None
        constant_count = 0

        for i, stmt in enumerate(body):
            # Handle adding newline before certain structures
            if isinstance(stmt, (ast.FunctionDef, ast.ClassDef, ast.For, 
                               ast.While, ast.AsyncFunctionDef, ast.AsyncFor)):
                if self.previous_end_line is not None and stmt.lineno - self.previous_end_line < 2:
                    marker = ast.Expr(value=ast.Constant(value=" "))
                    ast.copy_location(marker, stmt)
                    new_body.append(marker)
                    self.previous_end_line = stmt.lineno - 1  # Adjust for new line
                new_body.append(stmt)
                if hasattr(stmt, 'end_lineno'):
                    self.previous_end_line = stmt.end_lineno
                else:
                    self.previous_end_line = stmt.lineno
                constant_count = 0
                continue

            # Count constant expressions (assignments and expressions)
            if isinstance(stmt, (ast.Assign, ast.Expr, ast.AnnAssign)):
                constant_count += 1
            else:
                constant_count = 0

            # Add newline after every 4 constant expressions
            if constant_count == 4:
                marker = ast.Expr(value=ast.Constant(value=" "))
                ast.copy_location(marker, stmt)
                new_body.append(marker)
                constant_count = 0
                self.previous_end_line = stmt.lineno  # Reset line tracking

            new_body.append(stmt)
            
            # Update line tracking
            if hasattr(stmt, 'end_lineno'):
                self.previous_end_line = stmt.end_lineno
            else:
                self.previous_end_line = stmt.lineno

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
    
    print("Modified code:")
    print(new_code)


if __name__ == "__main__":
    main()
