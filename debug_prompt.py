def debug_prompt(code, error):
    prompt = f"""
You are tasked with debugging the following code.

Strict rules:
- Only debug the code; do not rewrite or reimagine it.
- Do not change the context or logic of the code.
- Do not alter variable names, function names, or class names.
- Only use the 'manim' library; no additional external libraries are allowed.
- Return the complete corrected code as **plain text** (without explaining about escaping characters like "\\" for JSON).

Here is the code:
{code}

Here is the error:
{error}

Format your final output strictly like this example:
"from manim import *\nclass Frame(Scene):\n    def construct(self):\n        text = Text('Hello').to_edge(CENTER, color='#FFFFFF')\n        self.play(Write(text))"
"""
    return prompt
