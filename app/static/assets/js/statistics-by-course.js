'use strict';

$(function () {

    /*-----------------------------------
    * Campus Selector and Dropdowns
    *-----------------------------------*/

    // Campus modal handler
    $('#campusModal .modal-body button').on('click', function (event) {
        // Find the button that caused the modal to close and update the campus
        let $button = $(event.target);
        $(this).closest('.modal').one('hidden.bs.modal', function () {
            localStorage.setItem("campus", $button.data('campus'));
            campus = localStorage.getItem("campus");

            populateSubjectDrop();
        });
    });

    function populateSubjectDrop() {
        // Restrict lookup to courses offered in the past 5 years
        $.ajax({
            url: `${API_HOST_URL}/api/v2/subjects/${campus}`,
            type: "GET",
            success: function (response) {
                let data = response.map(item => ({
                    'id': item['subject'],
                    'text': `${item['subject']} - ${item['subject_title']}`
                }));
                $('#sc-drop-subject').prepend('<option></option>').select2({
                    data: data,
                    // // Auto adjust the dropdown
                    dropdownAutoWidth: true,
                    // // Display the ID instead of the value
                    templateSelection: function (val) {
                        return val.text === 'Subject' ? val.text : val.id; // Manual placeholder override as it has
                    }
                }).on("select2:select", function (e) {
                    updateCourseDropdown($(this).select2('data')[0]['id']);
                });
            },
            error: function () {
                displayError("Unable to connect to API");
            }
        });
    }

    if (campus != null) {
        // If the campus is already filled, automatically load the subjects
        populateSubjectDrop();
    }

    $('#sc-drop-course').select2();

    function updateCourseDropdown(subject) {
        $.ajax({
            url: `${API_HOST_URL}/api/v2/courses/${campus}/${subject}`,
            type: "GET",
            success: function (response) {
                let data = response.map(item => ({
                    'id': `${item['course']}${item['detail']}`,
                    'text': `${item['course']}${item['detail']} - ${item['course_title']}`
                }));
                $('#sc-drop-course').empty().prepend('<option selected=""></option>').select2({
                    data: data,
                    // Auto adjust the dropdown
                    dropdownAutoWidth: true,
                    // Display the ID instead of the value
                    templateSelection: function (val) {
                        return val.id;
                    }
                }).on('select2:select', function(e) {
                    $('#sc-dropdown-form').submit();
                }).select2('open');
            },
            error: function () {
                displayError("Unable to connect to API");
            }
        });
    }


    /*-----------------------------------
    * Entry Points
    *-----------------------------------*/

    // Takes an input string and attempts to extract an array containing YEARSESSION, SUBJECT, COURSE, SECTION
    function parseStatisticsByCourseID(inputStr) {
        // Remove all non-character/numbers
        let stripped = inputStr.replace(/(?![A-Za-z0-9]+)./gi, "");
        // Split the result into four groups by regex. Index 0 contains the full match
        let results = stripped.match(/([A-Z]+?(?=[0-9]))([0-9]{3}[A-Z]?)/i);

        if (results == null || results.length !== 3) return false;

        return results.slice(1, 3).map(str => str.toUpperCase());
    }

    // Entry via ID
    $("#sc-id-form").on('submit', function () {
        let idSplit = parseStatisticsByCourseID($('#vg-id-form input').val());
        if (idSplit === false) {
            displayError("Invalid ID. Check again.");
        } else {
            getCourseStatistics('#sc-id-submit', idSplit[0], idSplit[1]);
        }
        return false;
    });

    // Entry via dropdowns
    $("#sc-dropdown-form").on('submit', function () {
        // Selectively show row based on desired year
        getCourseStatistics('#sc-dropdown-submit', $('#sc-drop-subject').val(), $('#sc-drop-course').val());

        return false; // Don't refresh the page.
    });

    function displayContentContainer() {
        let $content = $('#content-container')
        if ($content.hasClass("collapse")) {
            setTimeout(function () {
                $content.collapse();
                // Scroll user to the container
                // $([document.documentElement, document.body]).animate({
                //     scrollTop: $content.offset().top - 25
                // }, 500);
            }, 250);
        }
    }

    function getCourseStatistics(button, subject, course) {
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

        // Retrieve the data
        $.ajax({
            url: `${API_HOST_URL}/api/v2/course-statistics/${campus}//${subject}/${course}`,
            type: "GET",
            success: function (response) {
                updateCourseHeadmatter(response);

                // Retrieve historical averages
                $.ajax({
                    url: `${API_HOST_URL}/api/v2/course-statistics/average-history/${campus}/${subject}/${course}`,
                    type: "GET",
                    success: function (response) {
                        updateHistoricalAveragesChart(response);
                    }
                });

                // Retrieve professors
                $.ajax({
                    url: `${API_HOST_URL}/api/v2/course-statistics/teaching-team/${campus}/${subject}/${course}`,
                    type: "GET",
                    success: function (response) {
                        updateTeachingTeamTable(response);
                        $('#teaching-team h3').text(`${subject} ${course} Teaching Team`);
                    }
                });

                displayContentContainer();
            },
            error: function (response) {
                if (response.status === 404) displayError('Invalid ID, or ID does not exist.');
                else displayError("Unable to connect to API");
            },
            complete: function () {
                $button.html($button.data('original-text'));
                $button.removeClass('disabled');
            }
        });
    }

    function updateCourseHeadmatter(data) {
        // Update the card header
        $('#sc-row .card-header h3').text(`${data['campus']}  ${data['subject']} ${data['course']}${data['detail']}`);
        $('#sc-row .card-header h2').text(data['course_title']);
        // Update the headmatter
        let elements_h2 = $('#sc-headmatter h2');
        $(elements_h2[0]).text(parseFloat(data['average']).toFixed(2));
        $(elements_h2[1]).text(parseFloat(data['average_past_5_yrs'].toFixed(2)));
        $(elements_h2[2]).text(parseFloat(data['max_course_avg'].toFixed(2)));
        $(elements_h2[3]).text(parseFloat(data['min_course_avg'].toFixed(2)));

        // // Update the chart
        // $('#chart-grades-toggles').show();
    }

    let historicalAveragesChart;

    function updateHistoricalAveragesChart(apiResponseData) {
        let avgHistData = apiResponseData;
        Object.entries(avgHistData).forEach(function(ele) {
            const [key, value] = ele;
            if (value === '') {
                delete avgHistData[key];
            }
        });
        delete avgHistData['campus'];
        delete avgHistData['course'];
        delete avgHistData['detail'];
        delete avgHistData['subject'];
        let chartValues = Object.values(avgHistData);

        // Update the 5 Years/All Years switcher
        let recentValues = [], recentLabels = [];
        YEARSESSIONS_RECENT.slice().reverse().forEach(function(yearsession) {
            if (yearsession in avgHistData) {
                recentValues.push(avgHistData[yearsession]);
                recentLabels.push(yearsession);
            }
        })

        $('#five-years-toggle').on('click', function () {
            historicalAveragesChart.data.labels = recentLabels;
            historicalAveragesChart.data.datasets[0].data = recentValues;
            historicalAveragesChart.update();
        });

        $('#all-years-toggle').on('click', function () {
            historicalAveragesChart.data.labels = Object.keys(avgHistData)
            historicalAveragesChart.data.datasets[0].data = chartValues
            historicalAveragesChart.update();
        });
        
        let $chart = $('#chart-course-avg-hist');

        if (historicalAveragesChart) historicalAveragesChart.destroy();
        historicalAveragesChart = new Chart($chart, {
            type: 'line',
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
                            if (chartValues[item.index] !== '') {
                                content += `<span class="popover-body-value">${parseFloat(item.yLabel).toFixed(2)}</span>`;
                            } else {
                                content += `<span class="popover-body-value">No Data</span>`;
                            }
                            return content;
                        }
                    }
                }
            },
            data: {
                labels: Object.keys(avgHistData),
                datasets: [{
                    pointRadius: 5,
                    data: chartValues
                }]
            }
        });
        // Save to jQuery object

        $chart.data('chart', historicalAveragesChart);
    }

    // Init data table
    let teachingTeamTable = $('#teaching-team table').DataTable({
        columns: [
            { title: "Instructor or TA" , className: 'font-weight-bold'},
            { title: "YearSessions Active" },
        ],
        keys: !0,
        select: {
            style: "multi"
        },
        language: {
            paginate: {
                previous: "<i class='fas fa-angle-left'>",
                next: "<i class='fas fa-angle-right'>"
            }
        },
        style_cell: {
            'whiteSpace': 'normal',
            'height': 'auto',
        },
    });

    function updateTeachingTeamTable(apiResp) {
        // Parse the API response to map an instructor/TA to yearsessions they were active
        // Format needs to be array of arrays for datatables
        let teachingTeam = [];
        apiResp.forEach(function(ele) {
            if (ele['name'] === '') return;
            let activeSessions = [];
            Object.entries(ele).forEach(function (person) {
                const [key, value] = person;
                if (typeof value == 'number') {
                    activeSessions.push(key);
                }
            })
            // To string
            teachingTeam.push([ele['name'], activeSessions.join(', ')])
        });

        // Update the table
        teachingTeamTable.clear();
        teachingTeamTable.rows.add(teachingTeam);
        teachingTeamTable.draw();
    }
});