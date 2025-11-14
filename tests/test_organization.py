"""
Unit tests for organizational structure module.
Author: qm-somesh
Date: 2025-11-14

Tests for Organization, Department, and Employee classes.
"""

import pytest
from datetime import datetime
from src.organization import Organization, Department, Employee


class TestEmployee:
    """Test cases for Employee class."""
    
    def test_employee_creation(self):
        """Test creating a valid employee."""
        employee = Employee(
            id="E001",
            name="John Doe",
            email="john.doe@example.com",
            position="Software Engineer"
        )
        
        assert employee.id == "E001"
        assert employee.name == "John Doe"
        assert employee.email == "john.doe@example.com"
        assert employee.position == "Software Engineer"
        assert employee.department is None
    
    def test_employee_with_optional_fields(self):
        """Test creating employee with optional fields."""
        hire_date = datetime(2023, 1, 15)
        employee = Employee(
            id="E002",
            name="Jane Smith",
            email="jane.smith@example.com",
            position="Senior Developer",
            hire_date=hire_date,
            phone="+1-555-0123"
        )
        
        assert employee.hire_date == hire_date
        assert employee.phone == "+1-555-0123"
    
    def test_employee_invalid_email(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            Employee(
                id="E003",
                name="Invalid User",
                email="invalid-email",
                position="Tester"
            )
    
    def test_employee_missing_required_fields(self):
        """Test that missing required fields raise ValueError."""
        with pytest.raises(ValueError, match="Employee must have id, name, and email"):
            Employee(id="", name="Test", email="test@example.com", position="Dev")
    
    def test_employee_to_dict(self):
        """Test employee to_dict conversion."""
        employee = Employee(
            id="E004",
            name="Bob Wilson",
            email="bob@example.com",
            position="Manager"
        )
        
        result = employee.to_dict()
        
        assert result['id'] == "E004"
        assert result['name'] == "Bob Wilson"
        assert result['email'] == "bob@example.com"
        assert result['position'] == "Manager"
        assert result['department'] is None
    
    def test_employee_str(self):
        """Test employee string representation."""
        employee = Employee(
            id="E005",
            name="Alice Brown",
            email="alice@example.com",
            position="Analyst"
        )
        
        str_rep = str(employee)
        assert "Alice Brown" in str_rep
        assert "Analyst" in str_rep


class TestDepartment:
    """Test cases for Department class."""
    
    def test_department_creation(self):
        """Test creating a valid department."""
        dept = Department(
            id="D001",
            name="Engineering",
            description="Software Engineering Department"
        )
        
        assert dept.id == "D001"
        assert dept.name == "Engineering"
        assert dept.description == "Software Engineering Department"
        assert dept.organization is None
        assert dept.get_employee_count() == 0
    
    def test_department_missing_required_fields(self):
        """Test that missing required fields raise ValueError."""
        with pytest.raises(ValueError, match="Department must have id and name"):
            Department(id="", name="Test")
    
    def test_add_employee_to_department(self):
        """Test adding an employee to a department."""
        dept = Department(id="D002", name="HR")
        employee = Employee(
            id="E006",
            name="Charlie Davis",
            email="charlie@example.com",
            position="HR Manager"
        )
        
        dept.add_employee(employee)
        
        assert dept.get_employee_count() == 1
        assert employee in dept.get_employees()
        assert employee.department == dept
    
    def test_add_duplicate_employee(self):
        """Test that adding duplicate employee raises ValueError."""
        dept = Department(id="D003", name="Sales")
        employee = Employee(
            id="E007",
            name="Diana Evans",
            email="diana@example.com",
            position="Sales Rep"
        )
        
        dept.add_employee(employee)
        
        with pytest.raises(ValueError, match="already in"):
            dept.add_employee(employee)
    
    def test_remove_employee_from_department(self):
        """Test removing an employee from a department."""
        dept = Department(id="D004", name="Marketing")
        employee = Employee(
            id="E008",
            name="Frank Green",
            email="frank@example.com",
            position="Marketer"
        )
        
        dept.add_employee(employee)
        assert dept.get_employee_count() == 1
        
        dept.remove_employee(employee)
        assert dept.get_employee_count() == 0
        assert employee.department is None
    
    def test_remove_nonexistent_employee(self):
        """Test that removing non-existent employee raises ValueError."""
        dept = Department(id="D005", name="Finance")
        employee = Employee(
            id="E009",
            name="Grace Hill",
            email="grace@example.com",
            position="Accountant"
        )
        
        with pytest.raises(ValueError, match="not in"):
            dept.remove_employee(employee)
    
    def test_find_employee_in_department(self):
        """Test finding an employee by ID."""
        dept = Department(id="D006", name="IT")
        employee1 = Employee(id="E010", name="Henry", email="henry@example.com", position="IT Support")
        employee2 = Employee(id="E011", name="Ivy", email="ivy@example.com", position="Sysadmin")
        
        dept.add_employee(employee1)
        dept.add_employee(employee2)
        
        found = dept.find_employee("E010")
        assert found == employee1
        
        not_found = dept.find_employee("E999")
        assert not_found is None
    
    def test_department_to_dict(self):
        """Test department to_dict conversion."""
        dept = Department(id="D007", name="Legal", description="Legal Department")
        employee = Employee(id="E012", name="Jack", email="jack@example.com", position="Lawyer")
        
        dept.add_employee(employee)
        
        result = dept.to_dict()
        
        assert result['id'] == "D007"
        assert result['name'] == "Legal"
        assert result['description'] == "Legal Department"
        assert result['employee_count'] == 1
        assert len(result['employees']) == 1
    
    def test_department_str(self):
        """Test department string representation."""
        dept = Department(id="D008", name="Operations")
        
        str_rep = str(dept)
        assert "Operations" in str_rep
        assert "0 employees" in str_rep


class TestOrganization:
    """Test cases for Organization class."""
    
    def test_organization_creation(self):
        """Test creating a valid organization."""
        org = Organization(
            id="O001",
            name="Tech Corp",
            description="A technology company",
            industry="Technology"
        )
        
        assert org.id == "O001"
        assert org.name == "Tech Corp"
        assert org.description == "A technology company"
        assert org.industry == "Technology"
        assert org.get_department_count() == 0
    
    def test_organization_missing_required_fields(self):
        """Test that missing required fields raise ValueError."""
        with pytest.raises(ValueError, match="Organization must have id and name"):
            Organization(id="", name="Test Corp")
    
    def test_add_department_to_organization(self):
        """Test adding a department to an organization."""
        org = Organization(id="O002", name="Global Inc")
        dept = Department(id="D009", name="R&D")
        
        org.add_department(dept)
        
        assert org.get_department_count() == 1
        assert dept in org.get_departments()
        assert dept.organization == org
    
    def test_add_duplicate_department(self):
        """Test that adding duplicate department raises ValueError."""
        org = Organization(id="O003", name="Corp Ltd")
        dept = Department(id="D010", name="Admin")
        
        org.add_department(dept)
        
        with pytest.raises(ValueError, match="already in"):
            org.add_department(dept)
    
    def test_remove_department_from_organization(self):
        """Test removing a department from an organization."""
        org = Organization(id="O004", name="Business Co")
        dept = Department(id="D011", name="Strategy")
        
        org.add_department(dept)
        assert org.get_department_count() == 1
        
        org.remove_department(dept)
        assert org.get_department_count() == 0
        assert dept.organization is None
    
    def test_remove_nonexistent_department(self):
        """Test that removing non-existent department raises ValueError."""
        org = Organization(id="O005", name="Enterprise")
        dept = Department(id="D012", name="Analytics")
        
        with pytest.raises(ValueError, match="not in"):
            org.remove_department(dept)
    
    def test_find_department_in_organization(self):
        """Test finding a department by ID."""
        org = Organization(id="O006", name="Services Inc")
        dept1 = Department(id="D013", name="Support")
        dept2 = Department(id="D014", name="Training")
        
        org.add_department(dept1)
        org.add_department(dept2)
        
        found = org.find_department("D013")
        assert found == dept1
        
        not_found = org.find_department("D999")
        assert not_found is None
    
    def test_find_employee_across_departments(self):
        """Test finding an employee across all departments."""
        org = Organization(id="O007", name="Multi Corp")
        dept1 = Department(id="D015", name="Dev")
        dept2 = Department(id="D016", name="QA")
        
        employee1 = Employee(id="E013", name="Kate", email="kate@example.com", position="Developer")
        employee2 = Employee(id="E014", name="Leo", email="leo@example.com", position="Tester")
        
        dept1.add_employee(employee1)
        dept2.add_employee(employee2)
        
        org.add_department(dept1)
        org.add_department(dept2)
        
        found = org.find_employee("E014")
        assert found == employee2
        
        not_found = org.find_employee("E999")
        assert not_found is None
    
    def test_get_total_employees(self):
        """Test getting total employee count across all departments."""
        org = Organization(id="O008", name="Conglomerate")
        dept1 = Department(id="D017", name="Dept1")
        dept2 = Department(id="D018", name="Dept2")
        
        emp1 = Employee(id="E015", name="Mary", email="mary@example.com", position="Staff")
        emp2 = Employee(id="E016", name="Nick", email="nick@example.com", position="Staff")
        emp3 = Employee(id="E017", name="Oscar", email="oscar@example.com", position="Staff")
        
        dept1.add_employee(emp1)
        dept1.add_employee(emp2)
        dept2.add_employee(emp3)
        
        org.add_department(dept1)
        org.add_department(dept2)
        
        assert org.get_total_employees() == 3
    
    def test_get_all_employees(self):
        """Test getting all employees across all departments."""
        org = Organization(id="O009", name="Holdings")
        dept = Department(id="D019", name="Dept")
        
        emp1 = Employee(id="E018", name="Paul", email="paul@example.com", position="Staff")
        emp2 = Employee(id="E019", name="Quinn", email="quinn@example.com", position="Staff")
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        org.add_department(dept)
        
        all_employees = org.get_all_employees()
        assert len(all_employees) == 2
        assert emp1 in all_employees
        assert emp2 in all_employees
    
    def test_organization_to_dict(self):
        """Test organization to_dict conversion."""
        org = Organization(id="O010", name="Test Org", description="Test")
        dept = Department(id="D020", name="Test Dept")
        emp = Employee(id="E020", name="Rachel", email="rachel@example.com", position="Tester")
        
        dept.add_employee(emp)
        org.add_department(dept)
        
        result = org.to_dict()
        
        assert result['id'] == "O010"
        assert result['name'] == "Test Org"
        assert result['department_count'] == 1
        assert result['total_employees'] == 1
        assert len(result['departments']) == 1
    
    def test_organization_str(self):
        """Test organization string representation."""
        org = Organization(id="O011", name="Example Corp")
        
        str_rep = str(org)
        assert "Example Corp" in str_rep
        assert "0 departments" in str_rep
        assert "0 employees" in str_rep
    
    def test_complex_organization_structure(self):
        """Test a complete organizational structure."""
        # Create organization
        org = Organization(
            id="O012",
            name="TechStart Inc",
            description="A growing tech startup",
            industry="Software"
        )
        
        # Create departments
        eng_dept = Department(id="D021", name="Engineering", description="Software Development")
        hr_dept = Department(id="D022", name="Human Resources", description="HR Operations")
        
        # Create employees
        cto = Employee(id="E021", name="Sarah Johnson", email="sarah@techstart.com", position="CTO")
        dev1 = Employee(id="E022", name="Tom Williams", email="tom@techstart.com", position="Senior Developer")
        dev2 = Employee(id="E023", name="Emma Davis", email="emma@techstart.com", position="Junior Developer")
        
        hr_manager = Employee(id="E024", name="Michael Brown", email="michael@techstart.com", position="HR Manager")
        recruiter = Employee(id="E025", name="Lisa Anderson", email="lisa@techstart.com", position="Recruiter")
        
        # Build structure
        eng_dept.add_employee(cto)
        eng_dept.add_employee(dev1)
        eng_dept.add_employee(dev2)
        
        hr_dept.add_employee(hr_manager)
        hr_dept.add_employee(recruiter)
        
        org.add_department(eng_dept)
        org.add_department(hr_dept)
        
        # Verify structure
        assert org.get_department_count() == 2
        assert org.get_total_employees() == 5
        assert eng_dept.get_employee_count() == 3
        assert hr_dept.get_employee_count() == 2
        
        # Test finding
        found_dept = org.find_department("D021")
        assert found_dept == eng_dept
        
        found_emp = org.find_employee("E023")
        assert found_emp == dev2
        assert found_emp.department == eng_dept
