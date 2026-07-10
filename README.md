BuJiDao-PlatformPatcher

«一个用于 Minecraft PC 端 Mod 补丁自动检测、部署与管理的 Windows 后台工具。»

📌 项目介绍

BuJiDao-PlatformPatcher 是一个基于 Python 开发的 Windows 桌面工具，用于自动化处理 Minecraft PC 端补丁部署流程。

程序运行后会在后台监听目标文件变化，当检测到新的 Mod/补丁文件生成时，会自动完成文件定位、补丁部署等操作。

项目目标：

- 简化 Minecraft PC Mod 补丁安装流程
- 自动检测目标文件变化
- 减少手动复制文件操作
- 提供后台托盘运行体验

---

✨ 功能特点

文件监听

- 自动检测 Minecraft 相关目录
- 自动识别新的补丁文件
- 支持路径变化检测

自动部署

- 自动复制补丁文件
- 自动处理目标目录
- 避免重复部署

后台运行

- Windows 系统托盘支持
- 后台监听模式
- 状态通知提醒

用户体验

- 图形化界面
- 日志记录
- 异常捕获
- 自动化运行流程

---

🖥️ 运行环境

支持：

- Windows 10 / Windows 11

开发环境：

- Python 3.11+
- PySide6

---

📦 项目结构

BuJiDao-PlatformPatcher
│
├── main.py              # 程序入口
├── ui.py                # 主界面
├── tray.py              # 系统托盘
├── monitor.py           # 后台监听
├── file_detector.py     # 文件检测
├── patcher.py           # 补丁处理
├── notifier.py          # 系统通知
├── logger.py            # 日志系统
│
└── assets
    └── app.ico

---

🚀 使用方式

1. 启动程序

2. 开启监听模式

3. 启动 Minecraft PC

4. 程序自动检测补丁文件

5. 自动执行部署流程

---

🛠️ 技术栈

- Python
- PySide6
- Windows API
- 文件系统监听
- 多线程任务管理

---

📸 截图

<img width="482" height="370" alt="image" src="https://github.com/user-attachments/assets/3bf0e9cf-b294-42c0-9a52-092dc578a7c7" />


---

⚠️ 注意事项

- 本项目目前主要针对特定 Minecraft PC 环境开发。
- 使用前请确认补丁来源可靠。
- 请勿用于未经授权的软件修改行为。
⚠️ 使用声明

本项目仅供学习、研究和技术交流使用。

下载并使用本项目即代表你理解并同意：

- 请勿将本项目用于任何未经授权的用途。
- 请遵守当地法律法规以及相关软件的用户协议。
- 使用本项目产生的任何风险和后果，由使用者自行承担。

如果你不再需要本项目，请及时删除相关文件。

作者不对因使用本项目造成的任何直接或间接损失承担责任。

---

## 📄 开源协议

本项目采用 GNU General Public License v3.0（GPL-3.0）开源协议。

你可以自由使用、修改和重新发布本项目，但必须遵守 GPL-3.0 协议要求。

详细内容请查看 LICENSE 文件。
---

👤 Author

KOKO-GPT

---

有编译需求的，请运行资源文件夹内的build.bat
