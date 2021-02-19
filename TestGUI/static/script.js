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
$(document).ready(function () {
	document.getElementById("defaultOpen").click();

	$("#form-section-one").submit(function (e) {
		e.preventDefault();
		$('#section1-result').empty()
		$('#section1-result').hide()
		$('#section1-network').hide()
		serialize = $("#form-section-one").serializeArray()
		if (!serialize.find(item => item.name == 'strings').value && serialize.find(item => item.name == 'strings').value == '')
			return
		$.post("/api/search-pattern",
			$("#form-section-one").serializeArray(),
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
			});
		
	});
});
// Get the element with id="defaultOpen" and click on it
