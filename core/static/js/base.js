function OpenMenu() {
  var navbar = $(".menu");
  if (navbar.attr('class') === "menu") {
    navbar.addClass(" responsive");
  } else {
    navbar.attr('class', 'menu');
  }
}
