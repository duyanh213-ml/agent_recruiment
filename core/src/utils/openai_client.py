from openai import OpenAI
from src.settings.settings import OpenAISettings


class RecruitmentOpenAI:
    
    def __init__(self):
        self.client = OpenAI(api_key=OpenAISettings.LLM_API_KEY)
        
    def get_completions(self, prompts: str, system_role: str, system_content: str):
        completion = self.client.chat.completions.create(
            model=OpenAISettings.MODEL,
            messages=[
                {"role": system_role, "content": system_content},
                {
                    "role": "user",
                    "content": prompts
                }
            ]
        )
        return completion.choices[0].message.content
    
    
recruitment_openai = RecruitmentOpenAI()