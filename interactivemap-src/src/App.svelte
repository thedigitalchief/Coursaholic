
<script lang="ts">

	import {onMount} from 'svelte';
	import Chart from 'chart.js/auto'; // https://www.chartjs.org/
	import { DendogramController } from 'chartjs-chart-graph'; // https://github.com/sgratzl/chartjs-chart-graph
	import AutoComplete from "simple-svelte-autocomplete"; // https://github.com/pstanoev/simple-svelte-autocomplete
	import ChartDataLabels from 'chartjs-plugin-datalabels'; //https://github.com/chartjs/chartjs-plugin-datalabels
	Chart.register(DendogramController);

	let loaded = false;
	let canvas; // canvas that chart.js uses to draw
	let requisites = []; 
	let courses = [];
	let selectedCourse;

	function createChart(nodes, edges) {
		if (canvas)
			canvas.destroy();
		canvas = new Chart(document.getElementById("canvas").getContext("2d"), {
			type: DendogramController.id,
			data: {
				labels: nodes.map((d) => d.name),
				datasets: [{
					pointBackgroundColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
					pointRadius: 20,
					pointHoverRadius: 25,
					data: nodes.map((d) => Object.assign({}, d)),
					edges: edges
				}]
			},
			plugins: [ChartDataLabels],
			options: {
				tree: { orientation: "vertical" },
				layout: { padding: { left: 5, top: 5, bottom: 5, right: 5 } },
				plugins: {
					legend: { display: false },
					tooltip: { enabled: false },
					datalabels: {
						color: `#${Math.floor(Math.random()*16777215).toString(16)}`,
						formatter: function(value, context) { return value.name; },
						align: 'bottom',
						offset: 25,
						font: {size: 15}
					}
				}
			}
		});
	}

	function randRange(min, max)
	{
		return Math.random() * (max - min) + min;
	}

	$: selectedCourse, updateMap();
	function updateMap() {
		if (requisites.length < 1)
			return
		let nodes = [], edges = [];
		const prerequisites = requisites[selectedCourse].prerequisites;
		nodes.push({ "name":selectedCourse, "x":0, "y":0 });
		prerequisites.forEach(prereq_dict => {
			prereq_dict[Object.keys(prereq_dict)[0]].forEach(prereq => {
				const angle = Math.random()*Math.PI*2;
				edges.push({ "source": 0, "target": nodes.length });
				// nodes.push({ "name":prereq, "x":Math.cos(angle)*0.85, "y":Math.sin(angle)*0.85 });
				let x = 0, y = 0;
				while (Math.abs(x) < 0.2 && Math.abs(y) < 0.2)
				{
					x = randRange(-0.8, 0.8);
					y = randRange(-0.8, 0.8);
				}
				nodes.push({ "name": prereq, "x": x, "y": y });
			})
		})
		createChart(nodes, edges);
	}

	onMount(async () => {
		fetch('requisite.json')
		.then(response => response.json())
		.then(jsondata => {
			requisites = jsondata;
			courses = Object.keys(jsondata);
			selectedCourse = courses[0]
			while (requisites[selectedCourse].prerequisites.length < 2) // guarantees that first map looks interesting
				selectedCourse = courses[Math.floor(Math.random()*courses.length)];
			loaded = true;
		});
	});
</script>

<main>
	{#if loaded}
	<h1>Choose a course: </h1>
	<AutoComplete items={courses} bind:selectedItem={selectedCourse} maxItemsToShowInList={5}/>
	{/if}
	<canvas id="canvas"></canvas>
</main>

<style>
	main {
		text-align: center;
		padding: 0;
		width: 100%;
		height: 95%;
		margin: 0 0;
	}

	h1 {
		display: inline;
		color: #053179;
		text-transform: uppercase;
		font-size: 1.8em;
		font-weight: 200;
	}

	canvas {
		max-height: 100%;
		max-width: 100%;
	}
</style>