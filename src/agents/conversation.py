import json
from openai import AsyncOpenAI

class VietnameseCoachAgent:
    def __init__(self, template_path="data/prompt_templates.json"):
        with open(template_path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)
        self.client = AsyncOpenAI()
        self.memory = []

    async def generate_response(self, user_input: str, learner_level: str = "beginner") -> str:
        """
        Gọi API OpenAI thật để tạo phản hồi cá nhân hóa theo trình độ học viên,
        có tích hợp bộ nhớ lưu trữ ngữ cảnh hội thoại.
        """
        system_prompt = self.templates.get(f"{learner_level}_conversation", "")
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.memory)
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            ai_reply = response.choices[0].message.content.strip()
          
            self.memory.append({"role": "user", "content": user_input})
            self.memory.append({"role": "assistant", "content": ai_reply})
            
            if len(self.memory) > 12:
                self.memory = self.memory[-12:]
                
            return ai_reply
        except Exception as e:
            return f"[Error connecting to OpenAI]: {str(e)}"
