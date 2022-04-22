window.addEventListener('load', init);

function init() {
  findLinks();
  findDownloadButton();
  const swapButton = document.querySelector('#swap');
  swapButton.addEventListener('click', function(e){
    e.preventDefault();
    swapContent();
  })
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
    })
  }
}

function swapContent() {
  const swapButton = document.querySelector('#swap');
  swapButton.textContent = 'Show Top Artists'
  artist_table = document.querySelector('#artists');
  artist_table.classList.add('hidden');
  track_table = document.querySelector('#tracks');
  track_table.classList.remove('hidden');
  swapButton.removeEventListener('click', swapContent)
  swapButton.addEventListener('click', swapContentBack)
}

function swapContentBack() {
  const swapButton = document.querySelector('#swap');
  swapButton.textContent = 'Show Top Tracks'
  track_table = document.querySelector('#tracks');
  track_table.classList.add('hidden');
  artist_table = document.querySelector('#artists');
  artist_table.classList.remove('hidden');
  swapButton.removeEventListener('click', swapContentBack)
  swapButton.addEventListener('click', swapContent)
}