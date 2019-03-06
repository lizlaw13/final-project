$('.hamburger').on('click', function() {
  $('.sidebar').addClass('active');
});

$('.close').on('click', function() {
  $('.sidebar').removeClass('active');
});

$('#myModal').on('shown.bs.modal', function() {
  $('#myInput').trigger('focus');
});
