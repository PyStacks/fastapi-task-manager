import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute("""
    create table if not exists tasks (
        id integer primary key autoincrement,
        name text not null,
        description text,
        priority integer default 3,
        done integer default 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    )
""")

# 插入数据
name = '学习SQLITE数据库操作'
description = '第二周的学习任务，理解语法并进行运用'
priority = 4

cursor.execute("INSERT INTO tasks(name, description, priority) values(?,?,?)",
               (name, description, priority))

conn.commit()
print(f"插入成功，ID：{cursor.lastrowid}")

# 查询数据
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()
for row in rows:
    print(f"ID:{row[0]}, Name:{row[1]}, Description:{row[2]}, Priority:{row[3]}")

# 转换为字典格式
cursor.execute("SELECT * FROM tasks")
# print(cursor.description)
# print(cursor.fetchall())
columns = [desc[0] for desc in cursor.description]
tasks_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
print(tasks_dict)

# 关闭连接
conn.close()
