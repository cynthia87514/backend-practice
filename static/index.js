fetchMessages();

document.getElementById("messageForm").addEventListener("submit", async function(event){
    event.preventDefault();
    document.getElementById("uploadingMessage").style.display = "block";
    const formData = new FormData(event.target);
    await fetchSubmitForm(formData);
    document.getElementById("uploadingMessage").style.display = "none";
})

// Function Part //
async function fetchMessages(){
    try{
        document.getElementById("loadingMessage").style.display = "block";
        const response = await fetch("/api/messages");
        const messages = await response.json();
        renderMessages(messages);
    }catch(error){
        console.error("Error:", error);
    }finally{
        document.getElementById("loadingMessage").style.display = "none";
        document.getElementById("messageContainer").style.display = "block";
    }
}

function renderMessages(messages) {
    const messageContainer = document.getElementById("messageContainer");
    messageContainer.innerHTML = "";

    messages.forEach(message => {
        const messageElement = `
            <div class="message">
                <div class="messageText">${message.message}</div>
                <img src="${message.image}" alt="Uploaded image" class="messageImg">
                <div class="footer">
                    <button class="deleteButton" onclick="deleteMessage(${message.id})">
                        <img src="/static/images/delete.png" alt="Delete" class="deleteIcon">
                    </button>
                    <div class="messageTime">${new Date(message.created_at).toLocaleString("zh-TW", { 
                        timeZone: "Asia/Taipei",
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                        hour12: false
                    })}</div>
                </div>
            </div>
        `;
        messageContainer.insertAdjacentHTML("beforeend", messageElement);
    });
}

async function fetchSubmitForm(formData){
    try{
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        if (result.ok){
            alert("成功留言囉");
            // 成功留言後清空留言表單
            document.getElementById("messageForm").reset();
            // 成功留言後將留言新增到畫面中
            fetchMessages();
        }else{
            alert("留言失敗了，請再試一次");
        }
    }catch(error){
        console.error("Error:", error);
        alert("上傳留言時發生錯誤");
    };
}

async function deleteMessage(messageId){
    if (confirm("確定要刪除這則留言嗎？")){
        try{
            const response = await fetch(`/api/messages/${messageId}`,{
                method: "DELETE",
            });

            const result = await response.json();
            if (result.ok){
                alert("留言刪除成功");
                // 成功刪除後刷新留言列表
                fetchMessages();
            }else{
                alert("留言刪除失敗，請再試一次");
            }
        }catch(error){
            console.error("Error:", error);
            alert("刪除留言時發生錯誤");
        }
    }
}