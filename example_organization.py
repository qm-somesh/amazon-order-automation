"""
Example usage of the organizational structure module.
Author: qm-somesh
Date: 2025-11-14

This script demonstrates how to:
1. Create an organization
2. Add departments to the organization
3. Add employees to departments
4. Query and display the organizational structure
"""

from datetime import datetime
from src.organization import Organization, Department, Employee


def example_basic_structure():
    """Example 1: Create a basic organizational structure."""
    print("=" * 70)
    print("Example 1: Basic Organizational Structure")
    print("=" * 70)
    print()
    
    # Create organization
    org = Organization(
        id="ORG001",
        name="TechStart Inc",
        description="An innovative technology startup",
        industry="Software Development"
    )
    print(f"Created: {org}")
    print()
    
    # Create departments
    engineering = Department(
        id="DEPT001",
        name="Engineering",
        description="Software development and architecture"
    )
    
    sales = Department(
        id="DEPT002",
        name="Sales",
        description="Business development and customer acquisition"
    )
    
    # Add departments to organization
    org.add_department(engineering)
    org.add_department(sales)
    print(f"Added {org.get_department_count()} departments to organization")
    print()
    
    # Create employees
    cto = Employee(
        id="EMP001",
        name="Alice Johnson",
        email="alice@techstart.com",
        position="Chief Technology Officer",
        hire_date=datetime(2022, 1, 15)
    )
    
    dev1 = Employee(
        id="EMP002",
        name="Bob Smith",
        email="bob@techstart.com",
        position="Senior Software Engineer",
        hire_date=datetime(2022, 3, 1),
        phone="+1-555-0101"
    )
    
    dev2 = Employee(
        id="EMP003",
        name="Carol Davis",
        email="carol@techstart.com",
        position="Software Engineer",
        hire_date=datetime(2023, 6, 15)
    )
    
    sales_mgr = Employee(
        id="EMP004",
        name="David Wilson",
        email="david@techstart.com",
        position="Sales Manager",
        hire_date=datetime(2022, 2, 1)
    )
    
    sales_rep = Employee(
        id="EMP005",
        name="Emma Brown",
        email="emma@techstart.com",
        position="Sales Representative",
        hire_date=datetime(2023, 8, 1)
    )
    
    # Add employees to departments
    engineering.add_employee(cto)
    engineering.add_employee(dev1)
    engineering.add_employee(dev2)
    
    sales.add_employee(sales_mgr)
    sales.add_employee(sales_rep)
    
    print(f"Total employees in organization: {org.get_total_employees()}")
    print()
    
    # Display structure
    print("Organizational Structure:")
    print("-" * 70)
    org.print_structure()
    print()


def example_query_operations():
    """Example 2: Query operations on organizational structure."""
    print("=" * 70)
    print("Example 2: Query Operations")
    print("=" * 70)
    print()
    
    # Build structure
    org = Organization(
        id="ORG002",
        name="Global Corp",
        description="A multinational corporation"
    )
    
    hr_dept = Department(id="DEPT003", name="Human Resources")
    it_dept = Department(id="DEPT004", name="Information Technology")
    
    org.add_department(hr_dept)
    org.add_department(it_dept)
    
    # Add employees
    hr_manager = Employee(id="EMP006", name="Frank Garcia", email="frank@global.com", position="HR Manager")
    recruiter = Employee(id="EMP007", name="Grace Lee", email="grace@global.com", position="Recruiter")
    
    it_manager = Employee(id="EMP008", name="Henry Martinez", email="henry@global.com", position="IT Manager")
    sysadmin = Employee(id="EMP009", name="Ivy Chen", email="ivy@global.com", position="System Administrator")
    
    hr_dept.add_employee(hr_manager)
    hr_dept.add_employee(recruiter)
    
    it_dept.add_employee(it_manager)
    it_dept.add_employee(sysadmin)
    
    # Query operations
    print("1. Find department by ID:")
    found_dept = org.find_department("DEPT004")
    if found_dept:
        print(f"   Found: {found_dept}")
    print()
    
    print("2. Find employee by ID:")
    found_emp = org.find_employee("EMP007")
    if found_emp:
        print(f"   Found: {found_emp}")
        print(f"   Department: {found_emp.department.name}")
    print()
    
    print("3. Get all employees in IT department:")
    it_employees = it_dept.get_employees()
    for emp in it_employees:
        print(f"   - {emp.name} ({emp.position})")
    print()
    
    print("4. Organization statistics:")
    print(f"   Total Departments: {org.get_department_count()}")
    print(f"   Total Employees: {org.get_total_employees()}")
    for dept in org.get_departments():
        print(f"   - {dept.name}: {dept.get_employee_count()} employees")
    print()


def example_json_export():
    """Example 3: Export organizational structure to JSON."""
    print("=" * 70)
    print("Example 3: JSON Export")
    print("=" * 70)
    print()
    
    # Create a simple structure
    org = Organization(
        id="ORG003",
        name="StartupCo",
        description="A small startup",
        industry="E-commerce"
    )
    
    dept = Department(
        id="DEPT005",
        name="Operations",
        description="Day-to-day operations"
    )
    
    org.add_department(dept)
    
    emp1 = Employee(
        id="EMP010",
        name="Jack Robinson",
        email="jack@startupco.com",
        position="Operations Manager",
        hire_date=datetime(2023, 1, 1)
    )
    
    emp2 = Employee(
        id="EMP011",
        name="Karen White",
        email="karen@startupco.com",
        position="Operations Associate",
        hire_date=datetime(2023, 7, 1)
    )
    
    dept.add_employee(emp1)
    dept.add_employee(emp2)
    
    # Export to dictionary
    org_dict = org.to_dict()
    
    print("Organization as dictionary:")
    import json
    print(json.dumps(org_dict, indent=2))
    print()


