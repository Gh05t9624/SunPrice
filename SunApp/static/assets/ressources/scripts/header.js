// Change Background Header (Changement du Background)
function scrollHeader(){
  const header = document.getElementById('header')

  // When the scroll is greater than 80 viewport height, add the scroll-header class to the header class to the header tag
  if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)

const menulinks = document.querySelectorAll('.nav_link');

function colorLink() {
  menulinks.forEach(l => l.classList.remove('active-link'))
  this.classList.add('active-link')
}
menulinks.forEach(l => l.addEventListener('click', colorLink))

// Drop Down
let profilDropdownList = document.querySelector(".profil-dropdown-list");
let btn = document.querySelector(".link-profil");

const toggle = ()  => profilDropdownList.classList.toggle("active");


// slider
var politic = 0;
var P = 0;
var sliderP = document.getElementsByClassName("sliderP");
var lineP = document.getElementsByClassName("line_P");

autoP();

function showP(n) {
  for(P = 0; P < sliderP.length; P++) {
      sliderP[P].style.display = "none";
  }
  for(P = 0; P < lineP.length; P++) {
      lineP[P].className = lineP[P].className.replace("activeP");
  }
  sliderP[n - 1].style.display = ("block");
  lineP[n - 1].className += " activeP";
}

function autoP() {
  politic ++;
  if (politic > sliderP.length) {
      politic = 1;
  }
  showP(politic);
  setTimeout(autoP, 5000);
}

function plusSlideP(n) {
  politic+=n;
  if (politic > sliderP.length) {
      politic=1;
  }
  if(politic < 1) {
      politic=sliderP.length;
  }
  showP(politic);
}

function currentSlideP(n) {
  politic = n;
  showP(politic);
}
// End