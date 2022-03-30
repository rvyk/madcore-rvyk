
// function popup(){
//     setTimeout(function(){
//         $('.popup-box').css('display','block');
//         $(".popup-box").addClass('show');
//       },0);
// }
// function popupclose(){
//     setTimeout(function(){
//         $('.popup-box').css('display','none');
//         $(".popup-box").removeClass('show');
//       },0);   
// }
function infoopen(){
    $('.banner h2').html("DISCORD");
    $('.banner p').html("Żeby dowiedzieć się więcej, dołącz do nas na serwer discord.");
    $('.more').html("Pokaż ogólne");
    $('.adres').html("Skopiuj adres discorda");
    $(".more").attr("onclick","infoclose()");
    $(".adres").attr("onclick","kopiujdsc()");
};
function infoclose(){
    $('.banner h2').html("MADCORE.PL");
    $('.banner p').html("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer venenatis vestibulum urna. Nulla facilisi. Duis varius posuere lectus tempor vestibulum. Vivamus nec dictum diam. Curabitur vitae gravida nisl. In aliquam sollicitudin arcu, a vehicula metus lacinia at. Praesent et dolor at sem bibendum ultrices. Praesent ut nisl ipsum. Morbi sodales bibendum nisi ac ornare. Morbi nec sem nunc. Ut in fringilla nibh. Praesent a congue tellus. In quis nunc eu massa eleifend vulputate ac in purus. Vestibulum et congue enim, eu imperdiet lorem.");
    $('.more').html("Dowiedz się więcej");
    $('.adres').html("Skopiuj adres serwera");
    $(".more").attr("onclick","infoopen()");
    $(".adres").attr("onclick","kopiuj()");
};