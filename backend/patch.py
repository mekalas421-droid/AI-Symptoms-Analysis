import sys

path = 'app/models/user.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = 'role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), default=UserRole.PATIENT)'
new_str = 'role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role", values_callable=lambda obj: [e.value for e in obj]), default=UserRole.PATIENT)'

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed user.py')
else:
    print('String not found in user.py')
