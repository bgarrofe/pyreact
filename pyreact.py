"""
PyReact: A Python to JavaScript React Transpiler

This module provides a transpiler that converts Python classes into React components,
enabling developers to write React applications using Python syntax.
"""

import ast
import inspect
import re
from typing import Dict, List, Any, Optional


class Component:
    """
    Base class for PyReact components, similar to React.Component.
    
    This class provides the foundation for creating React-like components in Python
    that can be transpiled to JavaScript.
    """
    
    def __init__(self, props=None):
        """
        Initialize the component with optional props.
        
        Args:
            props (dict, optional): Properties passed to the component
        """
        self.props = props or {}
        self.state = {}
        self.children = []
        self.element = None
    
    def set_state(self, new_state):
        """
        Update component state, similar to React's setState.
        
        Args:
            new_state (dict): State updates to apply
        """
        if isinstance(new_state, dict):
            self.state.update(new_state)
        else:
            self.state = new_state
        # In a real implementation, this would trigger re-rendering
        self._trigger_update()
    
    def _trigger_update(self):
        """
        Internal method to handle state updates.
        In the transpiled JavaScript, this becomes a setState call.
        """
        pass
    
    def render(self):
        """
        Render method that must be implemented by subclasses.
        This method should return the component's virtual DOM structure.
        
        Returns:
            Element: The rendered virtual DOM tree
        """
        raise NotImplementedError("Components must implement the render method")
    
    def component_did_mount(self):
        """
        Lifecycle method called after component mounts.
        Transpiles to React's componentDidMount or useEffect.
        """
        pass
    
    def component_will_unmount(self):
        """
        Lifecycle method called before component unmounts.
        Transpiles to React's componentWillUnmount or useEffect cleanup.
        """
        pass
    
    def should_component_update(self, new_props, new_state):
        """
        Lifecycle method to control re-rendering.
        
        Args:
            new_props (dict): New props
            new_state (dict): New state
            
        Returns:
            bool: Whether component should update
        """
        return True


class Element:
    """
    Represents a virtual DOM element, similar to React elements.
    
    This class encapsulates HTML elements with their properties and children,
    providing a Python-based representation that can be transpiled to React.createElement calls.
    """
    
    def __init__(self, tag, props=None, children=None):
        """
        Initialize a virtual DOM element.
        
        Args:
            tag (str): HTML tag name (e.g., 'div', 'h1', 'button')
            props (dict, optional): Element properties/attributes
            children (list, optional): Child elements or text content
        """
        self.tag = tag
        self.props = props or {}
        self.children = children or []
        
        # Ensure children is always a list
        if not isinstance(self.children, list):
            self.children = [self.children]
    
    def __repr__(self):
        """String representation for debugging."""
        return f"Element(tag='{self.tag}', props={self.props}, children={len(self.children)})"


# Helper functions for creating common HTML elements
# These provide JSX-like syntax in Python

def div(*children, **props):
    """Create a div element."""
    return Element('div', props, list(children))

def h1(content=None, *children, **props):
    """Create an h1 element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('h1', props, all_children)

def h2(content=None, *children, **props):
    """Create an h2 element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('h2', props, all_children)

def h3(content=None, *children, **props):
    """Create an h3 element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('h3', props, all_children)

def p(content=None, *children, **props):
    """Create a p (paragraph) element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('p', props, all_children)

def span(content=None, *children, **props):
    """Create a span element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('span', props, all_children)

def button(content=None, *children, **props):
    """Create a button element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('button', props, all_children)

def input_field(**props):
    """Create an input element."""
    return Element('input', props, [])

def img(**props):
    """Create an img element."""
    return Element('img', props, [])

def a(content=None, *children, **props):
    """Create an anchor (a) element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('a', props, all_children)

def ul(*children, **props):
    """Create an unordered list (ul) element."""
    return Element('ul', props, list(children))

def ol(*children, **props):
    """Create an ordered list (ol) element."""
    return Element('ol', props, list(children))

def li(content=None, *children, **props):
    """Create a list item (li) element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('li', props, all_children)

def form(*children, **props):
    """Create a form element."""
    return Element('form', props, list(children))

