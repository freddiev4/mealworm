from openinference.instrumentation.agno import AgnoInstrumentor
from quotientai import QuotientAI

quotient = QuotientAI()

quotient.tracer.init(
    app_name='mealworm',
    environment='development',
    instruments=[AgnoInstrumentor()],
)