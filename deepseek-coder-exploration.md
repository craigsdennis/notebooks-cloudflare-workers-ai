## Exploring Code Generation Using DeepSeek Coder

AI Models being able to generate code unlocks all sorts of use cases. The [DeepSeek Coder](https://github.com/deepseek-ai/DeepSeek-Coder) models `@hf/thebloke/deepseek-coder-6.7b-base-awq` and `@hf/thebloke/deepseek-coder-6.7b-instruct-awq` are now available on [Workers AI](/workers-ai).

Let's explore them using the API!


```python
import sys
!{sys.executable} -m pip install python-dotenv
!{sys.executable} -m pip install --pre cloudflare
```

    Requirement already satisfied: python-dotenv in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (1.0.1)
    Requirement already satisfied: cloudflare in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (3.0.0b7)
    Requirement already satisfied: anyio<5,>=3.5.0 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from cloudflare) (4.3.0)
    Requirement already satisfied: distro<2,>=1.7.0 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from cloudflare) (1.9.0)
    Requirement already satisfied: httpx<1,>=0.23.0 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from cloudflare) (0.27.0)
    Requirement already satisfied: pydantic<3,>=1.9.0 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from cloudflare) (2.7.0)
    Requirement already satisfied: sniffio in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from cloudflare) (1.3.1)
    Requirement already satisfied: typing-extensions<5,>=4.7 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from cloudflare) (4.11.0)
    Requirement already satisfied: idna>=2.8 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from anyio<5,>=3.5.0->cloudflare) (3.6)
    Requirement already satisfied: certifi in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from httpx<1,>=0.23.0->cloudflare) (2024.2.2)
    Requirement already satisfied: httpcore==1.* in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from httpx<1,>=0.23.0->cloudflare) (1.0.4)
    Requirement already satisfied: h11<0.15,>=0.13 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from httpcore==1.*->httpx<1,>=0.23.0->cloudflare) (0.14.0)
    Requirement already satisfied: annotated-types>=0.4.0 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from pydantic<3,>=1.9.0->cloudflare) (0.6.0)
    Requirement already satisfied: pydantic-core==2.18.1 in /Users/craig/Code/scratch/test-unum-over-bias/venv/lib/python3.12/site-packages (from pydantic<3,>=1.9.0->cloudflare) (2.18.1)



```python
import os
from getpass import getpass

from IPython.display import display, Image, Markdown, Audio
from cloudflare import Cloudflare
```


```python
%load_ext dotenv
%dotenv
```

### Configuring your environment

To use the API you'll need your [Cloudflare Account ID](https://dash.cloudflare.com). Head to AI > Workers AI page and press the "Use REST API". This page will let you create a new API Token and copy your Account ID.

If you want to add these values to your environment variables, you can **create a new file** named `.env` and this notebook will read those values.

```bash
CLOUDFLARE_API_TOKEN="YOUR-TOKEN"
CLOUDFLARE_ACCOUNT_ID="YOUR-ACCOUNT-ID"
```

Otherwise you can just enter the values securely when prompted below.


```python
if "CLOUDFLARE_API_TOKEN" in os.environ:
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]
else:
    api_token = getpass("Enter you Cloudflare API Token")
```


```python
if "CLOUDFLARE_ACCOUNT_ID" in os.environ:
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
else:
    account_id = getpass("Enter your account id")
```


```python
client = Cloudflare(api_token=api_token)
```

### Generate code from a comment

A common use case is to complete the code for the user after they provide a descriptive comment.


```python
prompt = "# A function that checks if a given word is a palindrome"

result = client.workers.ai.run(
    "@hf/thebloke/deepseek-coder-6.7b-base-awq",
    account_id=account_id,
    messages=[
        {"role": "user", "content": prompt}
    ]
)
code = result["response"]

display(Markdown(f"""
    ```python
    {prompt}
    {code.strip()}
    ```
"""))
```



```python
# A function that checks if a given word is a palindrome
def is_palindrome(word):
    # Convert the word to lowercase
    word = word.lower()

    # Reverse the word
    reversed_word = word[::-1]

    # Check if the reversed word is the same as the original word
    if word == reversed_word:
        return True
    else:
        return False

# Test the function
print(is_palindrome("racecar"))  # Output: True
print(is_palindrome("hello"))    # Output: False
```



### Assist in debugging

We've all been there, bugs happen. Sometimes those stacktraces can be very intimidating, and a great use case of using Code Generation is to assist in explaining the problem.


```python
model = "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"

system_message = """
The user is going to give you code that isn't working. 
Explain to the user what might be wrong
"""

code = """# Welcomes our user
def hello_world(first_name="World"):
    print(f"Hello, {name}!")
"""

result = client.workers.ai.run(
    "@hf/thebloke/deepseek-coder-6.7b-instruct-awq",
    account_id=account_id,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": code},
    ]
)

display(Markdown(result["response"]))
```


