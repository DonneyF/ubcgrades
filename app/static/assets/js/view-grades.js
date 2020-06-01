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

            populateYearSessionDrop();
        });
    });

    // Update the dropdown on all subsequent page loads. TODO: Maybe a better solution?
    function populateYearSessionDrop() {
        $('#vg-drop-year').prepend('<option></option>').select2({
            data: campus === "UBCV" ? YEARSESSIONS_UBCV.map(item => ({
                'id': item,
                'text': item
            })) : YEARSESSIONS_UBCO.map(item => ({'id': item, 'text': item})),
        }).on("select2:select", function (e) {
            yearsession = new YearSession($(this).select2('data')[0]['id']);
            apiVersion = yearsession.year < 2014 ? "v1" : "v2";
            updateVGSubjectDrop();
        });
    }

    if (campus != null) {
       populateYearSessionDrop();
    }

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
    function updateVGSubjectDrop() {
        $.ajax({
            url: `${API_HOST_URL}/api/${apiVersion}/subjects/${campus}/${yearsession}`,
            type: "GET",
            success: function (response) {
                updateVGDropdown('subject', response);
            },
            error: function () {
                displayError("Unable to connect to API");
            }
        });
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param subject is the 2 to 4 character subject code
     */
    function updateVGCourseDrop(subject) {
        $.ajax({
            url: `${API_HOST_URL}/api/${apiVersion}/courses/${campus}/${yearsession}/${subject}`,
            type: "GET",
            success: function (response) {
                updateVGDropdown('course', response);
            },
            error: function () {
                displayError("Unable to connect to API");
            }
        });
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param course is the 3 to 4 character course code
     */
    function updateVGSectionDrop(course) {
        let subject = $("#vg-drop-subject").select2('data')[0]['id'];
        $.ajax({
            url: `${API_HOST_URL}/api/${apiVersion}/sections/${campus}/${yearsession}/${subject}/${course}`,
            type: "GET",
            success: function (response) {
                updateVGDropdown('section', response);
            },
            error: function () {
                displayError("Unable to connect to API");
            }
        });
    }


    /**
     * Updates the dropdowns with the values
     * @param id is the CSS id of the dropdown
     * @param response is the API response data
     */
    function updateVGDropdown(id, response) {
        let dropdown = $(`#vg-drop-${id}`);

        // Populate the dropdown with the new data
        if (["subject", "course"].indexOf(id) >= 0) {
            let data;
            if (id === "course") {
                data = response.map(item => ({
                    'id': `${item['course']}${item['detail']}`,
                    'text': `${item['course']}${item['detail']} - ${item['course_title']}`
                }));
            } else {
                data = response.map(item => ({
                    'id': item[id],
                    'text': `${item[id]} - ${item[`${id}_title`]}`
                }))
            }
            dropdown.empty().prepend('<option></option>').select2({
                data: data,
                // Auto adjust the dropdown
                dropdownAutoWidth: true,
                // Display the ID instead of the value
                templateSelection: function (val) {
                    return val.id;
                }
            });
        } else {
            dropdown.empty().prepend('<option></option>').select2({
                data: response.map(item => ({'id': item, 'text': item})),
            });
        }
        // If the response contains only one element or the section is length 2 with OVERALL, automatically select it
        if (id === "section" && response.length === 2 && response.includes("OVERALL")) {
            // Find the entry that is not OVERALL
            dropdown.select2("trigger", "select", {
                data: {id: response.filter(x => x !== "OVERALL")[0]}
            });
            $('#vg-dropdown-form').submit();
        } else {
            // Open the dropdown
            dropdown.select2('open');
        }
    }

    /*-----------------------------------
    * Entry Points
    *-----------------------------------*/

    // Takes an input string and attempts to extract an array containing YEARSESSION, SUBJECT, COURSE, SECTION
    function parseViewGradesID(inputStr) {
        // Remove all non-character/numbers
        let stripped = inputStr.replace(/(?![A-Za-z0-9]+)./gi, "");
        // Split the result into four groups by regex. Index 0 contains the full match
        let results = stripped.match(/([0-9]{4}[A-Z])([A-Z]+?(?=[0-9]))([0-9]{3}[A-Z]?)([0-9]{1,3})/i);

        if (results == null || results.length !== 5) return false;

        return results.slice(1, 5).map(str => str.toUpperCase());
    }

    // Entry via ID
    $("#vg-id-form").on('submit',function () {
        let idSplit = parseViewGradesID($('#vg-id-form input').val());
        if (idSplit === false) {
            displayError("Invalid ID. Check again.");
        } else {
            yearsession = new YearSession(idSplit[0]);
            apiVersion = yearsession.year < 2014 ? "v1" : "v2";
            getSectionGrades('#vg-id-submit', idSplit[0], idSplit[1], idSplit[2], idSplit[3]);
        }
        return false;
    });

    // Entry via dropdowns
    $("#vg-dropdown-form").on('submit',function () {
        // Selectively show row based on desired year
        getSectionGrades('#vg-dropdown-submit', yearsession, $('#vg-drop-subject').val(),
            $('#vg-drop-course').val(), $('#vg-drop-section').val());

        return false; // Don't refresh the page.
    });

    /**
     * Displays the grade card depending on api version and show the container if first submission
     */
    function displayContentContainer() {
        if (yearsession.year < 2014) {
            $('#tableau-dashboard-row').addClass('d-none');
            $('#pair-reports-row').removeClass('d-none');
        } else {
            $('#tableau-dashboard-row').removeClass('d-none');
            $('#pair-reports-row').addClass('d-none');
        }

        if ($('#content-container').hasClass("collapse")) {
            setTimeout(function () {
                $('#content-container').collapse();
            }, 250);
        }
    }

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

        // Retrieve the data
        $.ajax({
            url: `${API_HOST_URL}/api/${apiVersion}/grades/${campus}/${yearsession}/${subject}/${course}/${section}`,
            type: "GET",
            success: function (response) {
                if (apiVersion === "v1") updateGradeDatav1(response);
                else updateGradeDatav2(response);

                // Get the most recent sessions and update
                $.ajax({
                    url: `${API_HOST_URL}/api/recent-section-averages/${campus}/${subject}/${course}`,
                    type: "GET",
                    success: function (response) {
                        updateRecentSectionGrades(response);
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

    /*-----------------------------------
    * Data Callbacks
    *-----------------------------------*/

    function updateGradeDatav1(data) {
        // Update the card header
        $('#pair-reports-row .card-header h3').text(`${data['campus']} ${data['year']}${data['session']} ${data['subject']} ${data['course']}${data['detail']} ${data['section']}`);
        $('#pair-reports-row .card-header h2').text(data['course_title']);
        // Update the headmatter
        $('#vg-headmatter-v1 h2').each(function (index) {
            // Find each h2 and update
            let headmatter_entry = $(this);
            if (headmatter_entry != null) {
                let number = data[HEADMATTER_V1_KEYS[index]];
                if (number % 1 === 0) {
                    // number_string is a int
                    headmatter_entry.text(number);
                } else {
                    headmatter_entry.text(parseFloat(number).toFixed(2));
                }
            }
        });

        // Update the grades table
        $('#grades-v1 span').each(function (index) {
            $(this).text(data['grades'][GRADES_V1[index]]);
        });

        // Update the teaching team
        $("#teaching-team-v1").text(data['professor'].replace(/;/gi, ", "));

        // Update the chart
        $('#chart-grades-toggles').hide();
        updateGradesChart(data);
    }

    function updateGradeDatav2(data) {
        // Update the card header
        $('#tableau-dashboard-row .card-header h3').text(`${data['campus']} ${data['year']}${data['session']} ${data['subject']} ${data['course']}${data['detail']} ${data['section']}`);
        $('#tableau-dashboard-row .card-header h2').text(data['course_title']);
        // Update the headmatter
        $('#vg-headmatter-v2 h2').each(function (index) {
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
        $('#chart-grades-toggles').show();
        updateGradesChart(data);
    }

    // Update the card showing the most recent grades
    function updateRecentSectionGrades(data) {
        $('#recent-section-averages .card-body .row').empty();
        data.reverse();
        data.forEach(function (entry) {
            $('#recent-section-averages .card-body .row').append('<div class="col">' +
                `<h5 class="text-uppercase text-muted ls-1 mb-1">${entry['year']}${entry['session']} - ${entry['section']}</h5>` +
                `<h2 class="mb-0">${parseFloat(entry['average']).toFixed(2)}</h2></div>`)
        });
    }

    let sectionGradesChart;

    function updateGradesChart(apiResponseData) {
        let gradeData = apiVersion === "v1" ? GRADES_V1.map(x => apiResponseData['grades'][x]) : GRADES_V2.map(x => apiResponseData['grades'][x]);
        let $chart = $('#chart-grades');

        //if (sectionGradesChart == null) {
        if (sectionGradesChart) sectionGradesChart.destroy();
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
                labels: apiVersion === "v1" ? GRADES_V1.slice(0) : GRADES_V2.slice(0),
                datasets: [{
                    data: gradeData
                }]
            }
        });
        // Save to jQuery object

        $chart.data('chart', sectionGradesChart);
    }

});