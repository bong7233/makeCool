$(document).ready(() => {
  $(".detailBox").hide();
});
// 아코디언 열고닫기
$(".infoBox").mouseover(() => {
  $(".detailBox").slideToggle(100);
});

// 아코디언 숨기기
$("html").click((e) => {
  if (!$(e.target).hasClass("detailBox") && !$(e.target).hasClass("infoBox")) {
    $(".detailBox").hide();
  }
});
