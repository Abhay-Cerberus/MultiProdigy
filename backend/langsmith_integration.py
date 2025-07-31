from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

def run_chain(user_input: str):
    prompt = PromptTemplate(
        input_variables=["input"],
        template="Answer this question: {input}",
    )
    llm = OpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_input)
