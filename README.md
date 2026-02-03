HerMath is a Math（or other subjects）learning app，built by python


文件结构
```
HerMath/
│  # 入口程序
│  main.py
│  # 应用核心初始化
│  app.py
│
├───pages/  # 页面/视图模块
│   │  __init__.py  # 标记为Python包，方便导入模块
│   │  admin.py     # 原有管理员页面
│   │  student.py   # 后续扩展：学生端页面
│   │  teacher.py   # 后续扩展：教师端页面
│
├───data/  # 数据相关目录（规整数据文件，避免根目录杂乱）
│   │  database.db  # 原有数据库文件
│   │  init_data.py # 原有数据初始化脚本
│   │  data_backup/ # 后续扩展：数据库备份目录
│
└───utils/  # 工具类目录
    │  __init__.py
    │  common.py    # 后续扩展：通用工具函数（如格式转换、校验等）
    │  db_helper.py # 后续扩展：数据库操作辅助函数
```
