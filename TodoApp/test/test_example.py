import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2
    

class Student:
    def __init__(self, firstname: str, lastname: str, major: str, years: int):
        self.firstname = firstname
        self.lastname = lastname
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 2)

def test_student_attributes(default_student):
    assert default_student.firstname == "John"
    assert default_student.lastname == "Doe"
    assert default_student.major == "Computer Science"
    assert default_student.years == 2