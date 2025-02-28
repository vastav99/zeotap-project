document.addEventListener("DOMContentLoaded", () => {
    const chatBody = document.getElementById("chat-body");
    const userInput = document.getElementById("user-question");
    const platformSelect = document.getElementById("platform");
    const themeToggle = document.getElementById("theme-toggle");

    // Toggle Dark Mode
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        themeToggle.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    });

    // Send message when pressing Enter
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
            event.preventDefault(); // Prevents accidental form submission
        }
    });

    window.sendMessage = async function () {
        const question = userInput.value.trim();
        const platform = platformSelect.value;
    
        if (!question) {
            appendMessage("Please enter a question!", "error-message");
            return;
        }
    
        appendMessage(question, "user-message");
        userInput.value = ""; // Clears input box immediately after sending
        appendMessage("Thinking...", "bot-message", true);
    
        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question, platform })
            });
    
            const data = await response.json();
            console.log("API Response:", data); // Debugging: Log API response
    
            document.querySelector(".loading").remove();
    
            if (data.answer && data.answer.length > 0) {
                const reply = data.answer[0].content;
                if (reply.includes("quota exceeded")) {
                    appendMessage("⚠️ OpenAI API quota exceeded. Try again later.", "error-message");
                } else {
                    appendMessage(reply, "bot-message");
                }
            } else {
                appendMessage("No answer found.", "error-message");
            }
        } catch (error) {
            document.querySelector(".loading").remove();
            console.error("Error fetching response:", error);
            appendMessage("Error: Unable to connect. Try again later.", "error-message");
        }
    };
    
    
    function appendMessage(text, className, isLoading = false) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(className);
        if (isLoading) messageDiv.classList.add("loading");

        messageDiv.textContent = text;
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
});
