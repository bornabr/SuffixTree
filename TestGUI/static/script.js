function openPage(pageName, elmnt, color) {
	// Hide all elements with class="tabcontent" by default */
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// Remove the background color of all tablinks/buttons
	tablinks = document.getElementsByClassName("tablink");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].style.backgroundColor = "";
	}

	// Show the specific tab content
	document.getElementById(pageName).style.display = "block";

	// Add the specific color to the button used to open the tab content
	elmnt.style.backgroundColor = color;
}

function search_pattern (data) {
	$.post("/api/search-pattern",
		data,
		function (res) {
			console.log(res)
			tree = res.tree
			let nodes = new vis.DataSet(tree.nodes);

			// create an array with edges
			let edges = new vis.DataSet(tree.edges);

			// create a network
			let container = document.getElementById("section1-network");
			let data = {
				nodes: nodes,
				edges: edges,
			};
			let options = {};
			let network = new vis.Network(container, data, options);
			container.style.display = "block"

			result = res.result
			$('#section1-result').append(`<pre>${JSON.stringify(res.result, null, 2)}</pre>`)
			$('#section1-result').show()
			try {
				const link = document.createElement('a');
				link.href = window.URL.createObjectURL(new Blob(['\ufeff', JSON.stringify(result, null, 2)], { type: 'text/plain' }));
				link.setAttribute('download', 'result');
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			} catch(err) {
				console.log(err)
			}
			
		});
}

function lrs (data) {
	$.post("/api/lrs",
		data,
		function (res) {
			console.log(res)
			tree = res.tree
			let nodes = new vis.DataSet(tree.nodes);

			// create an array with edges
			let edges = new vis.DataSet(tree.edges);

			// create a network
			let container = document.getElementById("section2-network");
			let data = {
				nodes: nodes,
				edges: edges,
			};
			let options = {};
			let network = new vis.Network(container, data, options);
			container.style.display = "block"

			result = res.result
			$('#section2-result').append(`<pre>${JSON.stringify(res.result, null, 2)}</pre>`)
			$('#section2-result').show()
			try {
				const link = document.createElement('a');
				link.href = window.URL.createObjectURL(new Blob(['\ufeff', JSON.stringify(result, null, 2)], { type: 'text/plain' }));
				link.setAttribute('download', 'result');
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			} catch(err) {
				console.log(err)
			}
			
		});
}

$(document).ready(function () {
	document.getElementById("defaultOpen").click();

	$("#form-section-one").submit(function (e) {
		e.preventDefault();
		$('#section1-result').empty()
		$('#section1-result').hide()
		$('#section1-network').hide()
		const serialized = $("#form-section-one").serializeArray()
		const data = {}
		serialized.forEach(({ name, value }) => data[name] = value);
		if (!data.strings || data.strings == ''){
			if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
				alert('The File APIs are not fully supported in this browser.');
				return;
			}
			let inputFile = document.getElementById('file-input-1');
			if (!inputFile) {
				alert("Um, couldn't find the fileinput element.");
			}
			else if (!inputFile.files) {
				alert("This browser doesn't seem to support the `files` property of file inputs.");
			}
			else if (!inputFile.files[0]) {
				alert("Please select a file before submiting");
			}
			else {
				let file = inputFile.files[0];
				let fr = new FileReader();
				fr.readAsText(file);
				fr.onload = () => {
					data.strings = fr.result
					search_pattern(data)
				}
			}
		} else {
			search_pattern(data)
		}
	});
	
	$("#form-section-two").submit(function (e) {
		e.preventDefault();
		$('#section2-result').empty()
		$('#section2-result').hide()
		$('#section2-network').hide()
		const serialized = $("#form-section-two").serializeArray()
		const data = {}
		serialized.forEach(({ name, value }) => data[name] = value);
		console.log(data)
		if (!data.strings || data.strings == '') {
			if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
				alert('The File APIs are not fully supported in this browser.');
				return;
			}
			let inputFile = document.getElementById('file-input-2');
			if (!inputFile) {
				alert("Um, couldn't find the fileinput element.");
			}
			else if (!inputFile.files) {
				alert("This browser doesn't seem to support the `files` property of file inputs.");
			}
			else if (!inputFile.files[0]) {
				alert("Please select a file before submiting");
			}
			else {
				let file = inputFile.files[0];
				let fr = new FileReader();
				fr.readAsText(file);
				fr.onload = () => {
					data.strings = fr.result
					lrs(data)
				}
			}
		} else {
			lrs(data)
		}
	});
});
