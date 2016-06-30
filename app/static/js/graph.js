var app = angular.module('myApp');
  app.factory('Chart', [function(){
    return{
        createLineChart: function(table){
           var a =5;
           var createlinkedgraph3 = {
              "type": "LineChart",
              "data": table,
              "options" : {
                'legend': {'position': 'top'},
                'height': 350,
                'width' : '100%',
                'chartArea': {
                    'width': '80%',
                    'top': 30,
                    'bottom': 10,
                    'left': 55,
                    'right': 0
                },
                'backgroundColor': 'transparent',
              }
          }
           return createlinkedgraph3;
		},

createBarChart: function(table){
           var a =5;
           var createlinkedgraph3 = {
              "type": "ColumnChart",
              "data": table,
              "options" : {
                'isStacked':true,
                'legend': {'position': 'top'},
                'height': 350,
                'width' : '100%',
                'chartArea': {
                    'width': '80%',
                    'top': 30,
                    'bottom': 10,
                    'left': 55,
                    'right': 0
                },
                'bar': { groupWidth: '80%'},
                'backgroundColor': 'transparent',
                'hAxis': { 
                  'gridlines': { 
                    'color': 'transparent'
                  },
                  'baselineColor': 'transparent',
                  'slantedText': true,
                  'slantedTextAngle': 60,
                  'textStyle' : {
                    'fontSize': 14 
                },
                },
                'vAxes': {0: {
                    'gridlines': {color: 'transparent'},
                    'textStyle' : {
                    'fontSize': 14 ,
                    }},
                    },
                'legend': {position: 'top',alignment:'end',maxLines:5},
                'tooltip':{isHtml: true},
                'series': { 0: {color: '#008CDD',targetAxisIndex:0}
                          }
              }
          }
           return createlinkedgraph3;
    },
		
	createPieChart: function(){
            var options = {
          	'height': 350,
                'width' : '100%',
                'backgroundColor': 'transparent',
                'legend': {'position': 'bottom'},
                'chartArea': {
                    'width': '100%',
                    'top': 30,
                    'bottom': 10,
                    'left': 0,
                    'right': 0
                },
                'textStyle' : {
                    'fontSize': 14 
                },
                'tooltip':{isHtml: true},
                'is3D': true,
                'forceIFrame':true
               
        };
           return options;
		    }
      }
    }]);

   
  