$(document).ready(function () {

    // ✅ Display Siri response as animated message
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        if (message.trim() === "") return;  // ✅ Prevent empty message flicker
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // ✅ Show idle assistant UI
    eel.expose(ShowHood);
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
        ()=>{
            document.getElementsByClassName('.siri-message').innerText("hello I'm Jarvis");
        }

        

    }

    // ✅ Show sender's chat bubble
    eel.expose(senderText);
    function senderText(message) {
        if (message.trim() === "") return;

        const chatBox = document.getElementById("chat-canvas-body");
        chatBox.innerHTML += `
            <div class="row justify-content-end mb-4">
                <div class="width-size">
                    <div class="sender_message">${escapeHtml(message)}</div>
                </div>
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // ✅ Show assistant's reply bubble
    eel.expose(receiverText);
    function receiverText(message) {
        if (message.trim() === "") return;

        const chatBox = document.getElementById("chat-canvas-body");
        chatBox.innerHTML += `
            <div class="row justify-content-start mb-4">
                <div class="width-size">
                    <div class="receiver_message">${escapeHtml(message)}</div>
                </div>
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // ✅ Escape HTML to prevent injection
    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\"/g, "&quot;")
            .replace(/\'/g, "&#039;");
    }

});
