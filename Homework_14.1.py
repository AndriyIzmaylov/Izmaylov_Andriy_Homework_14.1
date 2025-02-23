# Модифікуйте клас Група (завдання минулої лекції) так, щоб при спробі додавання до
# групи більше 10-ти студентів, було порушено виняток користувача.
#
# Таким чином потрібно створити ще й виняток користувача для цієї ситуації. І обробити
# його поза межами класу. Тобто. потрібно перехопити цей виняток,
# при спробі додавання 11-го студента

class GroupLimitError(Exception):

    def __init__(self, message="Group limit reached. Cannot add more than 10 students."):
        super().__init__(message)


class Human:

    def __init__(self, gender, age, first_name, last_name):
        self.gender = gender
        self.age = age
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.age} years old, {self.gender}'


class Student(Human):

    def __init__(self, gender, age, first_name, last_name, record_book):
        super().__init__(gender, age, first_name, last_name)
        self.record_book = record_book

    def __str__(self):
        return f'{super().__str__()}, Record Book: {self.record_book}'

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.first_name == other.first_name and self.last_name == other.last_name
        return False

    def __hash__(self):
        return hash((self.first_name, self.last_name))


class Group:
    MAX_STUDENTS = 10

    def __init__(self, number):
        self.number = number
        self.group = set()

    def add_student(self, student):
        if len(self.group) >= self.MAX_STUDENTS:
            raise GroupLimitError()
        self.group.add(student)

    def delete_student(self, last_name):
        student = self.find_student(last_name)
        if student:
            self.group.remove(student)

    def find_student(self, last_name):
        for student in self.group:
            if student.last_name == last_name:
                return student
        return None

    def __str__(self):
        all_students = '\n'.join(str(student) for student in self.group)
        return f'Number: {self.number}\n{all_students}'


st1 = Student('Male', 30, 'Steve', 'Jobs', 'AN142')
st2 = Student('Female', 25, 'Liza', 'Taylor', 'AN145')
gr = Group('PD1')
gr.add_student(st1)
gr.add_student(st2)
print(gr)
assert str(gr.find_student('Jobs')) == str(st1), 'Test1'
assert gr.find_student('Jobs2') is None, 'Test2'
assert isinstance(gr.find_student('Jobs'), Student) is True, 'The find method should return an instance'

gr.delete_student('Taylor')
print(gr)

gr.delete_student('Taylor')

gr = Group('PD1')

for i in range(10):
    gr.add_student(Student('Male', 20 + i, f'Student{i}', f'Lastname{i}', f'AI1{i}'))

print(gr)

try:
    gr.add_student(Student('Male', 30, 'Extra', 'Student', 'AN999'))
except GroupLimitError as e:
    print(f'Error: {e}')
