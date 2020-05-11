/*!

=========================================================
* Argon Dashboard - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard
* Copyright 2018 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard/blob/master/LICENSE.md)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

//
// Bootstrap Datepicker
//

'use strict';

var Datepicker = (function() {

  // Variables

  var $datepicker = $('.datepicker');


  // Methods

  function init($this) {
    var options = {
      disableTouchKeyboard: true,
      autoclose: false
    };

    $this.datepicker(options);
  }


  // Events

  if ($datepicker.length) {
    $datepicker.each(function() {
      init($(this));
    });
  }

})();

//
// Icon code copy/paste
//

'use strict';

var CopyIcon = (function() {

  // Variables

  var $element = '.btn-icon-clipboard',
    $btn = $($element);


  // Methods

  function init($this) {
    $this.tooltip().on('mouseleave', function() {
      // Explicitly hide tooltip, since after clicking it remains
      // focused (as it's a button), so tooltip would otherwise
      // remain visible until focus is moved away
      $this.tooltip('hide');
    });

    var clipboard = new ClipboardJS($element);

    clipboard.on('success', function(e) {
      $(e.trigger)
        .attr('title', 'Copied!')
        .tooltip('_fixTitle')
        .tooltip('show')
        .attr('title', 'Copy to clipboard')
        .tooltip('_fixTitle')

      e.clearSelection()
    });
  }


  // Events
  if ($btn.length) {
    init($btn);
  }

})();

//
// Form control
//

'use strict';

var FormControl = (function() {

  // Variables

  var $input = $('.form-control');


  // Methods

  function init($this) {
    $this.on('focus blur', function(e) {
      $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
    }).trigger('blur');
  }


  // Events

  if ($input.length) {
    init($input);
  }

})();

//
// Google maps
//

var $map = $('#map-canvas'),
  map,
  lat,
  lng,
  color = "#5e72e4";

function initMap() {

  map = document.getElementById('map-canvas');
  lat = map.getAttribute('data-lat');
  lng = map.getAttribute('data-lng');

  var myLatlng = new google.maps.LatLng(lat, lng);
  var mapOptions = {
    zoom: 12,
    scrollwheel: false,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    styles: [{
      "featureType": "administrative",
      "elementType": "labels.text.fill",
      "stylers": [{
        "color": "#444444"
      }]
    }, {
      "featureType": "landscape",
      "elementType": "all",
      "stylers": [{
        "color": "#f2f2f2"
      }]
    }, {
      "featureType": "poi",
      "elementType": "all",
      "stylers": [{
        "visibility": "off"
      }]
    }, {
      "featureType": "road",
      "elementType": "all",
      "stylers": [{
        "saturation": -100
      }, {
        "lightness": 45
      }]
    }, {
      "featureType": "road.highway",
      "elementType": "all",
      "stylers": [{
        "visibility": "simplified"
      }]
    }, {
      "featureType": "road.arterial",
      "elementType": "labels.icon",
      "stylers": [{
        "visibility": "off"
      }]
    }, {
      "featureType": "transit",
      "elementType": "all",
      "stylers": [{
        "visibility": "off"
      }]
    }, {
      "featureType": "water",
      "elementType": "all",
      "stylers": [{
        "color": color
      }, {
        "visibility": "on"
      }]
    }]
  }

  map = new google.maps.Map(map, mapOptions);

  var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    animation: google.maps.Animation.DROP,
    title: 'Hello World!'
  });

  var contentString = '<div class="info-window-content"><h2>Argon Dashboard</h2>' +
    '<p>A beautiful Dashboard for Bootstrap 4. It is Free and Open Source.</p></div>';

  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map, marker);
  });
}

if ($map.length) {
  google.maps.event.addDomListener(window, 'load', initMap);
}

// //
// // Headroom - show/hide navbar on scroll
// //
//
// 'use strict';
//
// var Headroom = (function() {
//
// 	// Variables
//
// 	var $headroom = $('#navbar-main');
//
//
// 	// Methods
//
// 	function init($this) {
//
//     var headroom = new Headroom(document.querySelector("#navbar-main"), {
//         offset: 300,
//         tolerance: {
//             up: 30,
//             down: 30
//         },
//     });
//
//
//
// 	// Events
//
// 	if ($headroom.length) {
// 		headroom.init();
// 	}
//
// })();

//
// Navbar
//

'use strict';

var Navbar = (function() {

  // Variables

  var $nav = $('.navbar-nav, .navbar-nav .nav');
  var $collapse = $('.navbar .collapse');
  var $dropdown = $('.navbar .dropdown');

  // Methods

  function accordion($this) {
    $this.closest($nav).find($collapse).not($this).collapse('hide');
  }

  function closeDropdown($this) {
    var $dropdownMenu = $this.find('.dropdown-menu');

    $dropdownMenu.addClass('close');

    setTimeout(function() {
      $dropdownMenu.removeClass('close');
    }, 200);
  }


  // Events

  $collapse.on({
    'show.bs.collapse': function() {
      accordion($(this));
    }
  })

  $dropdown.on({
    'hide.bs.dropdown': function() {
      closeDropdown($(this));
    }
  })

})();


//
// Navbar collapse
//


var NavbarCollapse = (function() {

  // Variables

  var $nav = $('.navbar-nav'),
    $collapse = $('.navbar .collapse');


  // Methods

  function hideNavbarCollapse($this) {
    $this.addClass('collapsing-out');
  }

  function hiddenNavbarCollapse($this) {
    $this.removeClass('collapsing-out');
  }


  // Events

  if ($collapse.length) {
    $collapse.on({
      'hide.bs.collapse': function() {
        hideNavbarCollapse($collapse);
      }
    })

    $collapse.on({
      'hidden.bs.collapse': function() {
        hiddenNavbarCollapse($collapse);
      }
    })
  }

})();

//
// Form control
//

'use strict';

var noUiSlider = (function() {

  // Variables

  // var $sliderContainer = $('.input-slider-container'),
  // 		$slider = $('.input-slider'),
  // 		$sliderId = $slider.attr('id'),
  // 		$sliderMinValue = $slider.data('range-value-min');
  // 		$sliderMaxValue = $slider.data('range-value-max');;


  // // Methods
  //
  // function init($this) {
  // 	$this.on('focus blur', function(e) {
  //       $this.parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
  //   }).trigger('blur');
  // }
  //
  //
  // // Events
  //
  // if ($input.length) {
  // 	init($input);
  // }



  if ($(".input-slider-container")[0]) {
    $('.input-slider-container').each(function() {

      var slider = $(this).find('.input-slider');
      var sliderId = slider.attr('id');
      var minValue = slider.data('range-value-min');
      var maxValue = slider.data('range-value-max');

      var sliderValue = $(this).find('.range-slider-value');
      var sliderValueId = sliderValue.attr('id');
      var startValue = sliderValue.data('range-value-low');

      var c = document.getElementById(sliderId),
        d = document.getElementById(sliderValueId);

      noUiSlider.create(c, {
        start: [parseInt(startValue)],
        connect: [true, false],
        //step: 1000,
        range: {
          'min': [parseInt(minValue)],
          'max': [parseInt(maxValue)]
        }
      });

      c.noUiSlider.on('update', function(a, b) {
        d.textContent = a[b];
      });
    })
  }

  if ($("#input-slider-range")[0]) {
    var c = document.getElementById("input-slider-range"),
      d = document.getElementById("input-slider-range-value-low"),
      e = document.getElementById("input-slider-range-value-high"),
      f = [d, e];

    noUiSlider.create(c, {
      start: [parseInt(d.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
      connect: !0,
      range: {
        min: parseInt(c.getAttribute('data-range-value-min')),
        max: parseInt(c.getAttribute('data-range-value-max'))
      }
    }), c.noUiSlider.on("update", function(a, b) {
      f[b].textContent = a[b]
    })
  }

})();

//
// Popover
//

'use strict';

var Popover = (function() {

  // Variables

  var $popover = $('[data-toggle="popover"]'),
    $popoverClass = '';


  // Methods

  function init($this) {
    if ($this.data('color')) {
      $popoverClass = 'popover-' + $this.data('color');
    }

    var options = {
      trigger: 'focus',
      template: '<div class="popover ' + $popoverClass + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
    };

    $this.popover(options);
  }


  // Events

  if ($popover.length) {
    $popover.each(function() {
      init($(this));
    });
  }

})();

//
// Scroll to (anchor links)
//

'use strict';

var ScrollTo = (function() {

  //
  // Variables
  //

  var $scrollTo = $('.scroll-me, [data-scroll-to], .toc-entry a');


  //
  // Methods
  //

  function scrollTo($this) {
    var $el = $this.attr('href');
    var offset = $this.data('scroll-to-offset') ? $this.data('scroll-to-offset') : 0;
    var options = {
      scrollTop: $($el).offset().top - offset
    };

    // Animate scroll to the selected section
    $('html, body').stop(true, true).animate(options, 600);

    event.preventDefault();
  }


  //
  // Events
  //

  if ($scrollTo.length) {
    $scrollTo.on('click', function(event) {
      scrollTo($(this));
    });
  }

})();

//
// Tooltip
//

'use strict';

var Tooltip = (function() {

  // Variables

  var $tooltip = $('[data-toggle="tooltip"]');


  // Methods

  function init() {
    $tooltip.tooltip();
  }


  // Events

  if ($tooltip.length) {
    init();
  }

})();

//
// Orders chart
//

var OrdersChart = (function() {

  //
  // Variables
  //

  var $chart = $('#chart-orders');
  var $ordersSelect = $('[name="ordersSelect"]');


  //
  // Methods
  //

  // Init chart
  function initChart($chart) {

    // Create chart
    var ordersChart = new Chart($chart, {
      type: 'bar',
      options: {
        scales: {
          yAxes: [{
            gridLines: {
              lineWidth: 1,
              color: '#dfe2e6',
              zeroLineColor: '#dfe2e6'
            },
            ticks: {
              callback: function(value) {
                if (!(value % 10)) {
                  //return '$' + value + 'k'
                  return value
                }
              }
            }
          }]
        },
        tooltips: {
          callbacks: {
            label: function(item, data) {
              var label = data.datasets[item.datasetIndex].label || '';
              var yLabel = item.yLabel;
              var content = '';

              if (data.datasets.length > 1) {
                content += '<span class="popover-body-label mr-auto">' + label + '</span>';
              }

              content += '<span class="popover-body-value">' + yLabel + '</span>';

              return content;
            }
          }
        }
      },
      data: {
        labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
          label: 'Sales',
          data: [25, 20, 30, 22, 17, 29]
        }]
      }
    });

    // Save to jQuery object
    $chart.data('chart', ordersChart);
  }


  // Init chart
  if ($chart.length) {
    initChart($chart);
  }

})();

//
// Charts
//

//'use strict';

// //
// // Sales chart
// //
//
// var SalesChart = (function() {
//
//   // Variables
//
//   var $chart = $('#chart-sales');
//
//
//   // Methods
//
//   function init($chart) {
//
//     var salesChart = new Chart($chart, {
//       type: 'line',
//       options: {
//         scales: {
//           yAxes: [{
//             gridLines: {
//               lineWidth: 1,
//               color: Charts.colors.gray[900],
//               zeroLineColor: Charts.colors.gray[900]
//             },
//             ticks: {
//               callback: function(value) {
//                 if (!(value % 10)) {
//                   return '$' + value + 'k';
//                 }
//               }
//             }
//           }]
//         },
//         tooltips: {
//           callbacks: {
//             label: function(item, data) {
//               var label = data.datasets[item.datasetIndex].label || '';
//               var yLabel = item.yLabel;
//               var content = '';
//
//               if (data.datasets.length > 1) {
//                 content += '<span class="popover-body-label mr-auto">' + label + '</span>';
//               }
//
//               content += '<span class="popover-body-value">$' + yLabel + 'k</span>';
//               return content;
//             }
//           }
//         }
//       },
//       data: {
//         labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
//         datasets: [{
//           label: 'Performance',
//           data: [0, 20, 10, 30, 15, 40, 20, 60, 60]
//         }]
//       }
//     });
//
//     // Save to jQuery object
//
//     $chart.data('chart', salesChart);
//
//   };
//
//
//   // Events
//
//   if ($chart.length) {
//     init($chart);
//   }
//
// })();