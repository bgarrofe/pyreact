"""
Example components to demonstrate PyReact transpiler functionality.

This file contains sample React-like components written in Python
that can be transpiled to JavaScript using the PyReact transpiler.
"""

from pyreact import Component, div, h1, h2, button, p, span, input_field, PyReactTranspiler


class Counter(Component):
    """A simple counter component that demonstrates state management and event handling."""
    
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {'count': 0}
    
    def increment(self):
        self.set_state({'count': self.state['count'] + 1})
    
    def decrement(self):
        self.set_state({'count': self.state['count'] - 1})
    
    def reset(self):
        self.set_state({'count': 0})
    
    def render(self):
        return div(
            h1(f"Count: {self.state['count']}"),
            div(
                button("Increment", onclick=self.increment),
                button("Decrement", onclick=self.decrement),
                button("Reset", onclick=self.reset)
            )
        )


class Greeting(Component):
    """A greeting component that demonstrates props usage."""
    
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {'name': 'World'}
    
    def update_name(self):
        # In a real implementation, this would get input from a text field
        self.set_state({'name': 'PyReact User'})
    
    def render(self):
        name = self.props.get('name', self.state['name'])
        return div(
            h2(f"Hello, {name}!"),
            p("This is a greeting component built with PyReact."),
            button("Change Name", onclick=self.update_name)
        )


class ClickTracker(Component):
    """A component that tracks button clicks and demonstrates multiple state properties."""
    
    def __init__(self, props=None):
        super().__init__(props)
        self.state = {
            'clicks': 0,
            'last_clicked': 'Never',
            'total_time': 0
        }
    
    def handle_click(self):
        self.set_state({
            'clicks': self.state['clicks'] + 1,
            'last_clicked': 'Just now'
        })
    
    def clear_stats(self):
        self.set_state({
            'clicks': 0,
            'last_clicked': 'Never',
            'total_time': 0
        })
    
    def render(self):
        return div(
            h2("Click Tracker"),
            p(f"Total clicks: {self.state['clicks']}"),
            p(f"Last clicked: {self.state['last_clicked']}"),
            div(
                button("Click Me!", onclick=self.handle_click),
                button("Clear Stats", onclick=self.clear_stats)
            )
        )


def main():
    """Main function to demonstrate the transpiler."""
    print("PyReact Example - Transpiling Python Components to JavaScript")
    print("=" * 60)
    
    # Create transpiler instance
    transpiler = PyReactTranspiler()
    
    # Transpile each component
    print("\n1. Transpiling Counter component...")
    counter_js = transpiler.transpile_component(Counter)
    print("✓ Counter component transpiled successfully")
    
    print("\n2. Transpiling Greeting component...")
    greeting_js = transpiler.transpile_component(Greeting)
    print("✓ Greeting component transpiled successfully")
    
    print("\n3. Transpiling ClickTracker component...")
    tracker_js = transpiler.transpile_component(ClickTracker)
    print("✓ ClickTracker component transpiled successfully")
    
    # Display transpiled JavaScript for Counter
    print("\n" + "=" * 60)
    print("TRANSPILED JAVASCRIPT - Counter Component:")
    print("=" * 60)
    print(counter_js)
    
    # Generate complete JavaScript
    print("\n" + "=" * 60)
    print("COMPLETE JAVASCRIPT OUTPUT:")
    print("=" * 60)
    complete_js = transpiler.generate_complete_js()
    print(complete_js)
    
    # Generate HTML demo page
    print("\n" + "=" * 60)
    print("GENERATING HTML DEMO PAGE:")
    print("=" * 60)
    
    components_to_render = ['Counter', 'Greeting', 'ClickTracker']
    html_file = transpiler.save_html_demo(
        components=components_to_render,
        filename="pyreact_demo.html",
        title="PyReact Demo - Python to JavaScript React Components"
    )
    
    print(f"✓ HTML demo saved as: {html_file}")
    print("✓ Open pyreact_demo.html in your browser to see the working components!")
    
    # Display some stats
    print("\n" + "=" * 60)
    print("TRANSPILATION STATISTICS:")
    print("=" * 60)
    print(f"Components transpiled: {len(transpiler.components)}")
    print(f"Total JavaScript lines: {len(complete_js.splitlines())}")
    print(f"Component names: {', '.join(transpiler.components.keys())}")
    
    return transpiler


if __name__ == "__main__":
    # Run the example
    result = main()
    
    print("\n" + "=" * 60)
    print("EXAMPLE COMPLETE!")
    print("=" * 60)
    print("The PyReact transpiler has successfully converted Python components to JavaScript!")
    print("Check the generated 'pyreact_demo.html' file to see your components in action.")