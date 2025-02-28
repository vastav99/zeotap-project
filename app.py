from flask import Flask, request, jsonify, render_template
from indexing import create_index, search_index
import os
import logging
import openai
import time
from dotenv import load_dotenv
from openai.error import OpenAIError, RateLimitError, AuthenticationError, APIError

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Flask app
app = Flask(__name__)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure index exists before starting
if not os.path.exists("indexdir"):
    logging.info("Index directory missing. Creating index...")
    create_index()


@app.route("/")
def home():
    """Serve the chatbot UI."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    Handles user queries.
    1. Searches the index first.
    2. Only queries OpenAI if no results are found.
    """
    user_input = request.json.get("question", "").strip()
    platform = request.json.get("platform", "").strip()

    # Input validation
    if not user_input:
        return jsonify({"answer": [{"content": "Please provide a valid question."}]})
    if not platform:
        return jsonify({"answer": [{"content": "Please specify a platform."}]})


    # Step 1: Search the indexed FAQ data
    logging.info(f"Searching for '{user_input}' on platform '{platform}'.")
    response = search_index(platform, user_input)

    if response:  # If results are found in the index
        logging.info(f"Results found in index: {response}")
        return jsonify({"answer": [{"content": result.get("content", "")} for result in response]})

    # Step 2: Only call OpenAI if no index results are found
    logging.info("No results in the index. Querying OpenAI API.")
    openai_response = ask_openai(user_input)

    return jsonify({"answer": [{"content": openai_response}]})


def ask_openai(question):
    """
    Queries OpenAI API with retries and error handling.
    Stops retrying if the quota is exceeded.
    """
    max_retries = 3
    delay = 5  # Start with a 5-second delay

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}],
                max_tokens=150,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()

        except openai.error.RateLimitError:
            logging.warning(f"Rate limit exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff

        except openai.error.InvalidRequestError as e:
            logging.error(f"Invalid request error: {e}")
            return "The request was invalid. Please check your input."

        except openai.error.AuthenticationError:
            logging.error("Invalid OpenAI API Key. Please check your .env file.")
            return "Invalid OpenAI API Key."

        except openai.error.OpenAIError as e:
            if "insufficient_quota" in str(e):
                logging.error("OpenAI API quota exceeded. Please check your plan.")
                return "⚠️ OpenAI API quota exceeded. Please check your plan or try again later."
            logging.error(f"OpenAI API Error: {e}")
            return "An error occurred while processing your request."

    return "Rate limit exceeded. Please try again later."




@app.route("/create_index", methods=["POST"])
def create_index_route():
    """
    API route to manually trigger index creation.
    """
    try:
        create_index()
        return jsonify({"status": "Index created successfully."})
    except Exception as e:
        logging.error(f"Error creating index: {e}")
        return jsonify({"status": "Error creating index."}), 500


if __name__ == "__main__":
    app.run(debug=True)
