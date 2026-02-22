import os

SUBMISSIONS_DIR = "submissions"
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)


# -------------------------------------------------
# Utility to save file
# -------------------------------------------------
def save_file(name, content):
    with open(os.path.join(SUBMISSIONS_DIR, name), "w") as f:
        f.write(content)


# =================================================
# 1️⃣ TWO SUM (8 variants)
# =================================================

two_sum_variants = [

# 1 Correct (hash map)
"""
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return (seen[diff], i)
        seen[num] = i
""",

# 2 Correct (brute force)
"""
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
""",

# 3 Wrong (returns values not indices)
"""
def two_sum(nums, target):
    for i in nums:
        for j in nums:
            if i + j == target:
                return (i, j)
""",

# 4 Partial (breaks after first loop)
"""
def two_sum(nums, target):
    for i in range(len(nums)):
        if nums[i] + nums[i+1] == target:
            return (i, i+1)
""",

# 5 Inefficient (triple loop)
"""
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            for k in range(len(nums)):
                if nums[i] + nums[j] == target:
                    return (i, j)
""",

# 6 Always returns first two
"""
def two_sum(nums, target):
    return (0, 1)
""",

# 7 Correct but reversed return
"""
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return (i, seen[diff])
        seen[num] = i
""",

# 8 Missing return
"""
def two_sum(nums, target):
    pass
"""
]

for i, code in enumerate(two_sum_variants):
    save_file(f"two_sum_{i+1}.py", code)


# =================================================
# 2️⃣ FIBONACCI (8 variants)
# =================================================

fib_variants = [

# 1 Correct recursive
"""
def fib(n):
    if n < 0:
        return -1
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
""",

# 2 Correct iterative
"""
def fib(n):
    if n < 0:
        return -1
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""",

# 3 Wrong base case
"""
def fib(n):
    if n <= 1:
        return 1
    return fib(n-1) + fib(n-2)
""",

# 4 Returns n
"""
def fib(n):
    return n
""",

# 5 Off-by-one
"""
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-3)
""",

# 6 No negative handling
"""
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
""",

# 7 Infinite recursion
"""
def fib(n):
    return fib(n)
""",

# 8 Memoized correct
"""
def fib(n, memo={}):
    if n < 0:
        return -1
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
"""
]

for i, code in enumerate(fib_variants):
    save_file(f"fib_{i+1}.py", code)


# =================================================
# 3️⃣ CLIMB STAIRS (8 variants)
# =================================================

climb_variants = [

# 1 Correct DP
"""
def climb_stairs(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""",

# 2 Correct recursive
"""
def climb_stairs(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return climb_stairs(n-1) + climb_stairs(n-2)
""",

# 3 Wrong recurrence
"""
def climb_stairs(n):
    return n
""",

# 4 Off-by-one
"""
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n-1) + climb_stairs(n-2)
""",

# 5 Infinite recursion
"""
def climb_stairs(n):
    return climb_stairs(n)
""",

# 6 Always 1
"""
def climb_stairs(n):
    return 1
""",

# 7 No negative check
"""
def climb_stairs(n):
    if n == 0:
        return 1
    return climb_stairs(n-1) + climb_stairs(n-2)
""",

# 8 Efficient iterative
"""
def climb_stairs(n):
    if n < 0:
        return 0
    dp = [0]*(n+1)
    dp[0] = 1
    if n >= 1:
        dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
"""
]

for i, code in enumerate(climb_variants):
    save_file(f"climb_stairs_{i+1}.py", code)


# =================================================
# 4️⃣ VALID PARENTHESES (8 variants)
# =================================================

valid_variants = [

# 1 Correct stack
"""
def is_valid(s):
    stack = []
    mapping = {')':'(', ']':'[', '}':'{'}
    for ch in s:
        if ch in mapping.values():
            stack.append(ch)
        elif ch in mapping:
            if not stack or stack.pop() != mapping[ch]:
                return False
    return not stack
""",

# 2 Wrong: just count
"""
def is_valid(s):
    return s.count('(') == s.count(')')
""",

# 3 Always true
"""
def is_valid(s):
    return True
""",

# 4 Missing order check
"""
def is_valid(s):
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        else:
            stack.pop()
    return True
""",

# 5 Infinite loop
"""
def is_valid(s):
    while True:
        pass
""",

# 6 Partial correct
"""
def is_valid(s):
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            if not stack:
                return False
            stack.pop()
    return True
""",

# 7 Correct simple
"""
def is_valid(s):
    stack = []
    pairs = {')':'(', ']':'[', '}':'{'}
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack
""",

# 8 Empty only valid
"""
def is_valid(s):
    return s == ""
"""
]

for i, code in enumerate(valid_variants):
    save_file(f"is_valid_{i+1}.py", code)


# =================================================
# 5️⃣ COUNT COMPONENTS (8 variants)
# =================================================

graph_variants = [

# 1 Correct DFS
"""
def count_components(n, edges):
    graph = {i: [] for i in range(n)}
    for u,v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    def dfs(node):
        stack = [node]
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                stack.extend(graph[curr])

    count = 0
    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1
    return count
""",

# 2 Wrong: returns n always
"""
def count_components(n, edges):
    return n
""",

# 3 Counts edges
"""
def count_components(n, edges):
    return len(edges)
""",

# 4 No visited
"""
def count_components(n, edges):
    return 1
""",

# 5 Infinite recursion
"""
def count_components(n, edges):
    return count_components(n, edges)
""",

# 6 Correct BFS
"""
def count_components(n, edges):
    graph = {i: [] for i in range(n)}
    for u,v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    for i in range(n):
        if i not in visited:
            queue = [i]
            while queue:
                node = queue.pop(0)
                if node not in visited:
                    visited.add(node)
                    queue.extend(graph[node])
            count += 1
    return count
""",

# 7 Missing undirected add
"""
def count_components(n, edges):
    graph = {i: [] for i in range(n)}
    for u,v in edges:
        graph[u].append(v)

    return 1
""",

# 8 Always 0
"""
def count_components(n, edges):
    return 0
"""
]

for i, code in enumerate(graph_variants):
    save_file(f"count_components_{i+1}.py", code)


print("✅ 40 submission variants generated successfully.")