// Bal Sadan Floating Mitra AI Assistant
document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("toggleAiChatBtn");
    const chatWindow = document.getElementById("aiChatWindow");
    const closeBtn = document.getElementById("closeAiChatBtn");
    const chatForm = document.getElementById("aiChatForm");
    const userInput = document.getElementById("aiUserInput");
    const chatMessages = document.getElementById("aiChatMessages");

    if (!toggleBtn || !chatWindow) return;

    // Toggle Chat Window
    toggleBtn.addEventListener("click", function() {
        chatWindow.classList.toggle("d-none");
        if (!chatWindow.classList.contains("d-none")) {
            userInput.focus();
        }
    });

    closeBtn.addEventListener("click", function() {
        chatWindow.classList.add("d-none");
    });

    // Handle Quick Query Pills
    document.querySelectorAll(".quick-query-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const query = this.getAttribute("data-query");
            sendQuery(query);
        });
    });

    // Handle Form Submit
    chatForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;
        sendQuery(query);
    });

    function sendQuery(query) {
        // Render user message
        appendBubble("outgoing", query);
        userInput.value = "";

        // Render typing loader
        const loaderId = "loader-" + Date.now();
        const loaderDiv = document.createElement("div");
        loaderDiv.id = loaderId;
        loaderDiv.className = "ai-bubble incoming mb-2 text-muted small";
        loaderDiv.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin me-1 text-primary"></i> Mitra is thinking...';
        chatMessages.appendChild(loaderDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        fetch("/api/ai/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        })
        .then(res => res.json())
        .then(data => {
            const loader = document.getElementById(loaderId);
            if (loader) loader.remove();
            
            // Format markdown to HTML (basic bold, links, bullets)
            let formatted = formatText(data.reply);
            appendBubble("incoming", formatted);
        })
        .catch(err => {
            const loader = document.getElementById(loaderId);
            if (loader) loader.remove();
            appendBubble("incoming", "Thank you for reaching out to Sir Kasturchand Daga Bal Sadan. Please contact our Lakad Ganj office at 077095 58334.");
        });
    }

    function appendBubble(type, htmlContent) {
        const div = document.createElement("div");
        div.className = `ai-bubble ${type} mb-2 ${type === 'outgoing' ? 'ms-auto text-white' : ''}`;
        div.innerHTML = htmlContent;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function formatText(text) {
        if (!text) return "";
        let escaped = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/•\s/g, '<span class="text-primary me-1">•</span>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="text-primary text-decoration-underline" target="_blank">$1</a>')
            .replace(/\n/g, '<br>');
        return escaped;
    }
});
