# Linear Algebra Lab

一个用 Python 从零实现线性代数基础算法的学习项目。

项目不依赖 NumPy 等数值计算库，重点是把矩阵、向量、高斯消元和 LU 分解的数学过程写成可阅读、可测试的代码，并提供 LU 分解的交互式动画。

## 已实现的功能

- `Vector`：向量加减、数乘、点积、长度；
- `Matrix`：矩阵加减、数乘、矩阵乘法、矩阵乘向量、转置；
- 高斯消元：求解唯一解的线性方程组；
- LU 分解：分解 `A = L @ U`，并通过前代、回代求解 `A @ x = b`；
- LU 可视化：播放消元、构造 `L/U`、前代求 `y` 与回代求 `x` 的过程；
- 自动化测试：验证核心运算、求解器、LU 分解与可视化步骤。

## 项目结构

```text
linear-algebra-lab/
├── linear_algebra/              # 可导入的核心线性代数包
│   ├── vector.py                # Vector 类
│   ├── matrix.py                # Matrix 类
│   ├── solver.py                # 高斯消元的公开接口 solve(A, b)
│   └── algorithms/
│       ├── elimination.py       # 高斯消元实现
│       ├── lu.py                # LU 分解与 solve_lu(A, b)
│       └── operations.py        # 单位矩阵、增广矩阵
├── visualization/               # 不改动核心算法的可视化模块
│   ├── lu_steps.py              # 记录 LU 算法的状态快照
│   └── lu_visualizer.py         # 深色主题 Tkinter 动画窗口
├── examples/                    # 可直接运行的示例
├── tests/                       # 自动化测试
└── pyproject.toml               # 项目元数据
```

## 环境与安装

需要 Python 3.10 或更高版本。项目的核心与可视化均使用 Python 标准库；不安装也可以直接运行。

可选：以可编辑模式安装项目。

```powershell
pip install -e .
```

## 基础使用

```python
from linear_algebra import Matrix, Vector, solve

A = Matrix([[2, 0], [0, 3]])
v = Vector([1, 2])

print(A @ v)  # [2, 6]

# 解 A @ x = b
coefficients = Matrix([[2, 1], [1, -1]])
constants = Vector([5, 1])

print(solve(coefficients, constants))  # [2.0, 1.0]
```

运行基础示例：

```powershell
python examples\basic_usage.py
```

## LU 分解

LU 分解将系数矩阵拆成：

```text
A = L @ U
```

求解 `A @ x = b` 时，程序依次执行：

```text
L @ y = b     # 前代：从上到下求 y
U @ x = y     # 回代：从下到上求 x
```

```python
from linear_algebra import Matrix, Vector, lu_decompose, solve_lu

A = Matrix([[2, 1], [4, 3]])
b = Vector([5, 11])

L, U = lu_decompose(A)
x = solve_lu(A, b)

print(L)
print(U)
print(x)  # 单列矩阵：[2.0]、[1.0]
```

当前 LU 实现是最基础的无行交换版本；遇到零主元会报错。高斯消元求解器则使用主元交换处理此类情况。

## LU 可视化动画

在项目根目录运行：

```powershell
python -m visualization.lu_visualizer
```

窗口支持：

- 自定义输入矩阵 `A` 和向量 `b`；
- 上一步、下一步、自动播放；
- 高亮当前主元与目标消元行；
- 显示消元倍数写入 `L`；
- 动画展示前代求 `y` 与回代求 `x`；
- 深色主题与算法阶段进度条。

输入格式如下：矩阵每行以英文分号 `;` 分隔，同行数字以空格分隔；向量数字以空格分隔。

```text
A：2 1; 4 3
b：5 11
```

对应：

```text
A = [2  1]      b = [ 5]
    [4  3]          [11]
```

## 测试

在项目根目录运行全部测试：

```powershell
python -m unittest discover -s tests -v
```

测试覆盖矩阵与向量基础运算、高斯消元、LU 分解、错误输入处理，以及可视化步骤数据。