def label(content=None, *children, **props):
    """Create a label element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('label', props, all_children)

def select(*children, **props):
    """Create a select element."""
    return Element('select', props, list(children))

def option(content=None, *children, **props):
    """Create an option element."""
    all_children = [content] if content is not None else []
    all_children.extend(children)
    return Element('option', props, all_children)

def textarea(content=None, **props):
    """Create a textarea element."""
    children = [content] if content is not None else []
    return Element('textarea', props, children)

def br(**props):
    """Create a br (line break) element."""
    return Element('br', props, [])

def hr(**props):
    """Create an hr (horizontal rule) element."""
    return Element('hr', props, [])


class PyReactTranspiler:
    """Main transpiler class that converts Python components to JavaScript React code."""
    
    def __init__(self):
        self.components = {}
        self.js_output = []
        
    def transpile_component(self, component_class) -> str:
        """
        Transpile a Python component class to JavaScript React code.
        
        Args:
            component_class: The Python class to transpile
            
        Returns:
            str: The generated JavaScript code
        """
        # Get the source code of the class
        source_code = inspect.getsource(component_class)
        
        # Parse the source code into an AST
        tree = ast.parse(source_code)
        
        # Find the class definition
        class_def = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == component_class.__name__:
                class_def = node
                break
        
        if not class_def:
            raise ValueError(f"Could not find class definition for {component_class.__name__}")
        
        # Extract component information
        component_info = self._analyze_component_class(class_def)
        
        # Generate JavaScript code
        js_code = self._generate_js_component(component_info)
        
        # Store the component for later use
        self.components[component_class.__name__] = js_code
        
        return js_code
    
    def _analyze_component_class(self, class_def):
        """
        Analyze a Python class AST node to extract component information.
        
        Args:
            class_def: AST ClassDef node
            
        Returns:
            dict: Component information including methods, state, etc.
        """
        component_info = {
            'name': class_def.name,
            'methods': {},
            'init_method': None,
            'render_method': None,
            'initial_state': {},
        }
        
        # Analyze each method in the class
        for node in class_def.body:
            if isinstance(node, ast.FunctionDef):
                method_info = self._analyze_method(node)
                component_info['methods'][node.name] = method_info
                
                # Special handling for specific methods
                if node.name == '__init__':
                    component_info['init_method'] = method_info
                    # Extract initial state from __init__
                    component_info['initial_state'] = self._extract_initial_state(node)
                elif node.name == 'render':
                    component_info['render_method'] = method_info
        
        return component_info
    
    def _analyze_method(self, method_node):
        """
        Analyze a Python method AST node.
        
        Args:
            method_node: AST FunctionDef node
            
        Returns:
            dict: Method information
        """
        return {
            'name': method_node.name,
            'args': [arg.arg for arg in method_node.args.args],
            'body': method_node.body,
            'ast_node': method_node
        }
    
    def _extract_initial_state(self, init_node):
        """
        Extract initial state from __init__ method.
        
        Args:
            init_node: AST FunctionDef node for __init__
            
        Returns:
            dict: Initial state values
        """
        initial_state = {}
        
        for stmt in init_node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if (isinstance(target, ast.Attribute) and 
                        isinstance(target.value, ast.Name) and 
                        target.value.id == 'self' and 
                        target.attr == 'state'):
                        # Found self.state assignment
                        if isinstance(stmt.value, ast.Dict):
                            # Extract dictionary literal
                            for key, value in zip(stmt.value.keys, stmt.value.values):
                                if isinstance(key, ast.Constant):
                                    if isinstance(value, ast.Constant):
                                        # Handle basic constants properly
                                        if isinstance(value.value, str):
                                            initial_state[key.value] = value.value
                                        else:
                                            initial_state[key.value] = value.value
                                    else:
                                        initial_state[key.value] = self._ast_to_js_value(value)
        
        return initial_state
    
    def _ast_to_js_value(self, node):
        """
        Convert AST node to JavaScript value representation.
        
        Args:
            node: AST node
            
        Returns:
            str: JavaScript representation
        """
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            else:
                return str(node.value).lower() if isinstance(node.value, bool) else str(node.value)
        elif isinstance(node, ast.List):
            elements = [self._ast_to_js_value(el) for el in node.elts]
            return f'[{", ".join(elements)}]'
        elif isinstance(node, ast.Dict):
            pairs = []
            for key, value in zip(node.keys, node.values):
                key_str = self._ast_to_js_value(key)
                value_str = self._ast_to_js_value(value)
                pairs.append(f'{key_str}: {value_str}')
            return f'{{{", ".join(pairs)}}}'
        else:
            return 'null'
    
    def _generate_js_component(self, component_info):
        """
        Generate JavaScript React component from component information.
        
        Args:
            component_info: Component analysis results
            
        Returns:
            str: JavaScript component code
        """
        component_name = component_info['name']
        initial_state = component_info['initial_state']
        
        # Start building the JavaScript function
        js_lines = []
        js_lines.append(f"function {component_name}(props) {{")
        
        # Add state hook if there's initial state
        if initial_state:
            state_obj = self._dict_to_js_object(initial_state)
            js_lines.append(f"  const [state, setState] = React.useState({state_obj});")
            js_lines.append("")
        
        # Add component methods (excluding __init__ and render)
        for method_name, method_info in component_info['methods'].items():
            if method_name not in ['__init__', 'render']:
                method_js = self._transpile_method_to_js(method_info)
                if method_js:
                    js_lines.append(f"  {method_js}")
                    js_lines.append("")
        
        # Add render method
        if component_info['render_method']:
            render_js = self._transpile_render_method(component_info['render_method'])
            js_lines.append(f"  return {render_js};")
        else:
            js_lines.append("  return null;")
        
        js_lines.append("}")
        
        return "\n".join(js_lines)
    
    def _dict_to_js_object(self, python_dict):
        """
        Convert Python dictionary to JavaScript object string.
        
        Args:
            python_dict: Python dictionary
            
        Returns:
            str: JavaScript object representation
        """
        if not python_dict:
            return "{}"
        
        pairs = []
        for key, value in python_dict.items():
            if isinstance(value, str):
                pairs.append(f'{key}: "{value}"')
            elif isinstance(value, bool):
                pairs.append(f'{key}: {str(value).lower()}')
            else:
                pairs.append(f'{key}: {value}')
        
        return "{" + ", ".join(pairs) + "}"
    
    def generate_complete_js(self) -> str:
        """
        Generate complete JavaScript code with all transpiled components.
        
        Returns:
            str: Complete JavaScript code ready for execution
        """
        if not self.components:
            return "// No components to transpile"
        
        js_parts = []
        js_parts.append("// PyReact - Transpiled Components")
        js_parts.append("")
        
        for component_name, component_code in self.components.items():
            js_parts.append(component_code)
            js_parts.append("")
        
        return "\n".join(js_parts)
    
    def _transpile_method_to_js(self, method_info):
        """
        Transpile a Python method to JavaScript function.
        
        Args:
            method_info: Method information from analysis
            
        Returns:
            str: JavaScript function code
        """
        method_name = method_info['name']
        method_body = method_info['body']
        
        # Skip lifecycle methods that don't need transpilation
        if method_name in ['component_did_mount', 'component_will_unmount', 'should_component_update']:
            return None
        
        js_lines = []
        js_lines.append(f"const {method_name} = () => {{")
        
        # Transpile method body
        for stmt in method_body:
            js_stmt = self._transpile_statement(stmt)
            if js_stmt:
                js_lines.append(f"    {js_stmt}")
        
        js_lines.append("  };")
        
        return "\n".join(js_lines)
    
    def _transpile_render_method(self, render_method_info):
        """
        Transpile the render method to JavaScript JSX-like code.
        
        Args:
            render_method_info: Render method information
            
        Returns:
            str: JavaScript render code
        """
        render_body = render_method_info['body']
        
        # Track local variables for proper transpilation
        self.local_variables = {}
        
        # Process all statements to handle local variables
        js_statements = []
        return_statement = None
        
        for stmt in render_body:
            if isinstance(stmt, ast.Return):
                return_statement = stmt
            elif isinstance(stmt, ast.Assign):
                # Handle local variable assignments
                js_assign = self._transpile_render_assignment(stmt)
                if js_assign:
                    js_statements.append(js_assign)
        
        # Generate the return statement
        if return_statement:
            if js_statements:
                # If we have local variables, wrap in an IIFE
                statements_str = '; '.join(js_statements)
                return_expr = self._transpile_element_expression(return_statement.value)
                return f"(() => {{ {statements_str}; return {return_expr}; }})()"
            else:
                return self._transpile_element_expression(return_statement.value)
        
        return "null"
    
    def _transpile_render_assignment(self, assign_node):
        """
        Transpile assignment statements in render method to track local variables.
        
        Args:
            assign_node: AST Assign node
            
        Returns:
            str: JavaScript assignment or None
        """
        if len(assign_node.targets) == 1:
            target = assign_node.targets[0]
            if isinstance(target, ast.Name):
                var_name = target.id
                
                # Transpile the assignment value
                value_js = self._transpile_expression(assign_node.value)
                
                # Track this local variable
                self.local_variables[var_name] = value_js
                
                return f"const {var_name} = {value_js}"
        
        return None
    
    def _transpile_statement(self, stmt):
        """
        Transpile a Python statement to JavaScript.
        
        Args:
            stmt: AST statement node
            
        Returns:
            str: JavaScript statement
        """
        if isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                return self._transpile_method_call(stmt.value)
        elif isinstance(stmt, ast.Assign):
            return self._transpile_assignment(stmt)
        elif isinstance(stmt, ast.Return):
            return f"return {self._transpile_expression(stmt.value)};"
        
        return ""
    
    def _transpile_method_call(self, call_node):
        """
        Transpile a method call, especially set_state calls.
        
        Args:
            call_node: AST Call node
            
        Returns:
            str: JavaScript method call
        """
        if (isinstance(call_node.func, ast.Attribute) and
            isinstance(call_node.func.value, ast.Name) and
            call_node.func.value.id == 'self' and
            call_node.func.attr == 'set_state'):
            
            # Convert self.set_state to setState
            if call_node.args:
                state_arg = self._transpile_expression(call_node.args[0])
                return f"setState(prevState => ({{...prevState, ...{state_arg}}}));"
        
        return ""
    
    def _transpile_assignment(self, assign_node):
        """
        Transpile assignment statements.
        
        Args:
            assign_node: AST Assign node
            
        Returns:
            str: JavaScript assignment
        """
        # For now, skip most assignments as they're handled differently in React
        return ""
    
    def _transpile_expression(self, expr):
        """
        Transpile a Python expression to JavaScript.
        
        Args:
            expr: AST expression node
            
        Returns:
            str: JavaScript expression
        """
        if isinstance(expr, ast.Dict):
            return self._transpile_dict_literal(expr)
        elif isinstance(expr, ast.Constant):
            if isinstance(expr.value, str):
                return f'"{expr.value}"'
            else:
                return str(expr.value).lower() if isinstance(expr.value, bool) else str(expr.value)
        elif isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Attribute):
            return self._transpile_attribute_access(expr)
        elif isinstance(expr, ast.BinOp):
            return self._transpile_binary_operation(expr)
        elif isinstance(expr, ast.JoinedStr):
            return self._transpile_f_string(expr)
        elif isinstance(expr, ast.Call):
            return self._transpile_function_call(expr)
        elif isinstance(expr, ast.Subscript):
            return self._transpile_subscript(expr)
        else:
            return "null"
    
    def _transpile_element_expression(self, expr):
        """
        Transpile element expressions (like div(), h1(), etc.) to React.createElement.
        
        Args:
            expr: AST expression node
            
        Returns:
            str: React.createElement call
        """
        if isinstance(expr, ast.Call):
            return self._transpile_element_call(expr)
        else:
            return self._transpile_expression(expr)
    
    def _transpile_element_call(self, call_node):
        """
        Transpile element function calls to React.createElement.
        
        Args:
            call_node: AST Call node
            
        Returns:
            str: React.createElement call
        """
        if isinstance(call_node.func, ast.Name):
            element_name = call_node.func.id
            
            # Handle common HTML elements
            html_elements = ['div', 'h1', 'h2', 'h3', 'p', 'span', 'button', 'input_field', 'a', 'ul', 'ol', 'li', 'form', 'label', 'select', 'option', 'textarea', 'br', 'hr', 'img']
            
            if element_name in html_elements:
                # Convert input_field to input
                tag_name = 'input' if element_name == 'input_field' else element_name
                
                # Extract props and children
                props = {}
                children = []
                
                # Process arguments and keyword arguments
                for arg in call_node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        children.append(f'"{arg.value}"')
                    else:
                        children.append(self._transpile_element_expression(arg))
                
                # Process keyword arguments as props
                for keyword in call_node.keywords:
                    prop_name = keyword.arg
                    prop_value = self._transpile_prop_value(keyword.value)
                    
                    # Convert onclick to onClick, etc.
                    if prop_name == 'onclick':
                        prop_name = 'onClick'
                    elif prop_name == 'onchange':
                        prop_name = 'onChange'
                    elif prop_name == 'onsubmit':
                        prop_name = 'onSubmit'
                    
                    props[prop_name] = prop_value
                
                # Build React.createElement call
                props_str = self._build_props_object(props) if props else "null"
                
                if children:
                    children_str = f"[{', '.join(children)}]"
                    return f"React.createElement('{tag_name}', {props_str}, {children_str})"
                else:
                    return f"React.createElement('{tag_name}', {props_str})"
        
        return "null"
    
    def _transpile_prop_value(self, value_node):
        """
        Transpile prop values, handling event handlers specially.
        
        Args:
            value_node: AST node representing the prop value
            
        Returns:
            str: JavaScript prop value
        """
        if isinstance(value_node, ast.Attribute):
            if (isinstance(value_node.value, ast.Name) and 
                value_node.value.id == 'self'):
                # This is a method reference like self.increment
                return value_node.attr
        
        return self._transpile_expression(value_node)
    
    def _build_props_object(self, props_dict):
        """
        Build JavaScript props object from dictionary.
        
        Args:
            props_dict: Dictionary of prop names to values
            
        Returns:
            str: JavaScript object
        """
        if not props_dict:
            return "null"
        
        prop_pairs = []
        for key, value in props_dict.items():
            prop_pairs.append(f"{key}: {value}")
        
        return "{" + ", ".join(prop_pairs) + "}"
    
    def _transpile_dict_literal(self, dict_node):
        """
        Transpile Python dictionary literal to JavaScript object.
        
        Args:
            dict_node: AST Dict node
            
        Returns:
            str: JavaScript object literal
        """
        pairs = []
        for key, value in zip(dict_node.keys, dict_node.values):
            key_str = self._transpile_expression(key)
            value_str = self._transpile_expression(value)
            pairs.append(f"{key_str}: {value_str}")
        
        return "{" + ", ".join(pairs) + "}"
    
    def _transpile_attribute_access(self, attr_node):
        """
        Transpile attribute access like self.state['count'].
        
        Args:
            attr_node: AST Attribute node
            
        Returns:
            str: JavaScript property access
        """
        if (isinstance(attr_node.value, ast.Name) and 
            attr_node.value.id == 'self' and 
            attr_node.attr == 'state'):
            return "state"
        
        return f"{self._transpile_expression(attr_node.value)}.{attr_node.attr}"
    
    def _transpile_binary_operation(self, binop_node):
        """
        Transpile binary operations like addition, subscript access.
        
        Args:
            binop_node: AST BinOp node
            
        Returns:
            str: JavaScript binary operation
        """
        left = self._transpile_expression(binop_node.left)
        right = self._transpile_expression(binop_node.right)
        
        # Handle state access in binary operations
        if (isinstance(binop_node.left, ast.Subscript) and
            isinstance(binop_node.left.value, ast.Attribute) and
            isinstance(binop_node.left.value.value, ast.Name) and
            binop_node.left.value.value.id == 'self' and
            binop_node.left.value.attr == 'state'):
            left = self._transpile_subscript(binop_node.left)
        
        if isinstance(binop_node.op, ast.Add):
            return f"{left} + {right}"
        elif isinstance(binop_node.op, ast.Sub):
            return f"{left} - {right}"
        elif isinstance(binop_node.op, ast.Mult):
            return f"{left} * {right}"
        elif isinstance(binop_node.op, ast.Div):
            return f"{left} / {right}"
        else:
            return f"{left} {right}"
    
    def _transpile_f_string(self, joinedstr_node):
        """
        Transpile Python f-strings to JavaScript template literals.
        
        Args:
            joinedstr_node: AST JoinedStr node
            
        Returns:
            str: JavaScript template literal
        """
        parts = []
        for value in joinedstr_node.values:
            if isinstance(value, ast.Constant):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                # Check if this is a simple variable name that might be local
                if isinstance(value.value, ast.Name):
                    var_name = value.value.id
                    # Check if it's a tracked local variable
                    if hasattr(self, 'local_variables') and var_name in self.local_variables:
                        parts.append(f"${{{var_name}}}")
                    else:
                        expr_js = self._transpile_expression(value.value)
                        parts.append(f"${{{expr_js}}}")
                else:
                    expr_js = self._transpile_expression(value.value)
                    # Handle subscript access for state
                    if isinstance(value.value, ast.Subscript):
                        expr_js = self._transpile_subscript(value.value)
                    parts.append(f"${{{expr_js}}}")
        
        return "`" + "".join(parts) + "`"
    
    def _transpile_subscript(self, subscript_node):
        """
        Transpile subscript access like self.state['count'].
        
        Args:
            subscript_node: AST Subscript node
            
        Returns:
            str: JavaScript property access
        """
        if (isinstance(subscript_node.value, ast.Attribute) and
            isinstance(subscript_node.value.value, ast.Name) and
            subscript_node.value.value.id == 'self' and
            subscript_node.value.attr == 'state'):
            
            if isinstance(subscript_node.slice, ast.Constant):
                key = subscript_node.slice.value
                return f"state.{key}"
        
        return "null"
    
    def _transpile_function_call(self, call_node):
        """
        Transpile function calls.
        
        Args:
            call_node: AST Call node
            
        Returns:
            str: JavaScript function call
        """
        if isinstance(call_node.func, ast.Name):
            func_name = call_node.func.id
            args = [self._transpile_expression(arg) for arg in call_node.args]
            return f"{func_name}({', '.join(args)})"
        elif isinstance(call_node.func, ast.Attribute):
            # Handle method calls like self.props.get()
            obj_js = self._transpile_expression(call_node.func.value)
            method_name = call_node.func.attr
            args = [self._transpile_expression(arg) for arg in call_node.args]
            
            # Special handling for self.props.get() - use logical OR for fallback
            if (isinstance(call_node.func.value, ast.Attribute) and
                isinstance(call_node.func.value.value, ast.Name) and
                call_node.func.value.value.id == 'self' and
                call_node.func.value.attr == 'props' and
                method_name == 'get' and len(args) == 2):
                # Convert self.props.get('key', default) to (props.key || default)
                key_arg = args[0].strip('"\'')  # Remove quotes from string literal
                default_arg = args[1]
                return f"(props.{key_arg} || {default_arg})"
            
            return f"{obj_js}.{method_name}({', '.join(args)})"
        
        return "null"
    
    def generate_html_page(self, components: List[str], title: str = "PyReact App") -> str:
        """
        Generate a complete HTML page with React and transpiled components.
        
        Args:
            components: List of component names to render
            title: Page title
            
        Returns:
            str: Complete HTML page
        """
        # Generate the complete JavaScript code
        js_code = self.generate_complete_js()
        
        # Create the render calls for each component
        render_calls = []
        for component_name in components:
            render_calls.append(f"    ReactDOM.render(React.createElement({component_name}), document.getElementById('{component_name.lower()}-root'));")
        
        # Create container divs for each component
        container_divs = []
        for component_name in components:
            container_divs.append(f'    <div id="{component_name.lower()}-root"></div>')
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://unpkg.com/react@17/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .component-container {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        button {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }}
        
        button:hover {{
            background-color: #0056b3;
        }}
        
        h1, h2, h3 {{
            color: #333;
        }}
        
        .counter {{
            text-align: center;
            padding: 20px;
        }}
        
        .counter h1 {{
            font-size: 2em;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Components generated by PyReact - Python to JavaScript React Transpiler</p>
    
{"".join(container_divs)}

    <script>
{js_code}

    // Render components
{chr(10).join(render_calls)}
    </script>
</body>
</html>"""
        
        return html_template
    
    def save_html_demo(self, components: List[str], filename: str = "pyreact_demo.html", title: str = "PyReact Demo") -> str:
        """
        Generate and save an HTML demo page.
        
        Args:
            components: List of component names to render
            filename: Output filename
            title: Page title
            
        Returns:
            str: Path to saved HTML file
        """
        html_content = self.generate_html_page(components, title)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename


if __name__ == "__main__":
    print("PyReact Transpiler - Python to JavaScript React Converter")
    print("This module provides tools to convert Python classes to React components.")