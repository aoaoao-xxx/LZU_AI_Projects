PI = 3.1415926
NAME = "黑马★涛哥"

def log_separator1():
    print("-" * 30)
def log_separator2():
    print("+ " * 30)

# 规定 import * 只能拿到 log_separator1 和 PI
__all__ = ["log_separator1", "PI"]
if __name__ == "__main__":
    log_separator2()
