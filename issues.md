# Issues Found (line numbers refer to the original file)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B605) | Security (High) | 21 | `os.system("echo ... " + supplier)` runs through a shell, so a supplier name like `x & del file` could run extra commands | Removed `os.system` and `import os`; the message is now printed with `print()` |
| SQL injection (B608) | Security (Medium) | 11 | The INSERT query is built with `%` string formatting, so quotes or SQL in `supplier`/`item` change the query | Used a parameterized query with `?` placeholders and passed the values as a tuple |
| Silent broad exception (B110 / W0718) | Security (Low) / Bug | 26-28 | `except Exception: pass` hides every failure in `cleanup`, so a failed delete is never noticed | Catch only `sqlite3.Error` and log it with `logging.error` instead of passing |
| Unused argument (W0613) | Bug / Quality | 16 | `remarks` is never used in `markReceived` | Removed the parameter from `mark_received` and from its call |
| Naming style (C0103) | Style | 6, 9, 16, 20, 31 | `placeOrder`, `markReceived`, `notifyWarehouse`, `pendingCount` and `order_total` don't follow snake_case / UPPER_CASE | Renamed functions to snake_case; `order_total` is now a local variable in `main()` |
| Global statement and shadowed `conn` (W0603, W0621) | Design | 4, 10 | The global `order_total` and the global `conn` are redefined inside functions | Removed `global`; `conn` is created in `create_connection()` and passed as an argument; the total is kept in `main()` |
| Missing docstrings (C0114, C0116) | Documentation | 1, 9, 16, 20, 24, 31, 35 | No module or function docstrings | Added a module docstring and a short docstring for every function |
| Long lines and spacing (C0301, E501, E225) | Style | 5, 11, 12, 32 | Lines over the limit, and `order_total+=quantity` has no spaces | Wrapped long strings and statements, added spaces around `+=`, fixed blank lines between functions |