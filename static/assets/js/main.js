const nav  =document.querySelector('.navbar')
fetch('/base.html')
.then(res=>res.text())
.then(data=>{
    nav.innerHTML=data
})