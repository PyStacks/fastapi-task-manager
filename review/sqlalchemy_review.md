# SQLAlchemy核心概念复习

## 1. Session是什么？

Session就像"工作区"：
- 你做的所有修改都在Session里暂存
- `commit()`才真正写入数据库
- `rollback()`放弃所有修改
- `close()`后不能再操作

## 2. 懒加载 vs 预加载

| 方式 | 代码 | SQL执行时机 | 适用场景 |
|------|------|-------------|----------|
| 懒加载 | `user.tasks` | 访问属性时 | 确定需要关联数据时才用 |
| 预加载 | `.options(joinedload(User.tasks))` | 主查询时 | 确定要用关联数据时 |

## 3. 常见错误

### 错误1：Session已关闭后访问懒加载属性
```python
def get_user(db: Session):
    return db.query(User).first()

user = get_user(db)  # db已关闭
print(user.tasks)    # ❌ 报错：Session已关闭
```
### 错误2：N+1查询
- 症状：日志里看到大量相似的SELECT语句
- 解决：用joinedload或selectinload
####  方案 1：joinedload
```python
from sqlalchemy.orm import joinedload

users = (
    db.query(User)
    .options(joinedload(User.tasks))
    .limit(3)
    .all()
)
```
#### 方案 2：selectinload
```
from sqlalchemy.orm import selectinload

users = (
    db.query(User)
    .options(selectinload(User.tasks))
    .limit(3)
    .all()
)
```
### joinedload vs selectinload 对比

| 方式 | SQL 条数 | 底层实现 | 优点                |缺点|适用场景|
|------|------|-------------|-------------------|----|---
| joinedload | 1 条 | LEFT JOIN 联表查询 | 只发起一次数据库请求        |一对多时主表数据会重复传输，内存开销变大|一对一、关联数据量较小场景
| selectinload | 2 条 | 先查主表，再通过 IN () 查询所有关联数据 | 不会产生主数据重复，一对多性能更好 |需要两次数据库交互|一对多（User -> Tasks）推荐首选
