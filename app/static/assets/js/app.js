const YEARSESSIONS = ['2019S', '2018W', '2018S', '2017W', '2017S', '2016W', '2016S', '2015W', '2015S', '2014W', '2014S', '2013W', '2013S', '2012W', '2012S', '2011W', '2011S', '2010W', '2010S', '2009W', '2009S', '2008W', '2008S', '2007W', '2007S', '2006W', '2006S', '2005W', '2005S', '2004W', '2004S', '2003W', '2003S', '2002W', '2002S', '2001W', '2001S', '2000W', '2000S', '1999W', '1999S', '1998W', '1998S', '1997W', '1997S', '1996W', '1996S']
const HEADMATTER_V1 = ["Average", "Stdev", "High", "Low", "Pass", "Fail", "Enrolled", "Withdrew", "Audit", "Other"]
const HEADMATTER_V2_KEYS = ["average", "stdev", "high", "low", "enrolled"]
const GRADES_V2 = ["<50%", "50-54%", "55-59%", "60-63%", "64-67%", "68-71%", "72-75%", "76-79%", "80-84%", "85-89%", "90-100%"]
const API_HOST_URL = "http://localhost:5000"

'use strict';

$(function () {

    /*-----------------------------------
    * Dropdowns
    *-----------------------------------*/
    // Initialize dropdowns. A prepend is needed since the browser automatically selects the first value
    $('#vg-drop-year').prepend('<option></option>').select2({
        data: YEARSESSIONS.map(item => ({'id': item, 'text': item})),
    }).on("select2:select", function (e) {
        updateVGSubjectDrop($(this).select2('data')[0]['id']);
    });

    $('#vg-drop-subject').select2().on("select2:select", function (e) {
        updateVGCourseDrop($(this).select2('data')[0]['id']);
    });

    $('#vg-drop-course').select2().on("select2:select", function (e) {
        updateVGSectionDrop($(this).select2('data')[0]['id']);
    });

    $('#vg-drop-section').select2();


    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param yearsession a 5 character yearsession code.
     */
    function updateVGSubjectDrop(yearsession) {
        $.ajax({
            url: `${API_HOST_URL}/api/v2/subjects/UBCV/${yearsession}`,
            type: "GET",
            success: function (response) {
                updateSVDropdown('#vg-drop-subject', response);
            },
            error: function () {
                // TODO
            }
        });
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param subject is the 2 to 4 character subject code
     */
    function updateVGCourseDrop(subject) {
        let yearsession = $("#vg-drop-year").select2('data')[0]['id'];
        $.ajax({
            url: `${API_HOST_URL}/api/v2/courses/UBCV/${yearsession}/${subject}`,
            type: "GET",
            success: function (response) {
                updateSVDropdown('#vg-drop-course', response);
            },
            error: function () {
                // TODO
            }
        });
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param course is the 3 to 4 character course code
     */
    function updateVGSectionDrop(course) {
        let yearsession = $("#vg-drop-year").select2('data')[0]['id'];
        let subject = $("#vg-drop-subject").select2('data')[0]['id'];
        $.ajax({
            url: `${API_HOST_URL}/api/v2/sections/UBCV/${yearsession}/${subject}/${course}`,
            type: "GET",
            success: function (response) {
                updateSVDropdown('#vg-drop-section', response);
            },
            error: function () {
                // TODO
            }
        });
    }

    /**
     * Updates the dropdowns with the values
     * @param id is the CSS id of the dropdown
     * @param response is the API response data
     */
    function updateSVDropdown(id, response) {
        let dropdown = $(id);

        // Populate the dropdown with the new data
        dropdown.empty().prepend('<option></option>').select2({
            data: response.map(item => ({'id': item, 'text': item})),
        });
        // If the response contains only one element or the section is length 2 with OVERALL, automatically select it
        if (id === "#vg-drop-section" && response.length === 2 && response.includes("OVERALL")) {
            // Find the entry that is not OVERALL
            dropdown.select2("trigger", "select", {
                data: {id: response.filter(x => x !== "OVERALL")[0]}
            });
        } else {
            // Open the dropdown
            dropdown.select2('open');
        }
    }

    /*-----------------------------------
    * Entry Points
    *-----------------------------------*/

    // Takes an input string and attempts to extract an array containing YEARSESSION, SUBJECT, COURSE, SECTION
    function parseSVID(inputStr) {
        // Remove all non-character/numbers
        let stripped = inputStr.replace(/(?![A-Za-z0-9]+)./gi, "");
        // Split the result into four groups by regex. Index 0 contains the full match
        let results = stripped.match(/([0-9]{4}[A-Z])([A-Z]+?(?=[0-9]))([0-9]{3}[A-Z]?)([0-9]{1,3})/i)

        if (results.length !== 5) return false;

        return results.slice(1, 5).map(str => str.toUpperCase());
    }

    $("#vg-form").submit(function () {
        let yearsession = $('#vg-drop-year').val();
        getSectionGrades('#vg-btn-submit', yearsession, $('#vg-drop-subject').val(), $('#vg-drop-course').val(), $('#vg-drop-section').val());

        // Selectively show row based on desired year
        if (parseInt(yearsession.substring(0, 4)) < 2014) {
            $('#tableau-dashboard-row').addClass('d-none');
            $('#pair-reports-row').removeClass('d-none');
        } else {
            $('#tableau-dashboard-row').removeClass('d-none');
            $('#pair-reports-row').addClass('d-none');
        }

        // If first submission show the data
        if ($('#grade-container').hasClass("collapse")) {
            setTimeout(function () {
                $('#grade-container').collapse();
            }, 250);
        }
        return false; // Don't refresh the page.
    });

    /*-----------------------------------
    * API submission
    *-----------------------------------*/
    function getSectionGrades(button, yearsession, subject, course, section) {
        let $button = $(button);
        let loadingText = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
        if ($button.html() !== loadingText) {
            // Store original text
            $button.data('original-text', $button.html());
            // Set disabled state for button
            $button.addClass('disabled');
            // Set loading text
            $button.html(loadingText);
        }
        // Send API request synchronously
        $.ajax({
            url: `${API_HOST_URL}/api/v2/grades/UBCV/${yearsession}/${subject}/${course}/${section}`,
            type: "GET",
            success: function (response) {
                updateGradeData(response);
                $button.html($button.data('original-text'));
                $button.removeClass('disabled');
            },
            error: function (response) {
                // TODO
            }
        });
    }

    /*-----------------------------------
    * Data Callbacks
    *-----------------------------------*/

    function updateGradeData(data) {
        // Update the card header
        $('#card-header h3').text(`${data['campus']} ${data['year']}${data['session']} ${data['subject']} ${data['course']} ${data['section']}`);
        $('#card-header h2').text(data['title']);
        // Update the headmatter
        $('#vg-headmatter-v1 h2').each(function (index) {
            // Find each h2 and update
            let headmatter_entry = $(this);
            if (headmatter_entry != null) {
                let number = data[HEADMATTER_V2_KEYS[index]];
                if (number % 1 === 0) {
                    // number_string is a int
                    headmatter_entry.text(number);
                } else {
                    headmatter_entry.text(parseFloat(number).toFixed(2));
                }
            }
        });

        // Update the grades table
        $('#grades-v2 span').each(function (index) {
            $(this).text(data['grades'][GRADES_V2[index]]);
        });

        // Update the teaching team
        $("#teaching-team-v2").text(data['professor'].replace(/;/gi, ", "));

        // Update the chart
        updateGradesChart(data);
    }

    let sectionGradesChart;
    function updateGradesChart(apiResponseData) {
        let gradeData = GRADES_V2.map(x => apiResponseData['grades'][x]);
        let $chart = $('#chart-grades');

        if (sectionGradesChart == null) {
            sectionGradesChart = new Chart($chart, {
                type: 'bar',
                options: {
                    scales: {
                        yAxes: [{
                            gridLines: {
                                lineWidth: 1,
                                color: Charts.colors.gray[900],
                                zeroLineColor: Charts.colors.gray[900]
                            }
                        }]
                    },
                    tooltips: {
                        callbacks: {
                            label: function (item, data) {
                                let label = data.datasets[item.datasetIndex].label || '';
                                let content = '';
                                if (data.datasets.length > 1) {
                                    content += `<span class="popover-body-label mr-auto">${label}</span>`;
                                }

                                // Distinguish between entries with 0 values and no data
                                if (gradeData[item.index] !== "") {
                                    content += `<span class="popover-body-value">${item.yLabel}</span>`;
                                } else {
                                    content += `<span class="popover-body-value">No Data</span>`;
                                }
                                return content;
                            }
                        }
                    }
                },
                data: {
                    labels: GRADES_V2,
                    datasets: [{
                        data: gradeData
                    }]
                }
            });
        } else {
            // Replace the data and update
            sectionGradesChart.data.datasets[0].data = gradeData;
            sectionGradesChart.update();
        }

        // Save to jQuery object

        $chart.data('chart', sectionGradesChart);

    }

});


//
// Charts
//

'use strict';

var Charts = (function () {

    // Variable

    var $toggle = $('[data-toggle="chart"]');
    var mode = 'light'; //(themeMode) ? themeMode : 'light';
    var fonts = {
        base: 'Open Sans'
    }

    // Colors
    var colors = {
        gray: {
            100: '#f6f9fc',
            200: '#e9ecef',
            300: '#dee2e6',
            400: '#ced4da',
            500: '#adb5bd',
            600: '#8898aa',
            700: '#525f7f',
            800: '#32325d',
            900: '#212529'
        },
        theme: {
            'default': '#172b4d',
            'primary': '#5e72e4',
            'secondary': '#f4f5f7',
            'info': '#11cdef',
            'success': '#2dce89',
            'danger': '#f5365c',
            'warning': '#fb6340'
        },
        black: '#12263F',
        white: '#FFFFFF',
        transparent: 'transparent',
    };


    // Methods

    // Chart.js global options
    function chartOptions() {

        // Options
        var options = {
            defaults: {
                global: {
                    responsive: true,
                    maintainAspectRatio: false,
                    defaultColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
                    defaultFontColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
                    defaultFontFamily: fonts.base,
                    defaultFontSize: 13,
                    layout: {
                        padding: 0
                    },
                    legend: {
                        display: false,
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 16
                        }
                    },
                    elements: {
                        point: {
                            radius: 0,
                            backgroundColor: colors.theme['primary']
                        },
                        line: {
                            tension: .4,
                            borderWidth: 4,
                            borderColor: colors.theme['primary'],
                            backgroundColor: colors.transparent,
                            borderCapStyle: 'rounded'
                        },
                        rectangle: {
                            backgroundColor: colors.theme['warning']
                        },
                        arc: {
                            backgroundColor: colors.theme['primary'],
                            borderColor: (mode == 'dark') ? colors.gray[800] : colors.white,
                            borderWidth: 4
                        }
                    },
                    tooltips: {
                        enabled: false,
                        mode: 'index',
                        intersect: false,
                        custom: function (model) {

                            // Get tooltip
                            var $tooltip = $('#chart-tooltip');

                            // Create tooltip on first render
                            if (!$tooltip.length) {
                                $tooltip = $('<div id="chart-tooltip" class="popover bs-popover-top" role="tooltip"></div>');

                                // Append to body
                                $('body').append($tooltip);
                            }

                            // Hide if no tooltip
                            if (model.opacity === 0) {
                                $tooltip.css('display', 'none');
                                return;
                            }

                            function getBody(bodyItem) {
                                return bodyItem.lines;
                            }

                            // Fill with content
                            if (model.body) {
                                var titleLines = model.title || [];
                                var bodyLines = model.body.map(getBody);
                                var html = '';

                                // Add arrow
                                html += '<div class="arrow"></div>';

                                // Add header
                                titleLines.forEach(function (title) {
                                    html += '<h3 class="popover-header text-center">' + title + '</h3>';
                                });

                                // Add body
                                bodyLines.forEach(function (body, i) {
                                    var colors = model.labelColors[i];
                                    var styles = 'background-color: ' + colors.backgroundColor;
                                    //var indicator = '<span class="badge badge-dot"><i class="bg-primary"></i></span>';
                                    var align = (bodyLines.length > 1) ? 'justify-content-left' : 'justify-content-center';
                                    html += '<div class="popover-body d-flex align-items-center ' + align + '">' + body + '</div>';
                                });

                                $tooltip.html(html);
                            }

                            // Get tooltip position
                            var $canvas = $(this._chart.canvas);

                            var canvasWidth = $canvas.outerWidth();
                            var canvasHeight = $canvas.outerHeight();

                            var canvasTop = $canvas.offset().top;
                            var canvasLeft = $canvas.offset().left;

                            var tooltipWidth = $tooltip.outerWidth();
                            var tooltipHeight = $tooltip.outerHeight();

                            var top = canvasTop + model.caretY - tooltipHeight - 16;
                            var left = canvasLeft + model.caretX - tooltipWidth / 2;

                            // Display tooltip
                            $tooltip.css({
                                'top': top + 'px',
                                'left': left + 'px',
                                'display': 'block',
                                'z-index': '100'
                            });

                        },
                        callbacks: {
                            label: function (item, data) {
                                var label = data.datasets[item.datasetIndex].label || '';
                                var yLabel = item.yLabel;
                                var content = '';

                                if (data.datasets.length > 1) {
                                    content += '<span class="badge badge-primary mr-auto">' + label + '</span>';
                                }

                                content += '<span class="popover-body-value">' + yLabel + '</span>';
                                return content;
                            }
                        }
                    }
                },
                doughnut: {
                    cutoutPercentage: 83,
                    tooltips: {
                        callbacks: {
                            title: function (item, data) {
                                var title = data.labels[item[0].index];
                                return title;
                            },
                            label: function (item, data) {
                                var value = data.datasets[0].data[item.index];
                                var content = '';

                                content += '<span class="popover-body-value">' + value + '</span>';
                                return content;
                            }
                        }
                    },
                    legendCallback: function (chart) {
                        var data = chart.data;
                        var content = '';

                        data.labels.forEach(function (label, index) {
                            var bgColor = data.datasets[0].backgroundColor[index];

                            content += '<span class="chart-legend-item">';
                            content += '<i class="chart-legend-indicator" style="background-color: ' + bgColor + '"></i>';
                            content += label;
                            content += '</span>';
                        });

                        return content;
                    }
                }
            }
        }

        // yAxes
        Chart.scaleService.updateScaleDefaults('linear', {
            gridLines: {
                borderDash: [2],
                borderDashOffset: [2],
                color: (mode == 'dark') ? colors.gray[900] : colors.gray[300],
                drawBorder: false,
                drawTicks: false,
                lineWidth: 0,
                zeroLineWidth: 0,
                zeroLineColor: (mode == 'dark') ? colors.gray[900] : colors.gray[300],
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2]
            },
            ticks: {
                beginAtZero: true,
                padding: 10,
                callback: function (value) {
                    if (!(value % 10)) {
                        return value
                    }
                }
            }
        });

        // xAxes
        Chart.scaleService.updateScaleDefaults('category', {
            gridLines: {
                drawBorder: false,
                drawOnChartArea: false,
                drawTicks: false
            },
            ticks: {
                padding: 20
            },
            maxBarThickness: 10
        });

        return options;

    }

    // Parse global options
    function parseOptions(parent, options) {
        for (var item in options) {
            if (typeof options[item] !== 'object') {
                parent[item] = options[item];
            } else {
                parseOptions(parent[item], options[item]);
            }
        }
    }

    // Push options
    function pushOptions(parent, options) {
        for (var item in options) {
            if (Array.isArray(options[item])) {
                options[item].forEach(function (data) {
                    parent[item].push(data);
                });
            } else {
                pushOptions(parent[item], options[item]);
            }
        }
    }

    // Pop options
    function popOptions(parent, options) {
        for (var item in options) {
            if (Array.isArray(options[item])) {
                options[item].forEach(function (data) {
                    parent[item].pop();
                });
            } else {
                popOptions(parent[item], options[item]);
            }
        }
    }

    // Toggle options
    function toggleOptions(elem) {
        var options = elem.data('add');
        var $target = $(elem.data('target'));
        var $chart = $target.data('chart');

        if (elem.is(':checked')) {

            // Add options
            pushOptions($chart, options);

            // Update chart
            $chart.update();
        } else {

            // Remove options
            popOptions($chart, options);

            // Update chart
            $chart.update();
        }
    }

    // Update options
    function updateOptions(elem) {
        var options = elem.data('update');
        var $target = $(elem.data('target'));
        var $chart = $target.data('chart');

        // Parse options
        parseOptions($chart, options);

        // Toggle ticks
        toggleTicks(elem, $chart);

        // Update chart
        $chart.update();
    }

    // Toggle ticks
    function toggleTicks(elem, $chart) {

        if (elem.data('prefix') !== undefined || elem.data('prefix') !== undefined) {
            var prefix = elem.data('prefix') ? elem.data('prefix') : '';
            var suffix = elem.data('suffix') ? elem.data('suffix') : '';

            // Update ticks
            $chart.options.scales.yAxes[0].ticks.callback = function (value) {
                if (!(value % 10)) {
                    return prefix + value + suffix;
                }
            }

            // Update tooltips
            $chart.options.tooltips.callbacks.label = function (item, data) {
                var label = data.datasets[item.datasetIndex].label || '';
                var yLabel = item.yLabel;
                var content = '';

                if (data.datasets.length > 1) {
                    content += '<span class="popover-body-label mr-auto">' + label + '</span>';
                }

                content += '<span class="popover-body-value">' + prefix + yLabel + suffix + '</span>';
                return content;
            }

        }
    }


    // Events

    // Parse global options
    if (window.Chart) {
        parseOptions(Chart, chartOptions());
    }

    // Toggle options
    $toggle.on({
        'change': function () {
            var $this = $(this);

            if ($this.is('[data-add]')) {
                toggleOptions($this);
            }
        },
        'click': function () {
            var $this = $(this);

            if ($this.is('[data-update]')) {
                updateOptions($this);
            }
        }
    });


    // Return

    return {
        colors: colors,
        fonts: fonts,
        mode: mode
    };

})();