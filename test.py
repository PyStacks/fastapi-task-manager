from models import Task

task = Task(
    id=1,
    name="task",
    description="task"
)

task1 = Task(
    id=2,
    name="task2",
    description="task2"
)

new_task = task.model_dump()
print(new_task.items())

for k,v in new_task.items():
    setattr(task1,k,v)

print(task1)