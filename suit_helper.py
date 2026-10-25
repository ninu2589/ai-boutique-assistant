import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain, SequentialChain


class MissingAPIKeyError(Exception):
    pass


def get_llm():
    # Use GROQ_API_KEY from the environment if set, otherwise fall back to secret_file.py
    if not os.environ.get("GROQ_API_KEY"):
        try:
            from secret_file import API_KEY
        except ImportError:
            API_KEY = None
        if not API_KEY:
            raise MissingAPIKeyError("Set GROQ_API_KEY or add API_KEY to secret_file.py")
        os.environ["GROQ_API_KEY"] = API_KEY

    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.4)


def show_suit_and_saree_types(location):
    llm = get_llm()

    # Chain 1: location -> store_names
    prompt_template_name = PromptTemplate(
        input_variables=["location"],
        template=(
            "Suggest 5 well-known affordable ethnic shops in {location}, India that are popular for buying "
            "ladies' suits and sarees. Give only the names as a numbered list."
        ),
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="store_names")

    # Chain 2: store_names -> suit_types
    prompt_template_types = PromptTemplate(
        input_variables=["store_names"],
        template=(
            "For each of these stores, list the different types of suits and sarees available "
            "(for example fabric, style and occasion):\n{store_names}"
        ),
    )
    types_chain = LLMChain(llm=llm, prompt=prompt_template_types, output_key="suit_types")

    chain = SequentialChain(
        chains=[name_chain, types_chain],
        input_variables=["location"],
        output_variables=["store_names", "suit_types"],
    )

    return chain.invoke({"location": location})
