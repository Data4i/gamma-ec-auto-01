from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from ChainWorkflow.utils.prompt import prompt
from ChainWorkflow.utils.parser import parser
from ChainWorkflow.utils.model import llm
from ChainWorkflow.utils.runnable_functions import send_cold_email, send_cold_call, get_advise


prompt_template = PromptTemplate(
    template=prompt,
    input_variables=["company_name", "industry", "engagement_level", "objection"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

first_chain = prompt_template | llm | parser

cold_email_runnable = RunnableLambda(send_cold_email)
cold_call_runnable = RunnableLambda(send_cold_call)
get_advise_runnable = RunnableLambda(get_advise)

email_and_call_chain = RunnableParallel(
    email_status=cold_email_runnable,  
    call_status=cold_call_runnable,  
    advise_status=get_advise_runnable  
)

full_chain = first_chain | email_and_call_chain

