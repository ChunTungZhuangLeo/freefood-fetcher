"""
Core AI Assistant Agent
This is your main AI agent that can be customized for your hackathon project.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class AIAssistant:
    """Personal AI Assistant that can be extended for various tasks."""

    def __init__(self, system_prompt: str = None):
        self.system_prompt = system_prompt or """You are a helpful personal AI assistant.
        You help users with their daily tasks, answer questions, and automate workflows.
        Be concise, friendly, and proactive in offering help."""
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """Send a message and get a response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def analyze_text(self, text: str, task: str) -> str:
        """Analyze text for a specific task (summarize, extract, categorize, etc.)."""
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"Task: {task}\n\nText to analyze:\n{text}"
            }]
        )
        return response.content[0].text

    def generate_content(self, prompt: str, content_type: str = "text") -> str:
        """Generate content based on a prompt."""
        system = f"You are a creative {content_type} generator. Create engaging, high-quality content."

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []


# Example specialized agents you can create:

class StudyBuddyAgent(AIAssistant):
    """AI Study Assistant for students."""

    def __init__(self):
        super().__init__(system_prompt="""You are an AI study buddy for college students.
        You help with:
        - Summarizing lecture notes and textbooks
        - Creating study schedules
        - Generating practice quizzes
        - Explaining complex concepts simply
        - Providing motivation and study tips
        Be encouraging, clear, and educational.""")

    def summarize_notes(self, notes: str) -> str:
        return self.analyze_text(notes, "Summarize these lecture notes into key points and concepts")

    def generate_quiz(self, topic: str, num_questions: int = 5) -> str:
        prompt = f"Create {num_questions} quiz questions about: {topic}. Include answers at the end."
        return self.generate_content(prompt, "quiz")

    def explain_concept(self, concept: str) -> str:
        prompt = f"Explain this concept in simple terms with examples: {concept}"
        return self.chat(prompt)


class EmailTriageAgent(AIAssistant):
    """AI Email Management Assistant."""

    def __init__(self):
        super().__init__(system_prompt="""You are an AI email assistant.
        You help users manage their inbox by:
        - Categorizing emails (Urgent, Important, FYI, Spam)
        - Summarizing long email threads
        - Drafting responses
        - Extracting action items
        Be professional and efficient.""")

    def categorize_email(self, email_content: str) -> dict:
        prompt = f"""Categorize this email and respond in this exact format:
        CATEGORY: [Urgent/Important/FYI/Spam]
        SUMMARY: [One sentence summary]
        ACTION_REQUIRED: [Yes/No]
        SUGGESTED_ACTION: [What to do]

        Email:
        {email_content}"""

        response = self.analyze_text(email_content, prompt)
        return response

    def draft_reply(self, email_content: str, tone: str = "professional") -> str:
        prompt = f"Draft a {tone} reply to this email:\n{email_content}"
        return self.generate_content(prompt, "email reply")


if __name__ == "__main__":
    # Quick test
    assistant = AIAssistant()
    print("AI Assistant initialized. Testing...")
    response = assistant.chat("Hello! What can you help me with today?")
    print(f"Response: {response}")
