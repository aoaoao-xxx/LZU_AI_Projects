try:
    print("--------------------------")
    # print(my_name)        # NameError
    # print(1 / 0)          # ZeroDivisionError
    # print("ABC"[10])      # IndexError
    print("ABC".hello)      # AttributeError
    print("--------------------------")

except Exception as e:
    print("程序运行出错了，请联系管理员，错误信息：", e)
finally:
    # ✅ 重点：不管 try 里面有没有报错，finally 里代码**一定会执行**
    print("资源释放 ~")
