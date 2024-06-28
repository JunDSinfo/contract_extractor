from utilities import extract_json,validate_json_with_model,model_to_json,json_to_pydantic
from pydantic import BaseModel


class TermBase(BaseModel):
    term: str
    amount: str
    condition: str


class TaskBase(BaseModel):
    task: str
    location: str
    note: str


json_term_model = model_to_json(TermBase(term='',
                                    amount = "USD 2,500",
                                    condition = ''

))
json_task_model = model_to_json(TaskBase(task='',
                                    location = '',
                                    note = ''
                                  ))
contractor_prompt = f"""
               You are an expert in understanding invoices.
               You will receive input docs as invoices &
               you will have to answer questions based on the input docs
               You will be provided with a contract text containing various terms and constraints for work execution (e.g., budget constraints, types of allowable work, etc.).
               Your task is to extract all key terms from the contract and structure them in a JSON format. 
               Terms may be related to different sections and subsections of the contract, which should be reflected in your JSON.
               Please provide a response in a structured JSON format that matches the following model: {json_term_model}

               """

task_prompt = f"""
               You are an expert in understanding tasks.
               You will receive a list of task&
               you will have to answer questions based on the input docs
               You will be provided with a contract text containing various terms and constraints for work execution (e.g., budget constraints, types of allowable work, etc.).
               Your task is to extract all key terms from the contract and structure them in a JSON format.
               Please provide a response in a structured JSON format that matches the following model: {json_task_model}

               """

learning_prompt = [
    " Your role is to evaluate and recompute the budget given by the condition term for the business task. Someone will tell you their task, or you can ask them their task,  and then you should respond with a really clever budget",

    "input: An urgent business requirement necessitates travel to New York City over New Year’s weekend, with flight booking required on a Friday night. The base approved travel budget is $2,500",
    "output: Night and Weekend Travel Multiplier: 1.1, Seasonal and Location Adjustment for New York during New Year: 1.2, Urgency Multiplier for last-minute booking: 1.3. The total allowable expense for this travel scenario would be $2,500 * 1.1 * 1.2 * 1.3 = $4,158",

    "input: Trade show participation in Florida during hurricane season",
    "output: Weather and Environmental Considerations: $300. The total allowable expense for this travel scenario would be $2,500 + $300 = $2,800",
    "input: Negotiation meeting in high-risk area in Middle East (urgent)",
    "output: Urgency Multiplier for last-minute booking: 1.3. Weather and Environmental Considerations: $300. The total allowable expense for this travel scenario would be $2,500*1.3 + $300*1.3 = $3,640",
    "input: Research trip to remote part of Norway (booked last-minute)",
    "output: Urgency Multiplier for last-minute booking: 1.3. The total allowable expense for this travel scenario would be $2,500*1.3 = $3,250",
    "input: Marketing tour across Asia (planned and pre-approved)",
    "output: planned and pre-approved: 1.0. The total allowable expense for this travel scenario would be $9,500",

    "input: Sales training in Dubai during peak tourist season",
    "output:  Seasonal Price Fluctuation: 1.1. The total allowable expense for this travel scenario would be $2,500 * 1.1 = $2,750",
    "input: Field research in Amazon rainforest (urgent and rainy season)",
    "output:  Urgency Multiplier for last-minute booking: 1.3. Weather and Environmental Considerations: $300. The total allowable expense for this travel scenario would be $2,500 * 1.3 + 200*1.3 = $3,640",
    "input: Executive meeting in London during a bank holiday weekend",
    "output:  Night and Weekend Travel Multiplier: 1.1. The total allowable expense for this travel scenario would be $2,500 * 1.1 = $2,750",
    "input: Workshop in Las Vegas during a major conference",
    "output: ",
    ]


