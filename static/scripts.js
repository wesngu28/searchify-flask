window.addEventListener('load', init);

function init() {
  findLinks();
}

function findLinks() {
  const linkSearch = document.querySelectorAll('#pl_ytlinks td');
  for(let i = 0; i < linkSearch.length; i++) {
    if (linkSearch[i].textContent.includes('https')) {
      let link = document.createElement('a');
      link.href = linkSearch[i].textContent;
      link.textContent = 'Youtube Link';
      linkSearch[i].textContent = '';
      linkSearch[i].appendChild(link);
    }
  }
}