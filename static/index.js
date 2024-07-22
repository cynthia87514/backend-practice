document.getElementById("messageForm").addEventListener("submit", async function(event){
    event.preventDefault();
    const formData = new FormData(event.target);
    const jsonData = await formToJSON(formData);
    await fetchSubmitForm(jsonData);
})

async function formToJSON(formData){
    const jsonObject = {};
    formData.forEach((value, key) => {
        jsonObject[key] = value;
    });
    return JSON.stringify(jsonObject);
}

async function fetchSubmitForm(jsonData){
    try{
        const response = await fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: jsonData,
        });

        const result = await response.json();
        if (result.success){
            alert("Message submitted successfully!");
        }else{
            alert("Failed to submit message.");
        }
    }catch(error){
        console.error("Error:", error);
        alert("Error submitting message.");
    };
}