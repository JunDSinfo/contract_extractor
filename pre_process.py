from utilities import extract_json,validate_json_with_model,model_to_json,json_to_pydantic
from pydantic import BaseModel


class TermBase(BaseModel):
    term: str
    amount: str
    ratio: str
    condition: str


class TaskBase(BaseModel):
    task: str
    location: str
    note: str


json_term_model = model_to_json(TermBase(term='',
                                    amount = 'USD 2500',
                                    ratio = '10%',
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
               You are an expert in understanding Task. 
               You will receive the input doc and you identify and list the most important keywords or key phrases in the task. 
               These keywords should capture the main task, location, and scenarios.
               Ensure that your keyword extraction results are relevant, concise, and capture the essential topics within the text.
               Please provide a response in a structured JSON format that matches the following model: {json_task_model}"""

learning_prompt = [
    " Your role is to evaluate and recompute the budget given by the condition term for the business task. Someone will tell you their task, or you can ask them their task,  and then you should respond with a really clever budget",

    "input: New York City, New Year’s weekend. The base approved travel budget is $2,500",
    "output: Night and Weekend Travel Multiplier: 1.1, Seasonal and Location Adjustment for New York during New Year: 1.2, Urgency Multiplier for last-minute booking: 1.3. The total allowable expense for this travel scenario would be $2,500 * 1.1 * 1.2 * 1.3 = $4,158",

    "input: hurricane season",
    "output: Weather and Environmental Considerations: $300. The total allowable expense for this travel scenario would be $2,500 + $300 = $2,800",
    "input: high-risk area in Middle East (urgent)",
    "output: Urgency Multiplier for last-minute booking: 1.3. Weather and Environmental Considerations: $300. The total allowable expense for this travel scenario would be $2,500*1.3 + $300*1.3 = $3,640",
    "input: booked last-minute",
    "output: Urgency Multiplier for last-minute booking: 1.3. The total allowable expense for this travel scenario would be $2,500*1.3 = $3,250",
    "input: planned, pre-approved",
    "output: The total allowable expense for this travel scenario is accepted",

    "input: peak tourist season",
    "output:  Seasonal Price Fluctuation: 1.1. The total allowable expense for this travel scenario would be $2,500 * 1.1 = $2,750",
    "input: rainforest (urgent and rainy season)",
    "output:  Urgency Multiplier for last-minute booking: 1.3. Weather and Environmental Considerations: $300. The total allowable expense for this travel scenario would be $2,500 * 1.3 + 200*1.3 = $3,640",
    "input: holiday weekend",
    "output:  Night and Weekend Travel Multiplier: 1.1. The total allowable expense for this travel scenario would be $2,500 * 1.1 = $2,750",
    "input: Workshop in Las Vegas during a major conference",
    "output: ",
    ]


