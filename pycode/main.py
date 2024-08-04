from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv  
import argparse
import os
import sys
import json

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--language', type=str, default='Python')
parser.add_argument('--task', type=str, default='determine value of pi to ten decimal places')
args=parser.parse_args()

llm = OpenAI()

#  Prompts

code_prompt = PromptTemplate(
    template="Write a short {language} function that will {task}.",
    input_variables=["language", "task"]
    )

test_prompt = PromptTemplate(
    template="Write a test for the following {language} code:\n{code}",
    input_variables=["language", "task"]
    )

# Chains

code_chain = LLMChain(
    llm=llm, 
    prompt=code_prompt,
    output_key="code"
    )   

test_chain = LLMChain(
    llm=llm, 
    prompt=test_prompt,
    output_key="test"
    )

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["language", "task"],
    output_variables=["code", "test"]
    )

result = chain({
    "language": args.language, 
    "task": args.task
    })

# result = code_chain({
#     "language": args.language, 
#     "task": args.task
#     })

print(">>>>>>>>GENERATED CODE<<<<<<<<")
print(result["code"])
print(">>>>>>>>GENERATED TEST<<<<<<<<")
print(result["test"])
 
