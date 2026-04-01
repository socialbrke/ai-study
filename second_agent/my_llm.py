import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List,Dict

load_dotenv()

class HelloAgentsLLM:
    def __init__(self,model=None,apikey=None,baseurl=None,timeout=None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        self.apikey = apikey or os.getenv("LLM_API_KEY")
        self.baseurl = baseurl or os.getenv("LLM_BASE_URL")
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model,self.apikey,self.baseurl]):
            raise ValueError("模型ID，密钥和服务地址必须被提供在.env文件中定义")
        
        self.client = OpenAI(api_key = self.apikey,base_url= self.baseurl,timeout=self.timeout)
        
    def think(self,message,temperature=0):
        print(f'🧠 正在调用 {self.model} 模型...')
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = message,
                temperature = temperature,
                stream = False
            )
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            return response.choices[0].message.content
            '''
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)
            '''

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None

if __name__ == "__main__":
    try:
        llmclient = HelloAgentsLLM()
        example = [{"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}]
        
        print("---调用llm---")
        responsetext = llmclient.think(example)
        if responsetext:
            print("\n\n--- 完整模型响应 ---")
            print(responsetext)

    except ValueError as e:
        print(e)