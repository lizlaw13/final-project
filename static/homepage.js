$("button").on("shown.bs.modal", function() {
  console.log("hi");
  $("#myInput").trigger("focus");
});
