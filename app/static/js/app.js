var app = angular.module('myApp', [ 'googlechart', 'angularUtils.directives.dirPagination','ionic']);
app.controller('Sachin',['$scope', '$http', '$timeout', 'Chart', "$window", "$location", function($scope, $http, $timeout, Chart, $window, $location) {
    $scope.countrytable = false;
    $scope.showfilterdata = false;
    $scope.name1= {"Name":["Trip Advisor"]}

    $scope.sourcetable = [
    {"source":"Trip Advisor","sindex":81,"avgrating":"4/5","ranking":"25/100","reviews":"Trip Advisor","distribution":"+ve"}    ]
    $scope.revieindex = [];
    $scope.revierating = [];
    $scope.ratingfilter = ["Postive", "Negative", "Neutral"];
    $scope.singlelinechart=[];
    $scope.multilinechart=[];
    $scope.countrydata = function(idx){
        $scope.oppositionteam = idx;
        $scope.oppdata  = [];
        for(i=0;i<$scope.totaldata.length;i++)
        {
        	if($scope.totaldata[i].opposition == idx)
        	{
        		var data = {"opposition":$scope.totaldata[i].opposition,"date":$scope.totaldata[i].date,"run":$scope.totaldata[i].batting_score,"wicket":$scope.totaldata[i].wickets,"catch":$scope.totaldata[i].catches,"result":$scope.totaldata[i].match_result,"margin":$scope.totaldata[i].result_margin,"inning":$scope.totaldata[i].batting_innings,"ground":$scope.totaldata[i].ground,"concended":$scope.totaldata[i].runs_conceded,};
        		$scope.oppdata.push(data);
        	}	
        }
        $scope.countrytable = true;
    }

       
    $scope.showLoader = function(){
    	$http.post("/grouphotel")
        .success(function(response, status, headers, config) {
        
            $scope.test=response;
          })

       $http.post("/user")
        .success(function(response, status, headers, config) {
            $scope.userdata=response;
          
          })

        $http.post("/channel")
        .success(function(response, status, headers, config) {
            $scope.channel=response;
            
          })

        $http.post("/topic")
        .success(function(response, status, headers, config) {
            
          })



      
          $scope.getchart();
             }
  

    $scope.getchart = function(){
               

        if($scope.hotelname != undefined){
            var temp = $scope.startdate.split("/");
        var start = temp[1] + "/" + temp[0] + "/" + temp[2];
        console.log(start);

        var temp1 = $scope.enddate.split("/");
        var end = temp1[1] + "/" + temp1[0] + "/" + temp1[2];
             var data = {
            hotel:$scope.hotelname,
            startdate:start,
            enddate:end
                        }
        }
        else{
            var data = {
            hotel:"null",
            startdate:"1/01/2013",
            enddate:"30/06/2016"
                        }
            }

             $http.post("/queriedhotel",data)
        .success(function(response, status, headers, config) {

            $scope.queriedhotel=response;    
            console.log(response);          
            $scope.poswidth = $scope.queriedhotel[0]['Postive']*100/$scope.queriedhotel[0]['Total']+"%";
            $scope.negwidth = $scope.queriedhotel[0]['Negative']*100/$scope.queriedhotel[0]['Total']+"%";
            $scope.neuwidth = $scope.queriedhotel[0]['Neutral']*100/$scope.queriedhotel[0]['Total'] +"%";
            $scope.poswidth1 = $scope.queriedhotel[0]['mention_pos']*100/$scope.queriedhotel[0]['mention']+"%";
            $scope.negwidth1 = $scope.queriedhotel[0]['mention_neg']*100/$scope.queriedhotel[0]['mention']+"%";
            $scope.neuwidth1 = $scope.queriedhotel[0]['mention_neu']*100/$scope.queriedhotel[0]['mention']+"%";
                        
          })

        $http.post("/sourcesdata", data)
        .success(function(response, status, headers, config) {
           
             $scope.sourcesdata = response;
             console.log("soure");
             console.log(response);
             for(i=0;i<$scope.sourcesdata.length;i++)
            {
            var total = $scope.sourcesdata[i]["Count"] ;
            var pos = ($scope.sourcesdata[i]["PostiveCount"]/total) * 100;
            var neg = ($scope.sourcesdata[i]["NegativeCount"]/total) * 100;
            var neu = ($scope.sourcesdata[i]["NeutralCount"]/total) * 100;
            $scope.sourcesdata[i]["poswidth"] = pos +"%";
            $scope.sourcesdata[i]["negwidth"] = neg +"%";
            $scope.sourcesdata[i]["neuwidth"] = neu +"%";
            }

        })
          $http.post("/competive",data)
        .success(function(response, status, headers, config) {
            $scope.competive=response;
            for(i=0;i<$scope.competive.length;i++)
            {
            var total = $scope.competive[i]["Postive"] + $scope.competive[i]["Negative"] + $scope.competive[i]["Neutral"];
            var pos = ($scope.competive[i]["Postive"]/total) * 100;
            var neg = ($scope.competive[i]["Negative"]/total) * 100;
            var neu = ($scope.competive[i]["Neutral"]/total) * 100;
            $scope.competive[i]["poswidth"] = pos +"%";
            $scope.competive[i]["negwidth"] = neg +"%";
            $scope.competive[i]["neuwidth"] = neu +"%";
            }
          })
         $http.post("/topicdata",data)
        .success(function(response, status, headers, config) {
            $scope.topicdata=response;
           

            for(i=0;i<$scope.topicdata.length;i++)
            {
            var total = $scope.topicdata[i]["postive"] + $scope.topicdata[i]["Negative"] + $scope.topicdata[i]["Neutral"];
            var pos = ($scope.topicdata[i]["postive"]/total) * 100;
            var neg = ($scope.topicdata[i]["Negative"]/total) * 100;
            var neu = ($scope.topicdata[i]["Neutral"]/total) * 100;
            $scope.topicdata[i]["poswidth"] = pos +"%";
            $scope.topicdata[i]["negwidth"] = neg +"%";
            $scope.topicdata[i]["neuwidth"] = neu +"%";
            }
          })

         $http.post("/getdata", data)
        .success(function(response, status, headers, config) {
           
            
            $scope.positive = 0;
            $scope.negative = 0;
            $scope.neutral = 0;

            $scope.alldata = response.data;
            $scope.allreviewdata = response.data;
            for(var i=0;i<$scope.allreviewdata.length;i++)
            {
                var temp = $scope.unixtodate($scope.allreviewdata[i].Date);
                $scope.allreviewdata[i].Date = temp;
            }
            console.log($scope.allreviewdata);
            $scope.totalcount = $scope.alldata.length;
            for(var i=0;i<$scope.alldata.length;i++)
            {
                if($scope.alldata[i]["Sentiment"] == "Postive")
                {
                    $scope.positive = $scope.positive + 1;
                }
                if($scope.alldata[i]["Sentiment"] == "Negative")
                {
                    $scope.negative = $scope.negative + 1;
                }
                if($scope.alldata[i]["Sentiment"] == "Neutral")
                {
                    $scope.neutral = $scope.neutral + 1;
                }

                if($scope.alldata[i]["Channel"] == "Burrp")
                {

                }
            }
            $scope.poswidth = $scope.positive*100/$scope.totalcount+"%";
            $scope.negwidth = $scope.negative*100/$scope.totalcount +"%";
            $scope.neuwidth = $scope.neutral*100/$scope.totalcount +"%";

          })	
   $http.post("/singlelinechart",data)
        .success(function(response, status, headers, config) {
            $scope.singlelinechart=response;
          console.log("response34");
            console.log(response);
    })

         nv.addGraph(function() {
         var chart = nv.models.lineChart()
         .x(function(d) { return d[0]})
        .y(function(d) { return d[1] })
        .options({
            transitionDuration: 300,    // This should be duration: 300
            useInteractiveGuideline: true
                });
        chart.xAxis.tickFormat(function(d) {
            return d3.time.format('%d/%b/%y')(new Date(d))
        });
        chart.yAxis.tickFormat(d3.format(',.2f'));
        d3.select('#chart1 svg')
            .datum(cumulativeTestData())
            .call(chart);
        
        //TODO: Figure out a good way to do this automatically
       nv.utils.windowResize(function() { chart.update() });
  return chart;
    });

    $scope.reviewlink = function(url)
    {
        console.log(url);
        $window.open(url, '_self');

    }

    $scope.sharefb = function(data)
    {
        var url = "https://www.facebook.com/sharer/sharer.php?u=" + "data.Comment";
        console.log(url);
        // $window.open(url, '_self');
        $window.location.href = url;

    }
 
    function cumulativeTestData() {
        var data1= $scope.singlelinechart;
        return data1        
    }


     $http.post("/multilinechart",data)
        .success(function(response, status, headers, config) {
            $scope.multilinechart=response;
          console.log("response34");
            console.log(response);
    })

         nv.addGraph(function() {
         var chart = nv.models.lineChart()
         .x(function(d) { return d[0]})
        .y(function(d) { return d[1] })
        .options({
            transitionDuration: 300,    // This should be duration: 300
            useInteractiveGuideline: true
                });
        chart.xAxis.tickFormat(function(d) {
            return d3.time.format('%d/%b/%y')(new Date(d))
        });
        chart.yAxis.tickFormat(d3.format(',.2f'));
        d3.select('#chart2 svg')
            .datum(cumulative())
            .call(chart);
        
        //TODO: Figure out a good way to do this automatically
       nv.utils.windowResize(function() { chart.update() });
  return chart;
    });

 
    function cumulative() {
        var data2= $scope.multilinechart;
        return data2       
    }

    }

    $scope.unixtodate = function(UNIX_timestamp)
    {
        var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var time = date + ' ' + month + ' ' + year;
  return time;
    }
    
    $scope.reviewfilters = function(ios){

            var temp = [];
            if($scope.revieindex.indexOf(ios) == -1)
            {
                $scope.revieindex.push(ios);
            }
            else
            {
                $scope.revieindex.splice($scope.revieindex.indexOf(ios), 1);
            }
             console.log($scope.alldata);
             console.log($scope.revieindex);
             for(i=0;i<$scope.alldata.length;i++)
             {
                if($scope.revieindex.indexOf($scope.alldata[i]["Channel"]) >=0 || $scope.revieindex.indexOf($scope.alldata[i]["Sentiment"]) >=0)
                {
                    temp.push($scope.alldata[i]);
                }
             }

             if($scope.revieindex.length !=0)
             {
                $scope.allreviewdata = temp;
             }
             else{
                $scope.allreviewdata = $scope.alldata;
             }

             console.log(temp);
             
             console.log($scope.allreviewdata);
         }

       


}]);