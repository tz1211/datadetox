# Prompt Class
# 
# Written by Kushal Chattopadhyay for Datadetox project and educational purposes
# Uses RAG-based context engineering

class Prompt:
    """
    A class that contains all the prompts for the agents.
    """

    def __init__(self) -> None:
        self

    def eclair_hf_prompt(self):
        """Get the research instruction prompt."""
        PROMPT = (
            f"""
            Your task is to obtain the following info for the model.
            You must include the following. You must call 1 Hugging Face tool per task.
            You also have this information from the foundation model's family page
            You must indicate this.
            {{foundation_model_family()}}

                - "Foundation Model Family name & summary: if not found, say Did not find in dataset."
                - "Retrieve model architecture details",
                - "Get model size and parameters",
                - "Obtain training dataset information",
                - "Check model license and usage restrictions"
                - "Find related models that are related." 
            `

            """
        )
        return PROMPT
