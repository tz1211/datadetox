from agents import (
    Agent,
}

class TextSearchIdea(BaseModel):
    """
    A search idea. 
    Defines:
    - query: The search idea.
    - reasoning: Why this is a good search idea in context of the text.
    """
    query: str
    reasoning: str

class TextSearchIdeas(BaseModel):
    """A list of search ideas."""
    ideas: Sequence[TextSearchIdea]

SEARCH_PROMPT = Prompt().get_text_prompt()

text_agent = Agent[ShinanContext](
    name="TextAgent",
    instructions=SEARCH_PROMPT,
    model="gpt-4.1-nano-2025-04-14", 
    model_settings=ModelSettings(tool_choice="required"),
    output_type=TextSearchIdeas,
    tools=[context_tool],
    input_guardrails=[sensitive_guardrail],
)
