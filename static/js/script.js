document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const recordButton = document.getElementById('recordButton');
    
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    
    // Add a welcome message
    addBotMessage('നമസ്കാരം! എനിക്ക് സഹായിക്കാൻ കഴിയുമോ?');
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Record audio button
    recordButton.addEventListener('click', toggleRecording);
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            userInput.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: message })
                });
                
                const data = await response.json();
                if (data.response) {
                    addBotMessage(data.response);
                } else {
                    addBotMessage('ക്ഷമിക്കണം, എനിക്ക് ഉത്തരം നൽകാൻ കഴിയില്ല.');
                }
            } catch (error) {
                console.error('Error:', error);
                addBotMessage('ക്ഷമിക്കണം, ഒരു പിശക് സംഭവിച്ചു. പിന്നീട് ശ്രമിക്കുക.');
            }
        }
    }
    
    async function toggleRecording() {
        if (isRecording) {
            stopRecording();
        } else {
            await startRecording();
        }
    }
    
    async function startRecording() {
        try {
            audioChunks = [];
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await sendAudio(audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };
            
            mediaRecorder.start();
            isRecording = true;
            recordButton.classList.add('recording');
            addUserMessage('റെക്കോർഡിംഗ് ആരംഭിച്ചു...');
        } catch (error) {
            console.error('Error starting recording:', error);
            addBotMessage('ഓഡിയോ റെക്കോർഡിംഗ് പിശക്. മൈക്രോഫോൺ പ്രവർത്തിക്കുന്നുണ്ടോ എന്ന് പരിശോധിക്കുക.');
        }
    }
    
    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            isRecording = false;
            recordButton.classList.remove('recording');
            addUserMessage('റെക്കോർഡിംഗ് നിർത്തി...');
        }
    }
    
    async function sendAudio(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.response) {
                addBotMessage(data.response);
            } else if (data.error) {
                addBotMessage(data.error);
            } else {
                addBotMessage('ക്ഷമിക്കണം, എനിക്ക് ഓഡിയോ മനസ്സിലാക്കാൻ കഴിഞ്ഞില്ല.');
            }
        } catch (error) {
            console.error('Error:', error);
            addBotMessage('ക്ഷമിക്കണം, ഒരു പിശക് സംഭവിച്ചു. പിന്നീട് ശ്രമിക്കുക.');
        }
    }
    
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user-message');
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot-message');
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});