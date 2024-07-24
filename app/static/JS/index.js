const textInputValue = document.querySelector(".text-input-value")
const fileInputValue = document.querySelector(".file-input-value")
const submitBtn = document.querySelector(".submit-btn")
const boardContainer = document.querySelector(".board-container")
const messageContainer = document.querySelector(".message-container")

function createAndAppendMessageBlock(url, text){
  let messageBlock = document.createElement("div")
  messageBlock.className = "row align-items-start message-block"
  let messageImage = document.createElement("img")
  messageImage.className = "message-image"
  messageImage.src = "https://"+ url
  let messageText = document.createElement("p")
  messageText.innerText = text
  messageText.className = "message-text"
  messageBlock.appendChild(messageImage)
  messageBlock.appendChild(messageText)
  messageContainer.appendChild(messageBlock)
}

function createAndPrependMessageBlock(url, text){
  let messageBlock = document.createElement("div")
  messageBlock.className = "row align-items-start message-block"
  let messageImage = document.createElement("img")
  messageImage.src = "https://"+ url
  let messageText = document.createElement("p")
  messageText.innerText=text
  messageBlock.appendChild(messageImage)
  messageBlock.appendChild(messageText)
  messageContainer.prepend(messageBlock)
}

async function sentFetch(url, body, method){
    // const headers = {
    //   "Content-Type": "application/json",
    //   "Accept": "application/json",
    // }
    const response = await fetch(`${url}`,{
      method:`${method}`,
      body: body
    })
    let data = await response.json()
    console.log(data)
    return data["data"]
    
}

async function renderPostMessageImmediately(url, body, method){
  result = await sentFetch(url, body, method)
  const {image_cdn_url, message} = await result
  createAndPrependMessageBlock(image_cdn_url, message)
}
async function getAllMessage(url, method){
  const headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
  }
  const response = await fetch(`${url}`,{
    headers: headers,
    method:`${method}`,
  })
  let data = await response.json()
  return data["data"]
}
async function renderMessage(){
  messages_raw_data = await getAllMessage("/api/messages","GET")
  for (message of messages_raw_data){
    const {id, text, image_cdn_url} = message
    createAndAppendMessageBlock(image_cdn_url, text)
    console.log(message)
  }
}

window.addEventListener("load", ()=>{
  renderMessage()
})

submitBtn.addEventListener("click", ()=>{
  let textValue = textInputValue.value.toString();
  let file = fileInputValue.files[0];
  if(!file || !textValue){
    alert("請留言或上傳圖片");
    return;
  }else{
    const formData = new FormData();
    formData.append('file', file);
    formData.append('text', textValue);
    renderPostMessageImmediately( "/api/messages", formData, "POST");

  };
  
   
})
