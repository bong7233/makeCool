$(".infoBox").mouseover(() => {
  $(".detailBox").slideToggle(100);
});

$("html").click(function (e) {
  if (!$(e.target).hasClass("detailBox") && !$(e.target).hasClass("infoBox")) {
    $(".detailBox").hide();
  }
});