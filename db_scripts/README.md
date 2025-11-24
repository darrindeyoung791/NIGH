# 数据库设置与导入脚本

此目录包含用于设置 MySQL 数据库以及从 CSV/文本文件导入数据的脚本。

## 文件

- `setup_database.sql`：用于创建数据库和表的 MySQL 脚本
- `import_csv_to_mysql.py`：用于将 CSV/文本文件导入 MySQL 数据库的 Python 脚本

## 设置指南

### 1. 创建数据库和用户

运行 SQL 脚本以创建数据库、表和专用用户：

```sql
mysql -u root -p < setup_database.sql
```

这将创建：
- 数据库: `content_db`
- 用户: `content_user` 密码为 `secure_password`
- 用户的适当权限

### 2. 配置环境变量

在项目根目录下创建 `.env` 文件，用于存储数据库凭据：

```env
DB_HOST=localhost
DB_USER=nigh_content_user
DB_PASSWORD=nigh_secure_password
DB_NAME=content_db
```

> 注意：请确保将 `.env` 添加到 `.gitignore` 文件中，以防止敏感信息被提交到版本控制系统。

### 3. 安装 Python 依赖项

安装所需的包（确保它们已包含在主项目的 `requirements.txt` 中）：

```bash
pip install -r ../../requirements.txt
# 或直接安装：
pip install mysql-connector-python pandas python-dotenv
```

### 4. 运行导入脚本

```bash
python import_csv_to_mysql.py [数据目录路径]
```

如果未提供路径，脚本将默认在 `../db/raw data/` 中查找数据。

## 数据格式

脚本支持以下格式的 CSV 和文本文件：
- 文件应包含：文件名、网址、时间、语言、标题、内容
- 对于文本文件，每个字段应单独占一行
- 对于 CSV 文件，字段应以逗号分隔

## 表结构

导入的数据将存储在 `articles` 表中，包含以下列：
- `id`：每条记录的 UUID（主键）
- `filename`：原始文件名
- `url`：文章网址
- `time_recorded`：记录时间
- `language`：语言代码（例如，“eng”）
- `title`：文章标题
- `content`：文章内容
- `created_at`：记录创建时间戳