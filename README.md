# 🚂 Create Train Tracker (findtrine)

一个用于从《机械动力》（Create Mod）存档文件 `create_tracks.dat` 中查找、定位列车信息的命令行工具。

无需启动游戏，即可快速查看存档中所有列车的名称、车厢坐标、所在维度等信息，支持按名称搜索。

---

## ✨ 功能特点

- ✅ 解析 `create_tracks.dat` 文件，提取所有列车数据
- ✅ 显示每趟列车的名称（支持 JSON 格式名称的解析）
- ✅ 列出每节车厢的 **驾驶台坐标**（如果存在）或 **轮子坐标**
- ✅ 输出坐标对应的维度（主世界、下界、末地）
- ✅ 支持按列车名称关键词搜索
- ✅ 纯 Python 实现，轻量易用

---

## 📦 安装依赖

本工具需要 Python 3.6 或更高版本，并依赖 `nbtlib` 库。

```bash
pip install nbtlib
```

---

## ⬇️ 下载脚本

将本仓库中的 `findtrine.py` 文件下载到本地，或克隆整个仓库：

```bash
git clone https://github.com/你的用户名/findtrine.git
cd findtrine
```

---

## 🚀 使用方法

在命令行中运行：

```bash
python findtrine.py --file "路径/你的存档/create_tracks.dat" [--name "列车名关键词"]
```

### 参数说明

| 参数 | 简写 | 说明 |
|------|------|------|
| `--file` | `-f` | **必需**。指定 `create_tracks.dat` 文件的完整路径。 |
| `--name` | `-n` | 可选。按列车名称关键词搜索（不区分大小写）。省略则列出所有列车。 |

---

## 📝 示例

### 示例 1：列出存档中所有列车

```bash
python findtrine.py --file "E:\Minecraft\saves\我的世界\create_tracks.dat"
```

输出示例：
```
正在读取文件: E:\Minecraft\saves\我的世界\create_tracks.dat
共找到 3 个列车：

=== 列车: 特快列车 ===
路径: .data.RailGraphs[0].Trains[0]
  车厢 1:
    驾驶台坐标: (123.45, 67.89, 234.56) 维度 minecraft:overworld

=== 列车: 货运专线 ===
路径: .data.RailGraphs[0].Trains[1]
  车厢 1:
    FirstBogey.Point[0]: 坐标 (987.65, 43.21, -123.45) 维度 minecraft:overworld
    SecondBogey.Point[0]: 坐标 (990.12, 43.21, -120.78) 维度 minecraft:overworld
```

### 示例 2：搜索名称为“特快”的列车

```bash
python findtrine.py --file "E:\save\create_tracks.dat" --name "特快"
```

输出仅显示名称中包含“特快”的列车信息。

---

## ❓ 常见问题

**Q：找不到 `create_tracks.dat` 文件？**  
A：该文件通常位于你的 Minecraft 存档文件夹中（例如 `.minecraft/saves/你的存档/`）。如果游戏未加载过机械动力列车，文件可能不存在，请先在游戏中创建列车。

**Q：运行后显示“未找到任何列车”**  
A：可能存档中确实没有列车，或者文件路径错误。请检查路径并使用完整绝对路径。

**Q：坐标显示为 (0.00, 0.00, 0.00)**  
A：可能该车厢尚未在铁轨上放置，或者数据尚未被游戏保存。尝试进入游戏让列车跑动一下，再重新读取。

---

## 📜 许可证

本项目采用 **MIT 许可证**，详情请参见 [LICENSE](LICENSE) 文件。

你可以自由使用、修改、分发本工具，但请保留原版权声明。

---

## 🤝 贡献与反馈

如果你发现了 Bug，或有新功能建议，欢迎在 GitHub 仓库的 [Issues](https://github.com/xiaoou6630/findtrine/issues) 中提出。

如果你喜欢这个工具，不妨点个 ⭐ 支持一下！

---

## 📌 注意事项

- 本工具**只读取文件，不会修改任何存档数据**，请放心使用。
- 支持 Minecraft 1.16+ 及对应版本的 Create 模组（列车系统引入后的版本）。

