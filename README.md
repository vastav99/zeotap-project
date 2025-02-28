# Support Agent Chatbot for CDP

## Overview
This project is a Support Agent Chatbot designed to assist with "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot leverages official documentation from these platforms to provide accurate and context-aware responses to user queries. The application is built using Python and Flask, with additional libraries for natural language processing (NLP) and document indexing.

## Live Project Link
You can access the live version of the project [here](https://support-agent-chatbot-for-cdp.onrender.com/).

## Core Functionalities
1. **Answer "How-to" Questions**:
   - The chatbot can understand and respond to user questions about how to perform specific tasks or use features within each CDP.
   - Example questions:
     - "How do I set up a new source in Segment?"
     - "How can I create a user profile in mParticle?"
     - "How do I build an audience segment in Lytics?"
     - "How can I integrate my data with Zeotap?"

2. **Extract Information from Documentation**:
   - The chatbot retrieves relevant information from the provided documentation to answer user questions.
   - It navigates through the documentation, identifies relevant sections, and extracts the necessary instructions or steps.

3. **Handle Variations in Questions**:
   - The chatbot can handle variations in question phrasing and terminology.
   - It can manage extremely long questions without breaking them down and ignore irrelevant questions.

### Bonus Features
- **Cross-CDP Comparisons**:
  - The chatbot can answer questions about the differences in approaches or functionalities between the four CDPs.
  - Example question: "How does Segment's audience creation process compare to Lytics'?"

- **Advanced "How-to" Questions**:
  - The chatbot handles more complex or platform-specific "how-to" questions.
  - It provides guidance on advanced configurations, integrations, or use cases.

## Data Structures
### Index Directory
The index directory stores indexed data for fast search and retrieval. The indexing is handled by the `whoosh` library, which provides efficient search capabilities.

### Flask Application
The core application structure is built using the Flask framework. Flask provides a simple and flexible structure for building web applications and APIs.

### JSON Objects
JSON is used for communication between the frontend and backend, especially for sending user queries and receiving responses.

## Tech Stack
### Python
The primary programming language used for the project. Python is chosen for its simplicity, readability, and extensive libraries that support web development, machine learning, and data processing.

### Flask (2.0.1)
A lightweight web framework for Python. Flask is used for building the web application and API endpoints. It is chosen for its simplicity, flexibility, and strong community support.

### flask-cors (3.0.10)
A Flask extension to handle Cross-Origin Resource Sharing (CORS). It allows the web application to communicate with the backend server from different origins, which is essential for frontend-backend integration.

### openai (0.28)
A library to interact with OpenAI's API. This library is used to integrate the chatbot functionality, allowing the application to generate responses using OpenAI's language model.

### python-dotenv (0.19.2)
A library to load environment variables from a `.env` file. This is used for managing configuration settings securely and conveniently.

### werkzeug (2.0.3)
A comprehensive WSGI web application library. It is one of the dependencies of Flask and provides utilities for request handling and response creation.

### whoosh (2.7.4)
A fast, featureful full-text indexing and searching library implemented in pure Python. It is used for implementing search functionality within the application.

### beautifulsoup4 (4.11.1)
A library for parsing HTML and XML documents. It is useful for web scraping and extracting data from web pages.

## Explanation of Choice
- **Python**: Chosen for its versatility, ease of use, and extensive libraries that facilitate rapid development and integration with various services.
- **Flask**: Selected for its minimalistic approach, allowing developers to build web applications quickly without imposing a specific project structure or dependencies.
- **openai**: Integrated to leverage the powerful capabilities of OpenAI's language model for generating chatbot responses, enhancing the user experience.
- **whoosh**: Utilized for its efficient and easy-to-use full-text search capabilities, providing fast and accurate search results within the application.

## Getting Started
To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Suhassuresha/Support-Agent-Chatbot-for-CDP.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Support-Agent-Chatbot-for-CDP
    ```

3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up the environment variables by creating a `.env` file:
    ```dotenv
    OPENAI_API_KEY=your_openai_api_key
    ```

6. Run the Flask application:
    ```bash
    python app.py
    ```

7. Open your browser and navigate to `http://127.0.0.1:5000` to access the chatbot.

## Examples of Usage
### Asking a Question
To ask a question using the chatbot, send a POST request to the `/ask` endpoint with the following JSON payload:
```json
{
    "question": "How do I set up a new source in Segment?",
    "platform": "Segment"
}
```

Example using `curl`:
```bash
curl -X POST http://127.0.0.1:5000/ask -H "Content-Type: application/json" -d '{"question": "How do I set up a new source in Segment?", "platform": "Segment"}'
```

### Creating an Index
To manually trigger the creation of an index, send a POST request to the `/create_index` endpoint:
```json
{}
```

Example using `curl`:
```bash
curl -X POST http://127.0.0.1:5000/create_index -H "Content-Type: application/json" -d '{}'
```

## Limitations
### OpenAI API Retrieval Limitations
- **Rate Limits**: OpenAI's API has rate limits that may restrict the number of requests you can make within a certain timeframe. Ensure you handle rate limit errors gracefully.
- **Response Time**: The response time from OpenAI's API may vary depending on the load on their servers. Implement retries with exponential backoff to handle transient errors.
- **Cost**: Using OpenAI's API incurs costs based on the number of requests and the amount of data processed. Monitor your usage to avoid unexpected expenses.
- **Data Privacy**: Ensure that sensitive data is not sent to OpenAI's API, as the data will be processed by their servers.

## Contributing
If you would like to contribute to the project, please fork the repository and submit a pull request with your changes. Make sure to follow the coding standards and include appropriate tests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Data Sources
- Segment Documentation: [https://segment.com/docs/?ref=nav](https://segment.com/docs/?ref=nav)
- mParticle Documentation: [https://docs.mparticle.com/](https://docs.mparticle.com/)
- Lytics Documentation: [https://docs.lytics.com/](https://docs.lytics.com/)
- Zeotap Documentation: [https://docs.zeotap.com/home/en-us/](https://docs.zeotap.com/home/en-us/)