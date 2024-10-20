from typing import Dict, Union, List, Optional
import json

class Node:
    """AST node representation."""
    def __init__(self, type_: str, value: Optional[str] = None, 
                 left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.type = type_
        self.value = value
        self.left = left
        self.right = right
    
    def to_dict(self) -> dict:
        """Convert node to dictionary."""
        result = {"type": self.type}
        if self.value is not None:
            result["value"] = self.value
        if self.left:
            result["left"] = self.left.to_dict()
        if self.right:
            result["right"] = self.right.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'Node':
        """Create node from dictionary."""
        left = cls.from_dict(data["left"]) if "left" in data else None
        right = cls.from_dict(data["right"]) if "right" in data else None
        return cls(data["type"], data.get("value"), left, right)

class RuleEngine:
    """Rule engine implementation."""
    OPERATORS = {'AND', 'OR'}
    COMPARISONS = {'>', '<', '=', '>=', '<=', '!='}
    
    @staticmethod
    def create_rule(rule_string: str) -> Node:
        """Create AST from rule string."""
        def tokenize(s: str) -> List[str]:
            s = s.replace('(', ' ( ').replace(')', ' ) ')
            return [token.strip() for token in s.split() if token.strip()]
        
        def parse_expression(tokens: List[str]) -> Node:
            if not tokens:
                raise ValueError("Empty expression")
            
            stack = []
            operators = []
            
            i = 0
            while i < len(tokens):
                token = tokens[i]
                
                if token == '(':
                    operators.append(token)
                elif token == ')':
                    while operators and operators[-1] != '(':
                        right = stack.pop()
                        left = stack.pop()
                        op = operators.pop()
                        stack.append(Node("operator", op, left, right))
                    operators.pop()  # Remove '('
                elif token in RuleEngine.OPERATORS:
                    while (operators and operators[-1] != '(' and
                           operators[-1] in RuleEngine.OPERATORS):
                        right = stack.pop()
                        left = stack.pop()
                        op = operators.pop()
                        stack.append(Node("operator", op, left, right))
                    operators.append(token)
                else:
                    # Handle comparison expressions
                    if i + 2 < len(tokens):
                        field = token
                        comp_op = tokens[i + 1]
                        value = tokens[i + 2]
                        
                        if comp_op in RuleEngine.COMPARISONS:
                            condition = f"{field} {comp_op} {value}"
                            stack.append(Node("operand", condition))
                            i += 2
                    
                i += 1
            
            while operators:
                right = stack.pop()
                left = stack.pop()
                op = operators.pop()
                stack.append(Node("operator", op, left, right))
            
            return stack[0]
        
        tokens = tokenize(rule_string)
        return parse_expression(tokens)
    
    @staticmethod
    def combine_rules(rules: List[str]) -> Node:
        """Combine multiple rules into single AST."""
        if not rules:
            raise ValueError("No rules provided")
        
        rule_nodes = [RuleEngine.create_rule(rule) for rule in rules]
        
        # Combine rules with AND operator
        result = rule_nodes[0]
        for node in rule_nodes[1:]:
            result = Node("operator", "AND", result, node)
        
        return result
    
    @staticmethod
    def evaluate_rule(ast_json: Dict, data: Dict) -> bool:
        """Evaluate rule against provided data."""
        def evaluate_node(node: Dict) -> bool:
            if node["type"] == "operator":
                left = evaluate_node(node["left"])
                right = evaluate_node(node["right"])
                
                if node["value"] == "AND":
                    return left and right
                elif node["value"] == "OR":
                    return left or right
                
            elif node["type"] == "operand":
                condition = node["value"]
                field, op, value = [part.strip() for part in condition.split(' ', 2)]
                
                if field not in data:
                    raise ValueError(f"Field {field} not found in data")
                
                actual_value = data[field]
                expected_value = value.strip("'\"")  # Remove quotes if present
                
                try:
                    if expected_value.isdigit():
                        expected_value = int(expected_value)
                except ValueError:
                    pass
                
                if op == '>':
                    return actual_value > expected_value
                elif op == '<':
                    return actual_value < expected_value
                elif op == '=':
                    return actual_value == expected_value
                elif op == '>=':
                    return actual_value >= expected_value
                elif op == '<=':
                    return actual_value <= expected_value
                elif op == '!=':
                    return actual_value != expected_value
                
            return False
        
        return evaluate_node(ast_json)
    
    @staticmethod
    def ast_to_string(node: Node) -> str:
        """Convert AST back to rule string."""
        if node.type == "operator":
            left = RuleEngine.ast_to_string(node.left)
            right = RuleEngine.ast_to_string(node.right)
            return f"({left} {node.value} {right})"
        elif node.type == "operand":
            return node.value
        return ""
