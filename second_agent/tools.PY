from serpapi import search as S
from dotenv import load_dotenv
import os

load_dotenv() # 必须先调用这个方法加载 .env 文件
def search(query:str) -> str:
    """
    这是一个基于serpAPI的实战网页搜索引擎工具。
    它会智能解析搜索结果，优先返回直接答案或知识图谱信息。
    """

    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误：api未在.ENV文件里面配置"
        
        params = {
            "engine":"google",
            "q":query,
            "api_key":api_key,
            "hl":"zh-cn"
        }

        client = S(params)
        results = dict(client)
        # 智能解析:优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        
        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"

