class Person:
    def __init__(self, name, age):
        self.name= name
        self.age= age

    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old!"

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id= student_id

    def introduce(self):
        return f"Hi, I'm {self.name}, a student. My ID is {self.student_id}, and I'm {self.age} years old!"
    
class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject= subject
    
    def introduce(self):
        return f"Hi, I'm {self.name}, a teacher. I teach {self.subject}, and I'm {self.age} years old!"
    

##Test
student= Student("Marhsall", 17, "S123")
teacher= Teacher("Ms. Müller", 33, "Science")

print("---> School Management System <---")
print(student.introduce())
print(teacher.introduce())
print(f"\nStudent age: {student.age}")
print(f"Teacher subject: {teacher.subject}")

