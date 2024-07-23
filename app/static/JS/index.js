const textInputValue = document.querySelector(".text-input-value")
const fileInputValue = document.querySelector(".file-input-value")
const submitBtn = document.querySelector(".submit-btn")
const boardContainer = document.querySelector(".board-container")

async function sentFetch(url, body){
    // const headers = {
    //   "Content-Type": "application/json",
    //   "Accept": "application/json",
    // }
    const response = await fetch(`${url}`,{
      method:"POST",

      body: body
    })
    let data = await response.json()
    console.log(data)
    return data
}
async function getMessage(body){
  result = await sentFetch( "/api/messages", body)
  return result
}


submitBtn.addEventListener("click", ()=>{
  let textValue = textInputValue.value
  let file = fileInputValue.files[0]
  if(!file || !textValue){
    alert("請留言或上傳圖片")
    return
  }else{
    const formData = new FormData();
    formData.append('file', file);
    formData.append('text', textValue);
    result = getMessage(formData);
  }
  
   
})