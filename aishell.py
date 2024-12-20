import requests
import subprocess
import json

# Replace with your local Ollama server endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def query_ollama(user_message):
   
    if not user_message:
        print("No message provided.")
        return None

    # Prepare the payload for the Ollama API
    payload = {
        "model": "llama2",  # use model you like deployed in Ollama
        "prompt": user_message,
    }

    try:
        # Send the request to the Ollama server
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        if response.status_code == 200:
            reply = ""
            for line in response.iter_lines():
                if line:  # Skip empty lines
                    data = json.loads(line.decode("utf-8"))
                    reply += data.get("response", "")
            return reply
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the local Ollama server: {str(e)}")
        return None


def execute_command(command):
    # lets run
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    print("Welcome to the AI-powered Python command shell!")
    print("let me know what would you like me to do starting with #, or give me shell command to execute. Type 'exit' to quit.\n")

    while True:
        # Get user input
        user_input = input("cmd: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break


        if user_input.startswith("#"):
            # AI translate NL to Linux command 
            natural_language = user_input[1:].strip()  # Remove leading '#'
            prompt = f"what is linux command for:\nInput: {natural_language}\nOutput:"
            command = query_ollama(prompt)

            if not command:
                print("Failed to translate the command. Try again.")
                continue

            print(f"Translated Command: {command}")
            confirmation = input("Do you want to execute this command? (y/n): ").strip().lower()
            if confirmation == "y":
                 execute_command(command)
            else:
                 print("Command not executed.")
        else:
            # Direct shell execution
             execute_command(user_input)


if __name__ == "__main__":
    main()
