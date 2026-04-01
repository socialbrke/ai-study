from typing import Dict,Any
from tools import search

class ToolExecutor:
    """
    一个工具执行器，负责 管理和执行工具
    """
    def __init__(self):
        self.tools:Dict[str,Dict[str,Any]] = {}

    def registertool(self,name:str,description:str,func:callable):
        if name in self.tools:
            print("工具已经存在了")
        self.tools[name] = {"description":description,"func":func}
        print(f"工具‘{name}’已注册")

    def gettool(self,name:str) -> callable:
        return self.tools.get(name,{}).get("func")
    
    def getavailabletools(self) ->str:
        return "\n".join([
        f"- {name}: {info['description']}" 
        for name, info in self.tools.items()
        ])

if __name__ == "__main__":
    ToolExecutor = ToolExecutor()
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    ToolExecutor.registertool("search",search_description,search)

    print("---------看一下有哪些可以用的工具呢-----------")
    print(ToolExecutor.getavailabletools())

    print("-----执行Action：Search['英伟达最新的gpu型号是什么？']")
    tool_name = "search"
    tool_input = "intel最新的cPU型号是什么"

    tool_function = ToolExecutor.gettool(tool_name)
    if tool_function:
        print("-----观察")
        print(tool_function(tool_input))
    else:
        print("错误，未找到对应的工具哦")