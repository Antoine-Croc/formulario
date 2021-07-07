var text = '';
const reader = new FileReader();
reader.onload = function (e) {
	document.querySelector('.output').innerText = e.target.result;
}

function read(input) {
	const csv = input.files[0];
	text = reader.readAsText(csv);
}

function getText(){
	return document.getElementById('csvtext_use').innerText
}

function makecsvJson() {
	test(getText());
}