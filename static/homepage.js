$(".hamburger").on("click", function() {
  $(".sidebar").addClass("active");
});

$(".close").on("click", function() {
  $(".sidebar").removeClass("active");
});
