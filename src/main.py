import asyncio
from agents.conversation import VietnameseCoachAgent
from agents.pronunciation import PronunciationAnalyzer

async def main():
    print("====================================================")
    print("🚀 PRODUCTION-READY: AI VIETNAMESE FLUENCY ENGINE 🚀")
    print("====================================================\n")
    
    coach = VietnameseCoachAgent()
    analyzer = PronunciationAnalyzer()
    
    student_session = [
        "Xin chào! Tôi là David. Rất vui được học tiếng Việt.",
        "Tôi muốn học cách gọi món tại quán cà phê.",
        "Cho tôi một ly cà phê sửa đá không đường" 
    ]
    
    for user_text in student_session:
        print(f"\n[Student]: {user_text}")
        
        coach_task = asyncio.create_task(coach.generate_response(user_text, learner_level="beginner"))
        analysis_task = asyncio.create_task(analyzer.analyze_text(user_text))
        
        ai_reply, analysis_result = await asyncio.gather(coach_task, analysis_task)
        
        print(f"[AI Coach]: {ai_reply}")
        print(f"[Linguistic Feedback Check]:")
        print(f"  - Status: {analysis_result.get('status')}")
        print(f"  - Suggestions: {analysis_result.get('suggestions')}")
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(main())
