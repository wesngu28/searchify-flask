window.addEventListener('load', init);

function init() {
  findLinks();
  findDownloadButton();
  findAuthButton();
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

function findDownloadButton() {
  const downloadButton = document.querySelector('#dl');
  if (downloadButton !== null) {
      downloadButton.addEventListener('click', function(e) {
      e.preventDefault();
      fetch('/download-csv');
      return false;
    })
  }
}

function findAuthButton() {
  const authenticateButton = document.querySelector('#auth');
  authenticateButton.addEventListener('click', function(e) {
    e.preventDefault();
    window.location.href="http://127.0.0.1:5000/user"
    return false;
  })
}