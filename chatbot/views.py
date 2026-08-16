from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .ollama_client import ask_ollama


class ChatbotView(LoginRequiredMixin, TemplateView):
    """
    AI chatbot powered by local Ollama.
    """

    template_name = "chatbot/chat.html"

    def post(self, request, *args, **kwargs):

        message = request.POST.get(
            "message",
            "",
        ).strip()

        if not message:

            return self.render_to_response(
                {
                    "error": "Please enter a message."
                }
            )

        prompt = f"""
You are an AI assistant inside an Employee Management System (EMS).

The system contains:
- Employee management
- Department management
- Attendance management
- Leave management
- Reports
- User authentication and authorization

Answer the user's question clearly and professionally.

Do not invent employee records, passwords, private information,
or database information that has not been provided.

User question:
{message}
"""

        answer = ask_ollama(prompt)

        return self.render_to_response(
            {
                "user_message": message,
                "answer": answer,
            }
        )