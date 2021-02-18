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
		console.log($("#form-section-one").serializeArray())
		$.post("/api/search-pattern",
			$("#form-section-one").serializeArray(),
			function (res) {
				console.log(res)
				tree = res.tree
				var nodes = new vis.DataSet(tree.nodes);
	
				// create an array with edges
				var edges = new vis.DataSet(tree.edges);
	
				// create a network
				var container = document.getElementById("section1-network");
				var data = {
					nodes: nodes,
					edges: edges,
				};
				var options = {};
				var network = new vis.Network(container, data, options);
				container.style.display = "block"
			});
		
	});
});
// Get the element with id="defaultOpen" and click on it