def example_complex_organization():
    """Example 4: A more complex organizational structure."""
    print("=" * 70)
    print("Example 4: Complex Organization")
    print("=" * 70)
    print()
    
    # Create organization
    org = Organization(
        id="ORG004",
        name="MegaCorp International",
        description="A large multinational enterprise",
        industry="Technology & Consulting",
        founded_date=datetime(2010, 1, 1)
    )
    
    # Create multiple departments
    departments = [
        Department(id="DEPT006", name="Engineering", description="Software Development"),
        Department(id="DEPT007", name="Product Management", description="Product Strategy"),
        Department(id="DEPT008", name="Sales", description="Revenue Generation"),
        Department(id="DEPT009", name="Marketing", description="Brand and Marketing"),
        Department(id="DEPT010", name="Human Resources", description="People Operations"),
        Department(id="DEPT011", name="Finance", description="Financial Management")
    ]
    
    # Add all departments
    for dept in departments:
        org.add_department(dept)
    
    # Add employees to each department
    engineering = org.find_department("DEPT006")
    engineering.add_employee(Employee(id="EMP012", name="Liam Johnson", email="liam@mega.com", position="VP Engineering"))
    engineering.add_employee(Employee(id="EMP013", name="Maya Patel", email="maya@mega.com", position="Tech Lead"))
    engineering.add_employee(Employee(id="EMP014", name="Noah Kim", email="noah@mega.com", position="Senior Engineer"))
    engineering.add_employee(Employee(id="EMP015", name="Olivia Chen", email="olivia@mega.com", position="Engineer"))
    engineering.add_employee(Employee(id="EMP016", name="Peter Singh", email="peter@mega.com", position="Junior Engineer"))
    
    product = org.find_department("DEPT007")
    product.add_employee(Employee(id="EMP017", name="Quinn Davis", email="quinn@mega.com", position="Director of Product"))
    product.add_employee(Employee(id="EMP018", name="Rachel Green", email="rachel@mega.com", position="Product Manager"))
    
    sales = org.find_department("DEPT008")
    sales.add_employee(Employee(id="EMP019", name="Sam Taylor", email="sam@mega.com", position="VP Sales"))
    sales.add_employee(Employee(id="EMP020", name="Tina Brown", email="tina@mega.com", position="Sales Manager"))
    sales.add_employee(Employee(id="EMP021", name="Uma Wilson", email="uma@mega.com", position="Account Executive"))
    
    marketing = org.find_department("DEPT009")
    marketing.add_employee(Employee(id="EMP022", name="Victor Lee", email="victor@mega.com", position="Marketing Director"))
    marketing.add_employee(Employee(id="EMP023", name="Wendy Liu", email="wendy@mega.com", position="Marketing Manager"))
    
    hr = org.find_department("DEPT010")
    hr.add_employee(Employee(id="EMP024", name="Xavier Martinez", email="xavier@mega.com", position="HR Director"))
    hr.add_employee(Employee(id="EMP025", name="Yara Ahmed", email="yara@mega.com", position="HR Manager"))
    
    finance = org.find_department("DEPT011")
    finance.add_employee(Employee(id="EMP026", name="Zane Cooper", email="zane@mega.com", position="CFO"))
    finance.add_employee(Employee(id="EMP027", name="Amy Foster", email="amy@mega.com", position="Financial Analyst"))
    
    # Display full structure
    print(f"Organization: {org.name}")
    print(f"Industry: {org.industry}")
    print(f"Founded: {org.founded_date.year}")
    print()
    print(f"Total Departments: {org.get_department_count()}")
    print(f"Total Employees: {org.get_total_employees()}")
    print()
    print("Complete Structure:")
    print("-" * 70)
    org.print_structure()
    print()
    
    # Department breakdown
    print("Department Breakdown:")
    print("-" * 70)
    for dept in org.get_departments():
        print(f"{dept.name:25} {dept.get_employee_count():3} employees")
    print()


def example_employee_operations():
    """Example 5: Employee management operations."""
    print("=" * 70)
    print("Example 5: Employee Management Operations")
    print("=" * 70)
    print()
    
    org = Organization(id="ORG005", name="DynamicCorp")
    dept = Department(id="DEPT012", name="Customer Success")
    org.add_department(dept)
    
    # Add employees
    emp1 = Employee(id="EMP028", name="Ben Clark", email="ben@dynamic.com", position="CS Manager")
    emp2 = Employee(id="EMP029", name="Cara Hall", email="cara@dynamic.com", position="CS Rep")
    
    print("1. Adding employees to department:")
    dept.add_employee(emp1)
    dept.add_employee(emp2)
    print(f"   Department now has {dept.get_employee_count()} employees")
    print()
    
    print("2. List all employees:")
    for emp in dept.get_employees():
        print(f"   - {emp}")
    print()
    
    print("3. Remove an employee:")
    dept.remove_employee(emp2)
    print(f"   Department now has {dept.get_employee_count()} employees")
    print()
    
    print("4. Find employee by ID:")
    found = dept.find_employee("EMP028")
    if found:
        print(f"   Found: {found.name} - {found.position}")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("*" * 70)
    print(" " * 15 + "ORGANIZATIONAL STRUCTURE EXAMPLES")
    print("*" * 70)
    print("\n")
    
    # Run examples
    example_basic_structure()
    print("\n")
    
    example_query_operations()
    print("\n")
    
    example_json_export()
    print("\n")
    
    example_complex_organization()
    print("\n")
    
    example_employee_operations()
    print("\n")
    
    print("*" * 70)
    print(" " * 20 + "All examples completed!")
    print("*" * 70)
    print("\n")


if __name__ == "__main__":
    main()
