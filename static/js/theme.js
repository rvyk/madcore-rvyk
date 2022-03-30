// function change() {
//     $(".banner").toggleClass('dark');
//     $(".footer").toggleClass('dark');
//     $(".copyright").toggleClass('dark');
//     $(".social a").toggleClass('dark');
//     $(".footer ul li a").toggleClass('dark');
//     $(".scrollup").toggleClass('dark');
//     $(".topname").toggleClass('dark');
//     $(".topka1").toggleClass('dark');
//     $(".kratka").toggleClass('dark');
//     $(".kratkavalue").toggleClass('dark');
//     $("th").toggleClass('dark');
//     $("td").toggleClass('dark');
//     $("body").toggleClass('dark');
//     $("path").toggleClass('dark');
//     $("header").toggleClass('dark');
// }

let darkMode = localStorage.getItem('darkMode'); 

function enableDarkMode() {
    $(".banner").addClass('dark');
    $(".footer").addClass('dark');
    $(".copyright").addClass('dark');
    $(".social a").addClass('dark');
    $(".footer ul li a").addClass('dark');
    $(".scrollup").addClass('dark');
    $(".topname").addClass('dark');
    $(".topka1").addClass('dark');
    $(".topka2").addClass('dark');
    $(".topka3").addClass('dark');
    $(".kratka").addClass('dark');
    $(".kratkavalue").addClass('dark');
    $("th").addClass('dark');
    $("td").addClass('dark');
    $("body").addClass('dark');
    $("path").addClass('dark');
    $("header").addClass('dark');
    localStorage.setItem('darkMode', 'enabled');
}

function disableDarkMode() {
    $(".banner").removeClass('dark');
    $(".footer").removeClass('dark');
    $(".copyright").removeClass('dark');
    $(".social a").removeClass('dark');
    $(".footer ul li a").removeClass('dark');
    $(".scrollup").removeClass('dark');
    $(".topname").removeClass('dark');
    $(".topka1").removeClass('dark');
    $(".topka2").removeClass('dark');
    $(".topka3").removeClass('dark');
    $(".kratka").removeClass('dark');
    $(".kratkavalue").removeClass('dark');
    $("th").removeClass('dark');
    $("td").removeClass('dark');
    $("body").removeClass('dark');
    $("path").removeClass('dark');
    $("header").removeClass('dark');
    localStorage.setItem('darkMode', null);
}

$(document).ready(function () {
  if (darkMode === 'enabled') {
      enableDarkMode();
  }
});


$(document).on('click', '.theme', function(event){
  darkMode = localStorage.getItem('darkMode'); 
  if (darkMode !== 'enabled') {
    enableDarkMode();
  } else {  
    disableDarkMode(); 
  }
});
