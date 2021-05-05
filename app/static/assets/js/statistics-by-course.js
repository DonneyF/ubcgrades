'use strict';

$(function () {

    /**
     * Similar to the state machine for viewing grades, but much simpler
     * since we only care about two variables.
     */
    function StateHandler() {
        let _subject;
        let _course;
        let _synchronizing = false;

        let updateOrder = [
            "subject",
            "course",
        ]

        let constructHash = () => {
            return `${_subject}-${_course}`;
        };

        this.updateSubject = async (subject) => {
            _subject = subject;
            if (!_synchronizing) {
                // Reset the course so we get the dropdown
                _course = null;
            }
            updateCourseDropdown(subject, _course);
        };

        this.updateCourse = async (course) => {
            _course = course;
            this.updateState();
            $('#sc-dropdown-form').submit();
        };

        this.updateState = () => {
            _synchronizing = false;
            window.location.hash = constructHash();
        };

        this.resetState = () => {
            _synchronizing = false;
            let data = [null, null];
            [_subject, _course] = data;
            for (let i = 0; i < data.length; i++) {
                $(`#sc-drop-${updateOrder[i]}`).val(data[i]).trigger("change");
            }
            window.history.replaceState(undefined, undefined, " ");
        };

        this.synchronizeState = () => {
            _synchronizing = true;
            let fragments = window.location.hash.substring(1).split("-");
            if (fragments.length === 2) {
                [_subject, _course] = fragments;
                $("#sc-drop-subject").select2("trigger", "select", {
                    data: {
                        id: _subject,
                    }
                });
            } else {
                this.resetState();
            }
        };

        this.init = () => {
            if (window.location.hash) {
                this.synchronizeState();
            }
        };

        window.addEventListener("hashchange", () => {
            if (constructHash() !== window.location.hash.substring(1)) {
                this.synchronizeState();
            }
        });
    }

    let stateHandler = new StateHandler();
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
                });
                stateHandler.init();
            },
            error: function () {
                displayError("Unable to connect to API");
            }
        });
    }

    $('#sc-drop-subject').select2().on("select2:select", function (e) {
        stateHandler.updateSubject($(this).select2('data')[0]['id']);
    });

    $('#sc-drop-course').select2().on('select2:select', function(e) {
        stateHandler.updateCourse($(this).select2('data')[0]['id']);
    });

    if (campus != null) {
        // If the campus is already filled, automatically load the subjects
        populateSubjectDrop();
    }

    function updateCourseDropdown(subject, previousCourse) {
        $.ajax({
            url: `${API_HOST_URL}/api/v2/courses/${campus}/${subject}`,
            type: "GET",
            success: function (response) {
                let data = response.map(item => ({
                    'id': `${item['course']}${item['detail']}`,
                    'text': `${item['course']}${item['detail']} - ${item['course_title']}`
                }));
                let dropdown = $('#sc-drop-course');
                dropdown.empty().prepend('<option selected=""></option>').select2({
                    data: data,
                    // Auto adjust the dropdown
                    dropdownAutoWidth: true,
                    // Display the ID instead of the value
                    templateSelection: function (val) {
                        return val.id;
                    }
                });
                if (!previousCourse) {
                    dropdown.select2("open");
                } else {
                    dropdown.select2("trigger", "select", {
                        data: {
                            id: previousCourse,
                        }
                    });
                }
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
                        $('#teaching-team h2').text(`${subject} ${course} Teaching Team`);
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
        let avgHistData = apiResponseData['yearsessions'];
        Object.entries(avgHistData).forEach(function(ele) {
            const [key, value] = ele;
            if (value === null) {
                delete avgHistData[key];
            }
        });
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
            // To string and push to datatable
            teachingTeam.push([ele['name'], Object.keys(ele['yearsessions']).join(', ')])
        });

        // Update the table
        teachingTeamTable.clear();
        teachingTeamTable.rows.add(teachingTeam);
        teachingTeamTable.draw();
    }
});