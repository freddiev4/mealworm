from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from quotientai import QuotientAI

quotient = QuotientAI()

quotient.tracer.init(
    app_name='mealworm',
    environment='development',
    instruments=[OpenAIAgentsInstrumentor()],
)