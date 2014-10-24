$(window).load(function() {

  var dataArr = [];

  dataArr = $('microspecies-distribution').val();

  // {% for key,value in data.items %}
  //   dataArr.push({{value}});
  // {% endfor %}

  var plot1 = $.jqplot ('{{title|slugify}}', dataArr, {
		title: '{{title}}',
  	axes: {
  		xaxis: {
  			label: 'pH',
  			min: 0,
  			max: 14,
  			tickInterval: 1
  		},
  	},
  	seriesDefaults: {
  		showMarker: false
  	}
  });

});