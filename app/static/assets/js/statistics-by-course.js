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
        if ($('#content-container').hasClass("collapse")) {
            setTimeout(function () {
                $('#content-container').collapse();
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
        // Retrieve the data
        $.ajax({
            url: `${API_HOST_URL}/api/v2/course-statistics/${campus}//${subject}/${course}`,
            type: "GET",
            success: function (response) {
                updateCourseHeadmatter(response);
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
        // updateGradesChart(data);
    }


});