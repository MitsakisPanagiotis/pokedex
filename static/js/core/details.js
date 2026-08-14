const pHeight = document.getElementById('height');
const pWeight = document.getElementById('weight');

const re = new RegExp(/\d+.\d+/);
const feet = Intl.NumberFormat('en-GB', {
	style: 'unit',
	unit: 'foot',
	unitDisplay: 'narrow',
	maximumFractionDigits: 2
}).format(3.28084 * Number.parseFloat(pHeight.innerText.replace(',', '.').match(re)));
const pounds = Intl.NumberFormat('en-GB', {
	style: 'unit',
	unit: 'pound',
	unitDisplay: 'narrow',
	maximumFractionDigits: 2
}).format(2.20462 * Number.parseFloat(pWeight.innerText.replace(',', '.').match(re)));

pHeight.innerText += ` (${feet})`;
pWeight.innerText += ` (${pounds})`;