The error in your code is that you are trying to use a variable `name` which is not defined anywhere in your function. The correct variable to use is `first_name`. So, you should change `f"Hello, {name}!"` to `f"Hello, {first_name}!"`.

Here is the corrected code:

```python
# Welcomes our user
def hello_world(first_name="World"):
    print(f"Hello, {first_name}")
```

This function will print "Hello, World" if no arguments are passed to it, or "Hello, [User's Name]" if a string argument is passed.

For example:

```python
hello_world()
```

Output:

```
Hello, World
```

And:

```python
hello_world("John")
```

Output:

```
Hello, John
```















































### Write tests!

Writing unit tests is a common best practice. With the enough context, it's possible to write unit tests.


```python
model = "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"

system_message = "The user is going to give you code and would like to have tests written in the Python unittest module."

code = """
class User:

    def __init__(self, first_name, last_name=None):
        self.first_name = first_name
        self.last_name = last_name
        if last_name is None:
            self.last_name = "Mc" + self.first_name

    def full_name(self):
        return self.first_name + " " + self.last_name
"""

result = client.workers.ai.run(
    "@hf/thebloke/deepseek-coder-6.7b-instruct-awq",
    account_id=account_id,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": code},
    ]
)
display(Markdown(result["response"]))
```



Here is a simple unittest test case for the User class:

```python
import unittest

class TestUser(unittest.TestCase):

    def test_full_name(self):
        user = User("John", "Doe")
        self.assertEqual(user.full_name(), "John Doe")

    def test_default_last_name(self):
        user = User("Jane")
        self.assertEqual(user.full_name(), "Jane McJane")

if __name__ == '__main__':
    unittest.main()
```

In this test case, we have two tests:

- `test_full_name` tests the `full_name` method when the user has both a first name and a last name.
- `test_default_last_name` tests the `full_name` method when the user only has a first name and the last name is set to "Mc" + first name by default.

You can run these tests by executing the script. If everything is working correctly, you should see output indicating that both tests passed.



### Fill-in-the-middle Code Completion

A common use case in Developer Tools is to autocomplete based on context. DeepSeek Coder provides the ability to submit existing code with a placeholder, so that the model can complete in context.

Warning: The tokens are prefixed with `<｜` and suffixed with `｜>` make sure to copy and paste them.


```python
model = "@hf/thebloke/deepseek-coder-6.7b-base-awq"

code = """
<｜fim▁begin｜>import re

from jklol import email_service

def send_email(email_address, body):
    <｜fim▁hole｜>
    if not is_valid_email:
        raise InvalidEmailAddress(email_address)
    return email_service.send(email_address, body)<｜fim▁end｜>
"""

result = client.workers.ai.run(
    "@hf/thebloke/deepseek-coder-6.7b-base-awq",
    account_id=account_id,
    messages=[
        {"role": "user", "content": code}
    ]
)

display(Markdown(f"""
    ```python
    {result["response"].strip()}
    ```
"""))

```



```python
is_valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", email_address)
```



### Experimental: Extract data into JSON

No need to threaten the model or bring grandma into the prompt. Get back JSON in the format you want.


```python
model = "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"

# Learn more at https://json-schema.org/
json_schema = """
{
  "title": "User",
  "description": "A user from our example app",
  "type": "object",
  "properties": {
    "firstName": {
      "description": "The user's first name",
      "type": "string"
    },
    "lastName": {
      "description": "The user's last name",
      "type": "string"
    },
    "numKids": {
      "description": "Amount of children the user has currently",
      "type": "integer"
    },
    "interests": {
      "description": "A list of what the user has shown interest in",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
  },
  "required": [ "firstName" ]
}
"""

system_prompt = f"""
The user is going to discuss themselves and you should create a JSON object from their description to match the json schema below. 

<BEGIN JSON SCHEMA>
{json_schema}
<END JSON SCHEMA>

Return JSON only. Do not explain or provide usage examples.
"""

prompt = """Hey there, I'm Craig Dennis and I'm a Developer Educator at Cloudflare. My email is craig@cloudflare.com. 
            I am very interested in AI. I've got two kids. I love tacos, burritos, and all things Cloudflare"""

result = client.workers.ai.run(
    "@hf/thebloke/deepseek-coder-6.7b-instruct-awq",
    account_id=account_id,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)
display(Markdown(f"""
    ```json
    {result["response"].strip()}
    ```
"""))
```



```json
{
  "firstName": "Craig",
  "lastName": "Dennis",
  "numKids": 2,
  "interests": ["AI", "Cloudflare", "Tacos", "Burritos"]
}
```


