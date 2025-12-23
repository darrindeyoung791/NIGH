# 多语言国际中等教育情报系统

NIGH (**N**ovel **I**nsights into **G**lobal **H**igh Schools)

管理高校及其信息的系统，结合大语言模型和数据可视化功能，提供一站式便捷化数据查询。使用MySQL数据库、Flask后端以及基于HTML、CSS和JavaScript构建的轻量级Web界面。能够实现多角色用户管理、按条件查询与操作、数据可视化交互，AI 解读与查询等功能。网页适配各尺寸屏幕的显示。

## 界面设计

- 扁平化高级简约设计
- 使用符合 Material Design 3 设计规范的界面及其组件
- 字体使用 Inter 和 Noto Sans SC，均使用 Google Fonts 的在线字体
- 引入 Google 的 Material Icon 用于图标展示

## 编码规范

- 使用虚拟环境和 .env 存放 Python 环境和数据库配置信息
- 使用 Flask 推荐的目录规范存放网页和静态数据
- 网页样式和 js 代码放在 static。尽量在拆分和内联样式中选择将重复出现的拆分到一个 styles.css，单次出现的使用内联。每个页面单独存放 js 脚本。