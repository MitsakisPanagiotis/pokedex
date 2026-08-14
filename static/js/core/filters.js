const select = document.getElementById('generation');
const typeSelect = document.getElementById('type-1');
const type2Select = document.getElementById('type-2');
const pokemon = document.querySelectorAll('div.card-container');

select.addEventListener('change', applyFilter);
typeSelect.addEventListener('change', applyFilter);
type2Select.addEventListener('change', applyFilter);

function applyFilter() {
	let gen = select.value;
	let type1 = typeSelect.value;
	let type2 = type2Select.value;
	const pokemonList = Array.from(pokemon);

	const filtered = pokemonList.filter((p) => {
		return (
			(gen === 'all' || p.dataset.generation === gen) &&
			(type1 === 'all' || p.dataset.type1 === type1) &&
			(type2 === 'all' || p.dataset.type2 === type2)
		);
	});
	pokemon.forEach((p) => (p.style.display = 'none'));
	filtered.forEach((el) => (el.style.display = 'block'));
}
