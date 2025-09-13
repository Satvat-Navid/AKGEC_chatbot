document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const themeSlider = document.getElementById("theme-slider");


    // Function to add a message to the chatbox
    const addMessage = (message, sender) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", sender);
        
        const paragraph = document.createElement("p");

        // Use 'marked' library to render markdown for bot messages
        if (sender === "bot") {
            paragraph.innerHTML = marked.parse(message);
        } else {
            paragraph.textContent = message;
        }
        
        messageElement.appendChild(paragraph);

        if (sender === "bot" && message === "Thinking...") {
            messageElement.classList.add("loading");
        }

        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
        return messageElement;
    };
    
    // Function to handle sending a message
    const handleSendMessage = async () => {
        const query = userInput.value.trim();
        if (!query) return;

        addMessage(query, "user");
        userInput.value = "";
        userInput.style.height = 'auto';

        // Add the user's query to the history before making the API call
        // history.push({ "role": "user", "content": query });

        const thinkingMessage = addMessage("Thinking...", "bot");
        
        try {
            const botResponse = await getBotResponse(query);
            
            // Update the "Thinking..." message with the actual response
            thinkingMessage.querySelector("p").innerHTML = marked.parse(botResponse);
            thinkingMessage.classList.remove("loading");

            // Add the bot's response to the history
            // historyList.push({ "role": "model", "content": botResponse });
            
        } catch (error) {
            thinkingMessage.querySelector("p").textContent = "Oops! Something went wrong. Please try again.";
            thinkingMessage.classList.remove("loading");
            console.error("API Error:", error);
        }
    };

    let history = "";
    // This is the function that calls your FastAPI backend
    const getBotResponse = async (message) => {
        
        // history += `${history ? '\n' : ''}user: ${message}`;
        
        try {
            // const response = await fetch("/api/chat", {
            const response = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: message,
                    history: history, // Pass the formatted string
                }),
            });

            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }

            const data = await response.json();
            console.log(data)
            history = `${data.history ? data.history + '\n' : ''}user: ${message}\n reply: ${data.reply}`;
            return data.reply; // Return the reply from the backend
        } catch (error) {
            console.error("Error in getBotResponse:", error);
            // **FIXED**: Removed calls to undefined functions. Re-throw the error
            // so the outer catch block in handleSendMessage can display the error message.
            throw error; 
        }
    };

    // Event listeners
    sendBtn.addEventListener("click", handleSendMessage);
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    });

    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = `${userInput.scrollHeight}px`;
    });

    themeSlider.addEventListener("change", () => {
        if (themeSlider.checked) {
            document.body.classList.add("dark-theme");
            document.body.classList.remove("light-theme");
        } else {
            document.body.classList.add("light-theme");
            document.body.classList.remove("dark-theme");
        }
    });
});