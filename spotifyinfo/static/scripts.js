window.addEventListener('load', init);

function init() {
  let searchButton = document.querySelector('#sub');
  searchButton.disabled = true
  findLinks();
  findDownloadButton();
  let input = document.querySelector('#inp');
  input.addEventListener('input', validation);
  input.addEventListener('input', findSearchButton);
  findSwapButton();
}

function validation() {
  let input = document.querySelector('#inp');
  let searchButton = document.querySelector('#sub');
  spotifyUrl = new RegExp('^(https:\/\/open.spotify.com\/)([a-zA-Z0-9]+)(.*)$');
  spotifyUrlChars = new RegExp('^[A-Za-z0-9?.=:\/_]*$')
  if (!spotifyUrl.test(input.value) || !spotifyUrlChars.test(input.value)) {
    searchButton.disabled = true
  } else {
    searchButton.disabled = false
  }
}
function findSearchButton() {
  let searchButton = document.querySelector('#sub');
  if (searchButton !== null) {
    let input = document.querySelector('#inp');
    if (input.value !== null) {
      if ((input.value.includes('playlist')) || (input.value.includes('album') || (input.value.includes('track')) || (input.value.includes('artist')))) {
        searchButton.addEventListener('click', message);
      }
    }
  }
}

function message() {
  let p = document.createElement('p');
  p.textContent = 'Currently loading information...'
  let newHome = document.querySelector('#link_container');
  newHome.appendChild(p);
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


function findSwapButton() {
  const swapButton = document.querySelector('#swap');
  if (swapButton !== null) {
    swapButton.addEventListener('click', function(e){
      e.preventDefault();
      swapContent();
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