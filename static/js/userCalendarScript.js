let nav = 0;
let clicked = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const calendar = document.getElementById('calendar');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

function load() {
  const dt = new Date();

  if (nav !== 0) {
    dt.setMonth(new Date().getMonth() + nav);
  }

  const day = dt.getDate();
  const month = dt.getMonth();
  const year = dt.getFullYear();

  const firstDayOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
    weekday: 'long',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  });
  const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);

  document.getElementById('monthDisplay').innerText = 
    `${dt.toLocaleDateString('es', { month: 'long' })} ${year}`;

  calendar.innerHTML = '';

  for(let i = 1; i <= paddingDays + daysInMonth; i++) {
    const daySquare = document.createElement('div');
    daySquare.classList.add('day');

    const dayString = `${month + 1}/${i - paddingDays}/${year}`;

    if (i > paddingDays) {
      daySquare.innerText = i - paddingDays;
      currentUrl = String(window.location.href)
      currentUrlSplitted= currentUrl.split("/")


      if (i - paddingDays === day && nav === 0) {
        daySquare.id = 'currentDay';
      }
      if (((i - paddingDays > day && nav === 0) || nav!=0 )&& currentUrlSplitted[currentUrlSplitted.length - 4]==='usuarios'){
      daySquare.addEventListener('click', () => redirectToSalas(dayString)); 
      }
      if (currentUrlSplitted[currentUrlSplitted.length - 3]==='admin'){
      daySquare.addEventListener('click', () => redirectToDayView(dayString));
      }
    } 
    else {
      daySquare.classList.add('padding');
    }

    calendar.appendChild(daySquare);    
  }
}
function redirectToSalas(fecha){
  direccion = String(window.location.href)+"reservaSala/"+String(fecha);
  window.location.href = direccion;
}
function redirectToDayView(fecha){
  direccion = String(window.location.href)+"dayview/"+String(fecha);
  window.location.href = direccion;
}
function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
  });

  document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
  });

}

initButtons();
load();

