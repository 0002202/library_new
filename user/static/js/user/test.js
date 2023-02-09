$(function(){
    const divName = document.querySelectorAll('.name');
    
    for(var i =0; i<divName.length; i++){
        divName[i].addEventListener('click', function(){
            console.log(11);
        });
    }
})
