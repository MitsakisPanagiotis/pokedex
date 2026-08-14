import { searchClient } from 'https://cdn.jsdelivr.net/npm/@algolia/client-search@5.56.0/+esm';

const config = await fetch('/config').then((response) => response.json());
const input = document.getElementById('search-input');
const ul = document.getElementById('results');
const client = searchClient(config.APPLICATION_ID, config.SEARCH_API_KEY);

input.addEventListener('input', handleResults);

function handleResults(e) {
	let q = e.target.value;
	const response = client.searchSingleIndex({ indexName: 'pokemon', searchParams: { query: q } });
	response.then((data) => {
		let results = data.hits;

		if (q === '' || results.length === 0) {
			ul.classList.remove('show');
			ul.classList.add('hide');
			ul.innerHTML = '';
			return;
		}

		ul.innerHTML = '';
		for (let result of results) {
			let li = document.createElement('li');
			let text = document.createTextNode(result.name);
			let img = document.createElement('img');
			let a = document.createElement('a');
			let div = document.createElement('div');
			let imgDiv = document.createElement('div');
			img.setAttribute('src', result.sprite);
			img.setAttribute('alt', `${result.name}.png`);
			imgDiv.appendChild(img);
			a.setAttribute('rel', 'noopener noreferrer');
			a.setAttribute('href', `pokemon/${result.slug}`);
			div.appendChild(text);
			a.appendChild(imgDiv);
			a.appendChild(div);
			a.setAttribute('class', 'anchor');
			li.appendChild(a);
			li.setAttribute('class', 'list-item');
			ul.appendChild(li);
		}

		input.insertAdjacentElement('afterend', ul);
		ul.classList.remove('hide');
		ul.classList.add('show');
	});
}
