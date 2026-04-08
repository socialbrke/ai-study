def tags():
    def put_desc(fun):
        fun.desc = "这个拿去注册嘛"
        return fun
    return put_desc