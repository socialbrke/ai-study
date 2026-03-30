from openai import OpenAI

class OpenAICompatibelClient:

    def __init__(self,model,api_key,base_url):
        self.model = model
        self.client = OpenAI(api_key = api_key,base_url = base_url)
    
    def generate(self,prompt,system_prompt):
        print("正在调用LLM")
        try:
            messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":prompt}
            ]

            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                stream = False
            )

            answer = response.choices[0].message.content
            print("调用成功")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"