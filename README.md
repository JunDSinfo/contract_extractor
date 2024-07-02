Contract-Extractor

This task aims to assess the candidate’s ability to effectively use language models to analyze complex text documents and apply extracted information for automation tasks.

The structure of solutions is

1. model.py: This file contains the LLM using the Google Gemini
make sure that you have the ```GOOGLE_API_KEY``` and save it in the 
.env file 

2. pre_process.py: This file contains the pre-process steps:
   + The prompt of term extraction
   + The prompt of task extraction
   + The prompt of audit analysis

3. utils.py: This file contains the utility functions such as:
   + json processing
   + regex processing
4. main.py: This file is the main file which contains the ```streamlit app```
where you can call all the functions for the process step by step

Note: because you might use the free GOOGLE_API_KEY, the time response will be long,
please wait....to avoid of the limited request problem, the code is added some ```sleep``` functions



1. Clone the code to your PC
```git clone https://github.com/JunDSinfo/contract_extractor.git ```
check out the ```develop branch```
```git checkout develop```
2. Install all the dependencies
```pip install -r requirements.txt```
3. Run the script
```streamlit run main.py```
