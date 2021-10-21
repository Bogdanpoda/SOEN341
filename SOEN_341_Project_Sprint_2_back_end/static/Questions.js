let questions=document.querySelectorAll('.Questions');
let inputField=document.getElementById('questionID_Selected');

for (let i=0;i<questions.length;i++){
    questions[i].addEventListener('click',()=>{
        var x=confirm("Are you sure to choose the question number "+(i+1))

        if (x==true){
            inputField.value = i+1
        }
    })
}



