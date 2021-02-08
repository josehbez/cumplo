(function ($) {
/*
var randomScalingFactor = function() {
    return  Math.floor(Math.random() * Math.floor(50));
};
chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

var config = {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'DOLAR',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ],
        }, {
            label: 'UDIS',
            fill: false,
            backgroundColor: chartColors.green,
            borderColor: chartColors.green,
            borderDash: [5, 5],
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ],
        }, {
            label: 'TIIE 28',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ],
            fill: false,
        },{
            label: 'TIIE 91',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ],
            fill: false,
        },{
            label: 'TIIE 28',
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ],
            fill: false,
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Histórico'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Día'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Valor'
                }
            }]
        }
    }
};
*/

    function GetHistorical (){
        $("#request-container").hide();
        $("#start-container").show();

        var hc = document.getElementById('historical-chart');
        if (hc !== null){
            var ctx = hc.getContext('2d');
            fetch('/api/historical').then( response => response.json()).then( data=>{                
                if (data.success == true){
                    var hcConfig = {
                        type: 'line',
                        data: {
                            labels: data.payload.labels,
                            datasets:data.payload.datasets
                        },
                        options: {
                            responsive: true,
                            title: {
                                display: true,
                                text: 'Histórico'
                            },
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Día'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Valor'
                                    }
                                }]
                            }
                        }
                    };
                    new Chart(ctx, hcConfig);
                }else{
                    console.error("Error:", data.message)
                }
                console.log(data)
            }).catch((error)=>{
                console.error("Error:", error)
            });
            
            
        }

    }
    function GetBySerie(menu){
        var path = null; 
        var title = null; 
        if ( menu ===  "DOLAR"){
            title = "Tipo de Cambio";
            path = "/api/dollar";            
        }else if ( menu ===  "UDIS"){
            title ="Valor de UDIS";
            path ="/api/udis"
        }else if ( menu ===  "TIIE"){
            title ="Tasas de Interés Interbancarias";
            path ="/api/tiie";
        }else{
            return 0 
        }

        $("#start-container").hide();
        $("#request-container").show();
        
        $("#rc-title").text(title);

        var rc = document.getElementById('request-chart');
        if (rc !== null){
            var ctx = rc.getContext('2d');
            
            fetch(path,{
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
                },
                method: 'POST', 
                body: JSON.stringify({
                    'dt-from': $("#rc-date-from").val(),
                    'dt-to':$("#rc-date-to").val(),
                })
            }).then( response => response.json()).then( data=>{                
                if (data.success == true){
                    var rcConfig = {
                        type: 'line',
                        data: {
                            labels: data.payload.labels,
                            datasets:data.payload.datasets
                        },
                        options: {
                            responsive: true,
                            //title: {
                            //    display: true,
                            //    text: title
                            //},
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Día'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Valor'
                                    }
                                }]
                            }
                        }
                    };
                    new Chart(ctx, rcConfig);
                }else{
                    console.error(data.message)
                }
                console.log(data)
            }).catch((error)=>{
                console.error( error)
            });

        }
    }

    $(document).ready(function () {
        GetHistorical();
        $('.nav-item').on('click', function (e) {
            e.preventDefault();
            var menu = this.innerText;
            if (menu ===  "INICIO"){
                GetHistorical();
            }else{
                GetBySerie(menu);
            }
            $('.nav-item').removeClass('active');
            var athis = this;
            $(athis).addClass('active');

        });        
        $('#rc-button').on('click', function (e) {
            e.preventDefault();
            $.each( $('.nav-item'), function( key, value ) {
                if ($(value).hasClass('active')){
                    GetBySerie(value.innerText);
                }
            });
        });
        
    });

})(window.jQuery);