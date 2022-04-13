window.addEventListener('load', init);

function init() {
  const becomeURL = document.querySelectorAll('tbody > tr > td:first-child');
  console.log(becomeURL);
  for (let i = 0; i < becomeURL.length; i++) {
    let link = document.createElement('a');
    link.href = becomeURL[i].textContent;
    console.log(link);
    link.textContent = 'URL here';
    becomeURL[i].textContent = '';
    becomeURL[i].appendChild(link);
  }
}