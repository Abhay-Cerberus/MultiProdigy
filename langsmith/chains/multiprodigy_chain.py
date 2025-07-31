from langchain.tools import Tool

def math_chain(input_str):
    try:
        return str(eval(input_str))
    except:
        return "Invalid math expression"

def joke_chain(_):
    return "Why don't scientists trust atoms? Because they make up everything!"

tools = [
    Tool(name="MathTool", func=math_chain, description="Performs math calculations"),
    Tool(name="JokeTool", func=joke_chain, description="Tells a joke")
]
