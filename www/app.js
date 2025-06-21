$(document).ready(function () {

    // Animate `.text` using textillate
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });

    // ✅ SiriWave visualizer setup
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: 1,       // ✅ Changed from string to number
        speed: 0.30,        // ✅ Changed from string to number
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },
    });

    // ✅ Microphone button click event
    $("#MicBtn").click(function () {
        eel.playAssistantSound("1");
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();  // ✅ Correct: eel functions must be double-called
    });

    // ✅ Keyboard shortcut: Cmd/Ctrl + J to activate assistant
    function doc_keyUp(e) {
        if (e.key === 'j' && (e.ctrlKey || e.metaKey)) {  // ✅ Cross-platform (Ctrl for Windows/Linux)
            eel.playAssistantSound("1");
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // ✅ Play assistant with typed message
    function PlayAssistant(message) {
        if (message.trim() !== "") {  // ✅ Added trim() to prevent whitespace-only inputs
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // ✅ Toggle mic/send buttons based on text input
    function ShowHideButton(message) {
        if (message.trim().length === 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // ✅ Update button toggle while typing
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // ✅ Send button click handler
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    // ✅ Press Enter to send message
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

});