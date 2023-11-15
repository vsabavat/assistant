from openai import OpenAI
import time

from prompts import get_grocery_prompt, get_client_prompt 
from grocery import groceries_search

ORG_ID="org-mpBl3ckWJuZARAi2sRkSjz9F"

client = OpenAI(
        organization=ORG_ID,
        )

def find_groceries_from_store(search_terms):
    return groceries_search(search_terms)

# GROCERY_PROMPT.format(items=result['items'])
# models = client.models.list()
# import pdb
# pdb.set_trace()

def create_grocery_assistant():
    agent_prompt = get_grocery_prompt()
    assistant = client.beta.assistants.create(
            name="Indian Grocery Store Assistant",
            instructions="Help with finding groceries to purchase",
            tools=[],
            model="gpt-4"
            )
    return assistant

assistant = create_grocery_assistant()

def check_run(run, thread_id):
    while True:
        run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
                )
        if run.status == "requires_action":
            print("run requires action")
            return None
        if run.status not in ["expired", "completed", "failed", "cancelled"]:
            print("sleeping for 2 seconds...")
            time.sleep(2)
        else:
            print("run is done")
            return run

def display(thread_id):
    messages = client.beta.threads.messages.list(thread_id)
    output = messages.data[0].content[0].text.value
    print(output)
    return output 

def add_message(thread_id, msg_str):
    thread_message = client.beta.threads.messages.create(thread_id, role="user", content=msg_str)

def run_main():

    while True:
        print("Assistant: What would you like to buy? Enter the grocery item names only")
        user_input = input("User: ")

        result = find_groceries_from_store(user_input)

        thread_prompt = get_client_prompt(result) 

        thread = client.beta.threads.create()

        thread_message = client.beta.threads.messages.create(
          thread.id,
          role="user",
          content=f"{user_input}",
        )

        run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
                instructions=f"{thread_prompt}"
                )

        while True:
            check_run(run, thread.id)
            output = display(thread.id)
            if "done" in output:
                break
            user_input = input("User: ")
            add_message(thread.id, user_input)
            run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=assistant.id,
                    instructions=f"{thread_prompt}"
                    )

if __name__ == "__main__":
    run_main()
