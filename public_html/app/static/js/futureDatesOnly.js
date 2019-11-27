$(document).ready(function(){
    var today = new Date().toISOString().split('T')[0];
    document.getElementsByName("cardexpiration")[0].setAttribute('min', today);
});