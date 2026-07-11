import json
from openai import AsyncOpenAI

class PronunciationAnalyzer:
    def __init__(self, template_path="data/prompt_templates.json"):
        with open(template_path, "r", encoding="utf-8") as f:
            self.templates = json.load(f)
        self.client = AsyncOpenAI()

    async def analyze_text(self, student_text: str) -> dict:
        """
        Sử dụng LLM để phân tích cấu trúc cú pháp, lỗi chính tả, dấu thanh 
        và đề xuất cách phát âm chuẩn xác cho học viên người nước ngoài.
        """
        system_prompt = self.templates.get("pronunciation_feedback", "")
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this Vietnamese sentence: '{student_text}'"}
                ],
                temperature=0.3, # Đặt temperature thấp để phân tích chính xác, không sáng tạo lung tung
                response_format={ "type": "json_object" } # Ép OpenAI trả về định dạng JSON chuẩn
            )
            
            # Trả về kết quả phân tích dạng JSON chuyên nghiệp
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {
                "status": "Error",
                "suggestions": f"Failed to run linguistic analysis: {str(e)}"
            }
