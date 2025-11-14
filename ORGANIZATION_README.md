# Organizational Structure Module

This module provides a comprehensive system for modeling organizational hierarchies with organizations, departments, and employees.

## Overview

The organizational structure module allows you to:
- Create and manage organizations
- Add departments to organizations
- Add employees to departments
- Query and retrieve organizational data
- Export organizational structure to JSON
- Display hierarchical structures

## Classes

### Organization

Top-level container representing a company or organization.

**Attributes:**
- `id` (str): Unique identifier
- `name` (str): Organization name
- `description` (str): Optional description
- `industry` (str): Optional industry classification
- `founded_date` (datetime): Optional founding date

**Key Methods:**
- `add_department(department)`: Add a department to the organization
- `remove_department(department)`: Remove a department
- `find_department(department_id)`: Find a department by ID
- `find_employee(employee_id)`: Find an employee across all departments
- `get_departments()`: Get all departments
- `get_total_employees()`: Get total employee count
- `get_all_employees()`: Get all employees across departments
- `to_dict()`: Export to dictionary
- `print_structure()`: Display hierarchical structure

### Department

Middle-level container representing a department within an organization.

**Attributes:**
- `id` (str): Unique identifier
- `name` (str): Department name
- `description` (str): Optional description
- `organization` (Organization): Parent organization (set automatically)
- `manager` (Employee): Optional department manager

**Key Methods:**
- `add_employee(employee)`: Add an employee to the department
- `remove_employee(employee)`: Remove an employee
- `find_employee(employee_id)`: Find an employee by ID
- `get_employees()`: Get all employees
- `get_employee_count()`: Get number of employees
- `to_dict()`: Export to dictionary

### Employee

Individual employee record.

**Attributes:**
- `id` (str): Unique identifier
- `name` (str): Employee name
- `email` (str): Email address (validated)
- `position` (str): Job position/title
- `department` (Department): Parent department (set automatically)
- `hire_date` (datetime): Optional hire date
- `phone` (str): Optional phone number

**Key Methods:**
- `to_dict()`: Export to dictionary

## Usage Examples

### Basic Structure

```python
from src.organization import Organization, Department, Employee
from datetime import datetime

# Create organization
org = Organization(
    id="ORG001",
    name="TechCorp",
    description="A technology company",
    industry="Software"
)

# Create department
engineering = Department(
    id="DEPT001",
    name="Engineering",
    description="Software development"
)

# Add department to organization
org.add_department(engineering)

# Create employees
cto = Employee(
    id="EMP001",
    name="Jane Doe",
    email="jane@techcorp.com",
    position="CTO",
    hire_date=datetime(2020, 1, 1)
)

engineer = Employee(
    id="EMP002",
    name="John Smith",
    email="john@techcorp.com",
    position="Senior Engineer"
)

# Add employees to department
engineering.add_employee(cto)
engineering.add_employee(engineer)

# Display structure
org.print_structure()
```

### Querying

```python
# Find department by ID
dept = org.find_department("DEPT001")

# Find employee by ID across all departments
employee = org.find_employee("EMP002")

# Get statistics
print(f"Total departments: {org.get_department_count()}")
print(f"Total employees: {org.get_total_employees()}")

# Get employees in a department
employees = dept.get_employees()
for emp in employees:
    print(f"{emp.name} - {emp.position}")
```

### JSON Export

```python
import json

# Export entire organization to dictionary
org_data = org.to_dict()

# Convert to JSON
json_str = json.dumps(org_data, indent=2)
print(json_str)
```

## Running Tests

Run the test suite:

```bash
pytest tests/test_organization.py -v
```

All 28 tests cover:
- Employee creation and validation
- Department creation and employee management
- Organization creation and department management
- Query operations
- JSON export
- Complex organizational structures

## Running Examples

Run the comprehensive example script:

```bash
python example_organization.py
```

This demonstrates:
1. Basic organizational structure creation
2. Query operations
3. JSON export
4. Complex multi-department organizations
5. Employee management operations

## Features

- **Type Safety**: Uses Python dataclasses with type hints
- **Validation**: Validates required fields and email format
- **Bidirectional Relationships**: Employees know their departments, departments know their organization
- **Comprehensive Queries**: Find entities by ID, get counts, retrieve collections
- **Data Export**: Convert to dictionary/JSON for serialization
- **Pretty Printing**: Display hierarchical structure in readable format
- **Error Handling**: Clear error messages for validation failures
- **Immutability**: Returns copies of internal lists to prevent external modification

## Best Practices

1. **Always use unique IDs**: Each entity should have a unique identifier
2. **Validate emails**: The Employee class automatically validates email format
3. **Use bidirectional relationships**: Let the classes manage relationships automatically
4. **Export for persistence**: Use `to_dict()` to save organizational data
5. **Test thoroughly**: The test suite provides examples of proper usage

## Future Enhancements

Potential additions:
- Database persistence layer
- Role-based access control
- Organizational chart visualization
- Employee reporting relationships
- Department budgets and metrics
- Historical tracking of changes
- Import from external data sources

## License

This module is part of the amazon-order-automation project and follows the same MIT license.
