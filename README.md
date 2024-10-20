# Flask Rule Engine Project

## Overview

This project implements a flexible rule engine using Flask, allowing users to create, combine, and evaluate complex rules against provided data. The system uses a custom Abstract Syntax Tree (AST) to represent and process rules efficiently.

## Features

- Create and store rules with a user-friendly syntax
- Combine multiple rules into more complex rule sets
- Evaluate rules against provided data
- RESTful API for rule management and evaluation
- Web interface for easy interaction with the rule engine

## Project Structure

```
flask-rule-engine/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── rule_engine.py
│   └── templates/
│       └── index.html
│
├── config.py
├── run.py
└── README.md
└── requirement.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flask-rule-engine.git
   cd flask-rule-engine
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```
   python run.py
   ```

The application will be available at `http://localhost:5000`.

## Usage

### API Endpoints

- `GET /api/rules`: Retrieve all rules
- `POST /api/rules`: Create a new rule
- `POST /api/rules/evaluate`: Evaluate a rule against provided data
- `POST /api/rules/combine/preview`: Preview combined rules
- `DELETE /api/rules/<rule_id>`: Delete a specific rule
- `POST /api/rules/combine`: Combine multiple rules into a new rule

### Creating Rules

Rules are created using a simple syntax. For example:

```
(age > 18 AND income >= 50000) OR (credit_score > 700)
```

### Combining Rules

Multiple rules can be combined to create more complex rule sets. The system automatically joins rules using the AND operator.

### Evaluating Rules

Rules are evaluated against provided data. The data should be in JSON format, containing the fields referenced in the rule.

## Rule Engine

The `RuleEngine` class in `rule_engine.py` handles the core functionality:

- Parsing rule strings into AST nodes
- Combining multiple rules
- Evaluating rules against provided data
- Converting AST back to rule strings

## Database

The project uses SQLAlchemy with SQLite to store rules. Each rule is stored with its name, rule string, and AST representation.

## Web Interface

A basic web interface is provided at the root URL ('/'), allowing users to interact with the rule engine through a user-friendly interface.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
