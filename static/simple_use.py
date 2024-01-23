from autogen import AssistantAgent, UserProxyAgent
from typing import Literal
from pydantic import BaseModel, Field
from typing_extensions import Annotated
import autogen



config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k"],
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}


# create an AssistantAgent instance named "assistant"
finance_agent = AssistantAgent(
    name="finance_agent",
    system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
)

CurrencySymbol = Literal["USD", "EUR"]


def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.1
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")

# NOTE: for Azure OpenAI, please use API version 2023-12-01-preview or later as
# support for earlier versions will be deprecated.
# For API versions 2023-10-01-preview or earlier you may
# need to set `api_style="function"` in the decorator if the default value does not work:
# `register_for_llm(description=..., api_style="function")`.
@user_proxy.register_for_execution()
@finance_agent.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
    base_amount: Annotated[float, "Amount of currency in base_currency"],
    base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
    quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
    return f"{quote_amount} {quote_currency}"

schema = finance_agent.llm_config["tools"]

# print(schema)

response = user_proxy.initiate_chat(
    finance_agent,
    message="How much is 2000 USD in EUR?",
)
