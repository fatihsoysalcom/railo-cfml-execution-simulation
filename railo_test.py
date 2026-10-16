import io
import sys

# Simulate a basic CFML execution environment
class MockCFMLEngine:
    def __init__(self):
        self.variables = {}
        self.output = io.StringIO()

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        return self.variables.get(name, None)

    def write(self, text):
        self.output.write(str(text))

    def get_output(self):
        return self.output.getvalue()

    def reset(self):
        self.variables = {}
        self.output = io.StringIO()

# Simulate CFML tags and their execution
def cf_set(engine, name, value):
    engine.set(name, value)

def cf_output(engine, text):
    engine.write(text)

def cf_dump(engine, var):
    engine.write(f"<cfdump var=\" {var} \">\n{engine.get(var)}\n</cfdump>\n")

def cf_if(engine, condition, true_block, false_block=None):
    # Basic truthiness check for simulation
    if condition:
        true_block(engine)
    elif false_block:
        false_block(engine)

def cf_loop(engine, source, item, loop_body):
    if isinstance(source, list):
        for element in source:
            engine.set(item, element)
            loop_body(engine)
    elif isinstance(source, dict):
        for key, value in source.items():
            engine.set(key, key) # Simulate setting key as item
            engine.set(item, value) # Simulate setting value as item
            loop_body(engine)

# --- Test Scenarios (Simulating different repository behaviors) ---

def scenario_simple_variable(engine):
    print("--- Scenario: Simple Variable ---")
    cf_set(engine, "myVar", "Hello Railo!")
    cf_output(engine, "Value of myVar: ")
    cf_output(engine, engine.get("myVar"))
    print(engine.get_output())
    engine.reset()

def scenario_conditional_logic(engine):
    print("\n--- Scenario: Conditional Logic ---")
    cf_set(engine, "userStatus", "active")
    cf_if(engine, engine.get("userStatus") == "active",
            lambda eng: cf_output(eng, "User is online."),
            lambda eng: cf_output(eng, "User is offline."))
    print(engine.get_output())
    engine.reset()

def scenario_data_loop(engine):
    print("\n--- Scenario: Data Loop ---")
    users = [{"name": "Alice"}, {"name": "Bob"}]
    cf_loop(engine, users, "user", lambda eng: cf_output(eng, f"User: {eng.get('user')['name']}\n"))
    print(engine.get_output())
    engine.reset()

def scenario_complex_dump(engine):
    print("\n--- Scenario: Complex Dump ---")
    complex_data = {
        "config": {
            "timeout": 30,
            "retries": 3
        },
        "status": "running"
    }
    engine.set("complexData", complex_data)
    cf_dump(engine, "complexData")
    print(engine.get_output())
    engine.reset()

# --- Main Execution ---
if __name__ == "__main__":
    # This Python script simulates the behavior of a CFML engine like Railo
    # by providing mock functions for common CFML tags.
    # The 'scenarios' represent different ways CFML code might behave in
    # various public repositories (e.g., different logic, data structures).

    mock_engine = MockCFMLEngine()

    # Run the simulated test scenarios
    scenario_simple_variable(mock_engine)
    scenario_conditional_logic(mock_engine)
    scenario_data_loop(mock_engine)
    scenario_complex_dump(mock_engine)

    print("\nSimulation complete. These scenarios mimic how Railo might execute CFML code in different contexts.")
