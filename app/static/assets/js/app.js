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
        getSectionGrades('#vg-btn-submit', $('#vg-drop-year').val(), $('#vg-drop-subject').val(), $('#vg-drop-course').val(), $('#vg-drop-section').val());
        return false; // Don't refresh the page.
    });

    /*-----------------------------------
    * API submission
    *-----------------------------------*/
    function getSectionGrades(button, yearsession, subject, course, section) {
        let $button = $(button);
        let loadingText = 'Loading...';
        if ($button.html() !== loadingText) {
            // Store original text
            $button.data('original-text', $button.html());
            // Set disabled state for button
            $button.addClass('disabled');
            // Set loading text
            $button.html(loadingText);
        }
        // Send API request
        $.ajax({
            url: `${API_HOST_URL}/api/v2/grades/UBCV/${yearsession}/${subject}/${course}/${section}`,
            type: "GET",
            // Function to run on success
            success: function (response) {
                updateGradeData(response);
                $button.html($button.data('original-text'));
                $button.removeClass('disabled');
            },
            // Function to run on error
            error: function (response) {
                // TODO
            }
        });
    }

    /*-----------------------------------
    * Data Callbacks
    *-----------------------------------*/

    function updateGradeData(data) {
        // Update the headmatter
        data = Object.assign({}, data, data['stats']);
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
    }

});

//
// Select2.js
//

// 'use strict';
//
// var Select2 = (function () {
//
//     //
//     // Variables
//     //
//
//     var $select = $('[data-toggle="select"]');
//
//
//     //
//     // Methods
//     //
//
//     function init($this) {
//         var options = {
//             // dropdownParent: $this.closest('.modal').length ? $this.closest('.modal') : $(document.body),
//             // minimumResultsForSearch: $this.data('minimum-results-for-search'),
//             // templateResult: formatAvatar
//             //placeholder: $this.data()['placeholder'],
//             //allowClear: true
//         };
//         $this.select2(options);
//     }
//
//
//     //
//     // Events
//     //
//
//     if ($select.length) {
//
//         // Init selects
//         $select.each(function () {
//             init($(this));
//         });
//     }
//
// })();