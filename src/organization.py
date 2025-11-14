"""
Organizational Structure Module
Author: qm-somesh
Date: 2025-11-14

This module provides classes to model an organizational hierarchy with:
- Organizations (top level)
- Departments (under organizations)
- Employees (under departments)
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Employee:
    """Represents an employee within a department."""
    
    id: str
    name: str
    email: str
    position: str
    department: Optional['Department'] = None
    hire_date: Optional[datetime] = None
    phone: Optional[str] = None
    
    def __post_init__(self):
        """Validate employee data after initialization."""
        if not self.id or not self.name or not self.email:
            raise ValueError("Employee must have id, name, and email")
        if '@' not in self.email:
            raise ValueError("Invalid email format")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert employee to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'position': self.position,
            'department': self.department.name if self.department else None,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'phone': self.phone
        }
    
    def __str__(self) -> str:
        """String representation of employee."""
        dept = f" ({self.department.name})" if self.department else ""
        return f"Employee: {self.name} - {self.position}{dept}"


@dataclass
class Department:
    """Represents a department within an organization."""
    
    id: str
    name: str
    description: str = ""
    organization: Optional['Organization'] = None
    manager: Optional[Employee] = None
    _employees: List[Employee] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate department data after initialization."""
        if not self.id or not self.name:
            raise ValueError("Department must have id and name")
    
    def add_employee(self, employee: Employee) -> None:
        """
        Add an employee to this department.
        
        Args:
            employee: The employee to add
            
        Raises:
            ValueError: If employee is already in this department
        """
        if employee in self._employees:
            raise ValueError(f"Employee {employee.name} is already in {self.name}")
        
        # Update employee's department reference
        employee.department = self
        self._employees.append(employee)
    
    def remove_employee(self, employee: Employee) -> None:
        """
        Remove an employee from this department.
        
        Args:
            employee: The employee to remove
            
        Raises:
            ValueError: If employee is not in this department
        """
        if employee not in self._employees:
            raise ValueError(f"Employee {employee.name} is not in {self.name}")
        
        employee.department = None
        self._employees.remove(employee)
    
    def get_employees(self) -> List[Employee]:
        """Get all employees in this department."""
        return self._employees.copy()
    
    def get_employee_count(self) -> int:
        """Get the number of employees in this department."""
        return len(self._employees)
    
    def find_employee(self, employee_id: str) -> Optional[Employee]:
        """
        Find an employee by ID.
        
        Args:
            employee_id: The employee ID to search for
            
        Returns:
            The employee if found, None otherwise
        """
        for employee in self._employees:
            if employee.id == employee_id:
                return employee
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert department to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'organization': self.organization.name if self.organization else None,
            'manager': self.manager.name if self.manager else None,
            'employee_count': self.get_employee_count(),
            'employees': [emp.to_dict() for emp in self._employees]
        }
    
    def __str__(self) -> str:
        """String representation of department."""
        org = f" ({self.organization.name})" if self.organization else ""
        return f"Department: {self.name}{org} - {self.get_employee_count()} employees"


@dataclass
class Organization:
    """Represents an organization containing departments."""
    
    id: str
    name: str
    description: str = ""
    industry: Optional[str] = None
    founded_date: Optional[datetime] = None
    _departments: List[Department] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate organization data after initialization."""
        if not self.id or not self.name:
            raise ValueError("Organization must have id and name")
    
    def add_department(self, department: Department) -> None:
        """
        Add a department to this organization.
        
        Args:
            department: The department to add
            
        Raises:
            ValueError: If department is already in this organization
        """
        if department in self._departments:
            raise ValueError(f"Department {department.name} is already in {self.name}")
        
        # Update department's organization reference
        department.organization = self
        self._departments.append(department)
    
    def remove_department(self, department: Department) -> None:
        """
        Remove a department from this organization.
        
        Args:
            department: The department to remove
            
        Raises:
            ValueError: If department is not in this organization
        """
        if department not in self._departments:
            raise ValueError(f"Department {department.name} is not in {self.name}")
        
        department.organization = None
        self._departments.remove(department)
    
    def get_departments(self) -> List[Department]:
        """Get all departments in this organization."""
        return self._departments.copy()
    
    def get_department_count(self) -> int:
        """Get the number of departments in this organization."""
        return len(self._departments)
    
    def find_department(self, department_id: str) -> Optional[Department]:
        """
        Find a department by ID.
        
        Args:
            department_id: The department ID to search for
            
        Returns:
            The department if found, None otherwise
        """
        for department in self._departments:
            if department.id == department_id:
                return department
        return None
    
    def find_employee(self, employee_id: str) -> Optional[Employee]:
        """
        Find an employee across all departments.
        
        Args:
            employee_id: The employee ID to search for
            
        Returns:
            The employee if found, None otherwise
        """
        for department in self._departments:
            employee = department.find_employee(employee_id)
            if employee:
                return employee
        return None
    
    def get_total_employees(self) -> int:
        """Get the total number of employees across all departments."""
        return sum(dept.get_employee_count() for dept in self._departments)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees across all departments."""
        all_employees = []
        for department in self._departments:
            all_employees.extend(department.get_employees())
        return all_employees
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert organization to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'industry': self.industry,
            'founded_date': self.founded_date.isoformat() if self.founded_date else None,
            'department_count': self.get_department_count(),
            'total_employees': self.get_total_employees(),
            'departments': [dept.to_dict() for dept in self._departments]
        }
    
    def __str__(self) -> str:
        """String representation of organization."""
        return (f"Organization: {self.name} - "
                f"{self.get_department_count()} departments, "
                f"{self.get_total_employees()} employees")
    
    def print_structure(self, indent: int = 0) -> None:
        """
        Print the complete organizational structure.
        
        Args:
            indent: The indentation level for nested printing
        """
        prefix = "  " * indent
        print(f"{prefix}{self}")
        
        for dept in self._departments:
            print(f"{prefix}  {dept}")
            for emp in dept.get_employees():
                print(f"{prefix}    - {emp.name} ({emp.position})")
