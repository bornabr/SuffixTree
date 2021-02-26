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
			tree = res.tree_simple_view
			result = res.result
			console.log(tree)
			$('#section1-network').val(tree)
			$('#section1-network').show()
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
			tree = res.tree_simple_view
			result = res.result
			console.log(tree)
			$('#section2-network').val(tree)
			$('#section2-network').show()
			$('#section2-result').append(`<pre>${result}</pre>`)
			$('#section2-result').show()
			try {
				const link = document.createElement('a');
				link.href = window.URL.createObjectURL(new Blob(['\ufeff', String(result)], { type: 'text/plain' }));
				link.setAttribute('download', 'result');
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			} catch(err) {
				console.log(err)
			}
			
		});
}

function lcs (data) {
	$.post("/api/lcs",
		data,
		function (res) {
			console.log(res)
			tree = res.tree_simple_view
			result = res.result
			console.log(tree)
			$('#section3-network').val(tree)
			$('#section3-network').show()
			$('#section3-result').append(`<pre>${result}</pre>`)
			$('#section3-result').show()
			try {
				const link = document.createElement('a');
				link.href = window.URL.createObjectURL(new Blob(['\ufeff', String(result)], { type: 'text/plain' }));
				link.setAttribute('download', 'result');
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			} catch(err) {
				console.log(err)
			}
			
		});
}

function lps(data) {
	$.post("/api/lps",
		data,
		function (res) {
			console.log(res)
			tree = res.tree_simple_view
			result = res.result
			console.log(tree)
			$('#section4-network').val(tree)
			$('#section4-network').show()
			$('#section4-result').append(`<pre>${result}</pre>`)
			$('#section4-result').show()
			try {
				const link = document.createElement('a');
				link.href = window.URL.createObjectURL(new Blob(['\ufeff', String(result)], { type: 'text/plain' }));
				link.setAttribute('download', 'result');
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			} catch (err) {
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
	
	$("#form-section-three").submit(function (e) {
		e.preventDefault();
		$('#section3-result').empty()
		$('#section3-result').hide()
		$('#section3-network').hide()
		const serialized = $("#form-section-three").serializeArray()
		const data = {}
		serialized.forEach(({ name, value }) => data[name] = value);
		console.log(data)
		if (!data.strings || data.strings == '') {
			if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
				alert('The File APIs are not fully supported in this browser.');
				return;
			}
			let inputFile = document.getElementById('file-input-3');
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
					lcs(data)
				}
			}
		} else {
			lcs(data)
		}
	});
	
	$("#form-section-four").submit(function (e) {
		e.preventDefault();
		$('#section4-result').empty()
		$('#section4-result').hide()
		$('#section4-network').hide()
		const serialized = $("#form-section-four").serializeArray()
		const data = {}
		serialized.forEach(({ name, value }) => data[name] = value);
		console.log(data)
		if (!data.strings || data.strings == '') {
			if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
				alert('The File APIs are not fully supported in this browser.');
				return;
			}
			let inputFile = document.getElementById('file-input-4');
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
					lps(data)
				}
			}
		} else {
			lps(data)
		}
	});
	
});
