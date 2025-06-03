# PyReact - Python to JavaScript React Transpiler

A powerful transpiler that converts Python classes into React components, enabling developers to write React applications using Python syntax.

## 🚀 Features

- **Component Classes**: Write React components as Python classes
- **State Management**: Automatic conversion of `self.state` to React `useState` hooks
- **Event Handling**: Convert Python methods to JavaScript event handlers
- **JSX-like Syntax**: Use helper functions like `div()`, `h1()`, `button()` for elements
- **F-string Support**: Python f-strings become JavaScript template literals
- **HTML Generation**: Complete HTML pages with working React components

## 📦 Installation

No external dependencies required! PyReact uses only Python standard library modules.

```bash
git clone <repository-url>
cd pyreact
```

## 🎯 Quick Start

### 1. Create a Python Component

```python
from pyreact import Component, div, h1, button

class Counter(Component):
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {'count': 0}
    
    def increment(self):
        self.set_state({'count': self.state['count'] + 1})
    
    def render(self):
        return div(
            h1(f"Count: {self.state['count']}"),
            button("Increment", onclick=self.increment)
        )
```

### 2. Transpile to JavaScript

```python
from pyreact import PyReactTranspiler

transpiler = PyReactTranspiler()
js_code = transpiler.transpile_component(Counter)
print(js_code)
```

### 3. Generate Working HTML Demo

```python
# Generate a complete HTML page
html_file = transpiler.save_html_demo(
    components=['Counter'],
    filename="demo.html",
    title="My PyReact App"
)
```

## 📚 Component Examples

### Counter Component
```python
class Counter(Component):
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {'count': 0}
    
    def increment(self):
        self.set_state({'count': self.state['count'] + 1})
    
    def decrement(self):
        self.set_state({'count': self.state['count'] - 1})
    
    def render(self):
        return div(
            h1(f"Count: {self.state['count']}"),
            button("Increment", onclick=self.increment),
            button("Decrement", onclick=self.decrement)
        )
```

### Greeting Component
```python
class Greeting(Component):
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {'name': 'World'}
    
    def render(self):
        name = self.props.get('name', self.state['name'])
        return div(
            h2(f"Hello, {name}!"),
            p("Welcome to PyReact!")
        )
```

## 🏗️ Available HTML Elements

PyReact provides helper functions for common HTML elements:

- **Text Elements**: `h1()`, `h2()`, `h3()`, `p()`, `span()`
- **Layout**: `div()`, `section()`, `header()`, `footer()`
- **Interactive**: `button()`, `input_field()`, `textarea()`, `select()`
- **Lists**: `ul()`, `ol()`, `li()`
- **Forms**: `form()`, `label()`, `option()`
- **Media**: `img()`, `a()`
- **Utility**: `br()`, `hr()`

## 🔄 Generated JavaScript Output

PyReact converts your Python components to modern React function components:

```python
# Python
class Counter(Component):
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {'count': 0}
    
    def increment(self):
        self.set_state({'count': self.state['count'] + 1})
    
    def render(self):
        return div(h1(f"Count: {self.state['count']}"))
```

```javascript
// Generated JavaScript
function Counter(props) {
  const [state, setState] = React.useState({count: 0});

  const increment = () => {
    setState(prevState => ({...prevState, count: prevState.count + 1}));
  };

  return React.createElement('div', null, [
    React.createElement('h1', null, [`Count: ${state.count}`])
  ]);
}
```

## 🧪 Running the Example

```bash
python3 example.py
```

This will:
1. Transpile three example components (Counter, Greeting, ClickTracker)
2. Generate JavaScript code
3. Create a complete HTML demo page (`pyreact_demo.html`)
4. Open the HTML file in your browser to see working React components!

## 🎛️ API Reference

### PyReactTranspiler

Main transpiler class:

```python
transpiler = PyReactTranspiler()

# Transpile a single component
js_code = transpiler.transpile_component(MyComponent)

# Get all transpiled JavaScript
complete_js = transpiler.generate_complete_js()

# Generate HTML demo page
html_content = transpiler.generate_html_page(['Component1', 'Component2'])

# Save HTML demo to file
filename = transpiler.save_html_demo(['MyComponent'], 'demo.html')
```

### Component Base Class

```python
class MyComponent(Component):
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {}  # Initial state
    
    def set_state(self, new_state):
        # Updates component state (triggers re-render in React)
        pass
    
    def render(self):
        # Must return an Element (created with helper functions)
        return div("Hello World")
```

## ✨ Supported Features

- ✅ **Component Classes** with inheritance
- ✅ **State Management** (`self.state`, `self.set_state`)
- ✅ **Event Handlers** (`onclick`, `onchange`, etc.)
- ✅ **Props** access via `self.props`
- ✅ **F-strings** → Template literals
- ✅ **Method Calls** between components
- ✅ **Nested Elements** and composition
- ✅ **HTML Generation** with React integration

## 🔮 Future Enhancements

- Context API support
- Lifecycle methods (componentDidMount, etc.)
- Custom hooks equivalent
- Component composition patterns
- TypeScript output option
- Bundle optimization
- Source maps
- Error boundaries

## 📄 License

MIT License - feel free to use in your projects!

## 🤝 Contributing

Contributions welcome! This is a proof-of-concept that demonstrates Python-to-JavaScript transpilation for React-like components.

---

**PyReact** - Write React in Python! 🐍 ⚛️