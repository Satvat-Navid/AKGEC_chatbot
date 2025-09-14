document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const themeSlider = document.getElementById("theme-slider");
    let isBotThinking = false;

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
        if (isBotThinking) return;

        const query = userInput.value.trim();
        if (!query) return;

        addMessage(query, "user");
        userInput.value = "";
        userInput.style.height = 'auto';

        const lowerCaseQuery = query.toLowerCase();

        const greetingsKeywords = [
            "hello",
            "hi",
            "hey",
            "hey there",
            "hi there",
            "greetings",
            "salutations",
            "howdy",
            "yo",
            "what's up",
            "sup",
            "what's new",
            "how's it going",
            "how are you",
            "good morning",
            "good afternoon",
            "good evening",
            "good day",
            "what's happening",
            "how have you been",
            "long time no see",
            "nice to see you"
        ];
        const thanksKeywords = [
            "thanks",
            "thank you",
            "thx",
            "ty",
            "cheers",
            "thanks a lot",
            "thanks a bunch",
            "thanks a million",
            "thank you so much",
            "many thanks",
            "i appreciate it",
            "much appreciated",
            "i'm grateful",
            "we're grateful",
            "thank you for your help",
            "much obliged",
            "i owe you one",
            "you're the best",
            "you're a lifesaver",
            "i can't thank you enough",
            "my gratitude",
            "that's very kind of you"
        ];
        const farewellKeywords = [
            "bye",
            "goodbye",
            "farewell",
            "see you later",
            "see you soon",
            "see ya",
            "talk to you later",
            "later",
            "catch you later",
            "take care",
            "have a good one",
            "until next time",
            "peace",
            "i'm out",
            "have a great day",
            "have a good night",
            "all the best",
            "bye for now",
            "so long",
            "adios",
            "take it easy",
            "cheerio"
        ];
        
        const thinkingMessage = addMessage("Thinking...", "bot");
        // Object to hold all local keyword-based responses
        const localResponses = {
            greetings: {
                keywords: greetingsKeywords,
                reply: "**Hello!** 👋  \n\nWelcome to **Ajay Kumar Garg Engineering College (AKGEC)**.  \n\n*How can I assist you today?*\n\nYou can ask about:\n\n- 📅 **Seminars & workshops**\n- 📚 **Course details & syllabus**\n- 🗂️ **Research projects & publications**\n- 🏢 **Campus facilities & student services**\n- 🎓 **Admissions, placements, and alumni events** \n\nFeel free to let me know what you need!"
            },
            thanks: {
                keywords: thanksKeywords,
                reply: "**You’re most welcome!**  \n\nIf you need any more information about **AKGEC events**, workshops, *student activities*, or anything else related to the college, just let me know. I’m here to help!"
            },
            farewells: {
                keywords: farewellKeywords,
                reply: "**Bye!**  \n*Thank you for reaching out to Ajay Kumar Garg Engineering College.*  \nIf you have any more queries about **academics, events, or campus facilities**, feel free to ask.  \n\n**Have a great day!** 🎓"
            }
        };

        for (const category in localResponses) {
            if (localResponses[category].keywords.includes(lowerCaseQuery)) {
                const reply = localResponses[category].reply;
                setTimeout(() => {
                    // addMessage(reply, "bot");
                    thinkingMessage.querySelector("p").innerHTML = marked.parse(reply);
                    thinkingMessage.classList.remove("loading");
                }, 1500); // Short delay for a natural feel
                return; // Stop the function to prevent the API call
            }
        }
        
        try {
            // SET STATE TO THINKING AND DISABLE INPUTS
            isBotThinking = true;
            userInput.disabled = true;
            sendBtn.disabled = true;
            
            const botResponse = await getBotResponse(query);
            
            // Update the "Thinking..." message with the actual response
            thinkingMessage.querySelector("p").innerHTML = marked.parse(botResponse);
            thinkingMessage.classList.remove("loading");            
        } catch (error) {
            thinkingMessage.querySelector("p").textContent = "Oops! Something went wrong. Please try again.";
            thinkingMessage.classList.remove("loading");
            console.error("API Error:", error);
        } finally {
        // ALWAYS RE-ENABLE INPUTS AFTER RESPONSE OR ERROR
        isBotThinking = false;
        userInput.disabled = false;
        sendBtn.disabled = false;
        // userInput.focus(); // Optional: focus back on the input field
    }

    };

    let history = "";
    // This is the function that calls your FastAPI backend
    const getBotResponse = async (message) => {
        
        try {
            // const response = await fetch("/api/chat", {
            const response = await fetch("/api/chat", {
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