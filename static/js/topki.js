function smierci(){
    $(".topka1").addClass('schowany');
    $(".topka3").removeClass('schowany');
    $(".menu1").removeClass('aktywny');
    $(".menu3").addClass('aktywny');
}
function zabojstwa(){
    $(".topka1").removeClass('schowany');
    $(".topka3").addClass('schowany');
    $(".menu1").addClass('aktywny');
    $(".menu3").removeClass('aktywny');
}