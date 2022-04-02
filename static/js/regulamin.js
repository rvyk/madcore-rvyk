function discord(){
    $(".regulamin-discord").removeClass('turnoff');
    $(".discord").addClass('aktywny');
    $(".platnosci").removeClass('aktywny');
    $(".regulamin-platnosci").addClass('turnoff');
    $(".minecraft").removeClass('aktywny');
    $(".regulamin-minecraft").addClass('turnoff');
}
function platnosci(){
    $(".regulamin-discord").addClass('turnoff');
    $(".discord").removeClass('aktywny');
    $(".regulamin-platnosci").removeClass('turnoff');
    $(".platnosci").addClass('aktywny');
    $(".regulamin-minecraft").addClass('turnoff');
    $(".minecraft").removeClass('aktywny');
}
function minecraft(){
    $(".discord").removeClass('aktywny');
    $(".regulamin-discord").addClass('turnoff');
    $(".platnosci").removeClass('aktywny');
    $(".regulamin-platnosci").addClass('turnoff');
    $(".minecraft").addClass('aktywny');
    $(".regulamin-minecraft").removeClass('turnoff');
}