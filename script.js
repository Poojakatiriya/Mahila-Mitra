async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;
    
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    
    // Send message to backend (Flask/Node.js)
    let response = await fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    });
    
    let data = await response.json();
    chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
    
    document.getElementById("user-input").value = "";
}
