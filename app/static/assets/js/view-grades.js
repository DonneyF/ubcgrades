'use strict';

$(function () {

    /**
     * State machine that controls state and history handling as students
     * navigate between different courses. It follows the update order of
     * year, subject, course, section.
     *
     * When the state of the app changes, this handler will try to resolve
     * the new state in that given order until it reaches a mismatch. On
     * mismatch, the old behaviour of opening the dropdown will occur.
     *
     * Browser history state is pushed to the browser on successful selection
     * of a course. Invalid inputs are wiped from the history stack.
     */
    function StateHandler() {
        let _year;
        let _subject;
        let _course;
        let _section;

        let updateOrder = [
            "year",
            "subject",
            "course",
            "section",
        ];

        let constructHash = () => {
            return `${_year}-${_subject}-${_course}-${_section}`;
        };

        this.updateYear = async (year, dropdown = true) => {
            _year = year;
            if (dropdown) {
                let nextId = "subject";
                let response = await updateVGSubjectDrop();
                let data = updateVGDropdown(nextId, response);
                this.resolveState(nextId, response, data);
            }
        };

        this.updateSubject = async (subject, dropdown = true) => {
            _subject = subject;
            if (dropdown) {
                let nextId = "course";
                let response = await updateVGCourseDrop(subject);
                let data = updateVGDropdown(nextId, response);
                this.resolveState(nextId, response, data);
            }
        };

        this.updateCourse = async (course, dropdown = true) => {
            _course = course;
            if (dropdown) {
                let nextId = "section";
                let response = await updateVGSectionDrop(course);
                let data = updateVGDropdown(nextId, response);
                this.resolveState(nextId, response, data);
            }
        };

        this.updateSection = async (section, dropdown = true) => {
            _section = section;
            this.updateState();
            if (dropdown) {
                $('#vg-dropdown-form').submit();
            }
        };

        /**
         * Last stage of the state machine that consolidates all
         * the substates and pushes the state to the browser history stack.
         */
        this.updateState = () => {
            // This shouldn't push a new state to the history stack
            // if the hashes are the same, so we don't need to check
            window.location.hash = constructHash();
            $("#vg-copy-url-input").val(document.location.href);
        };

        /**
         * Resolves the state of the app, determining whether to open
         * the dropdown (if the previous state wasn't found), or to
         * trigger a select on the next dropdown to move to the next state.
         * @param id selector suffix for the dropdown to target
         * @param response response from API
         * @param data parsed data from the dropdown handlers
         */
        this.resolveState = (id, response, data) => {
            let indexOfId = updateOrder.indexOf(id);
            let dropdown = $(`#vg-drop-${id}`);
            let dataArray = [_year, _subject, _course, _section];
            if (data.find((e) => e.id === dataArray[indexOfId])) {
                dropdown.select2("trigger", "select", {
                    data: {
                        id: dataArray[indexOfId],
                    }
                });
            } else {
                if (dataArray[indexOfId]) {
                    displayWarning(`${id.charAt(0).toUpperCase()}${id.slice(1)} ${dataArray[indexOfId]} not found.`);
                }
                if (id === "section" && response.length === 2 && response.includes("OVERALL")) {
                    dropdown.select2("trigger", "select", {
                        data: {id: response.filter(x => x !== "OVERALL")[0]}
                    });
                } else {
                    dropdown.select2("open");
                }
            }
        };

        /**
         * Resets the state machine and updates the browser history.
         */
        this.resetState = () => {
            let data = [(yearsession) ? yearsession.toString() : null, null, null, null];
            [_year, _subject, _course, _section] = data;
            for (let i = 0; i < data.length; i++) {
                $(`#vg-drop-${updateOrder[i]}`).val(data[i]).trigger("change");
            }
            window.history.replaceState(undefined, undefined, " ");
        };

        /**
         * Synchronizes the state machine with the URL fragment.
         */
        this.synchronizeState = () => {
            let fragments = window.location.hash.substring(1).split("-");
            if (fragments.length === 4) {
                [_year, _subject, _course, _section] = fragments;
                $("#vg-drop-year").select2("trigger", "select", {
                    data: {
                        id: _year,
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

        /**
         * Share URL handlers below.
         */
        $("#vg-copy-url-form").on("submit", () => {
            try {
                navigator.clipboard.writeText(document.location.href);
                displayInfo("Copied!");
            } catch (e) {
                displayError("Failed to copy, try manually.");
            }
            return false;
        });

        $("#vg-copy-url-input").on("click", (e) => {
            e.target.setSelectionRange(0, e.target.value.length)
        });
    }

    let stateHandler = new StateHandler();
    // This will get arbitrarily large but it makes the app speedier on nav
    // We'll just hope users don't OOM before refreshing the page ¯\_(ツ)_/¯
    const apiCache = {};


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
            stateHandler.init();
        });
    });

    function populateYearSessionDrop() {
        $('#vg-drop-year').prepend('<option></option>').select2({
            data: campus === "UBCV" ? YEARSESSIONS_UBCV.map(item => ({
                'id': item,
                'text': item
            })) : YEARSESSIONS_UBCO.map(item => ({'id': item, 'text': item})),
        }).on("select2:select", function (e) {
            yearsession = new YearSession($(this).select2('data')[0]['id']);
            apiVersion = yearsession.year < 2014 ? "v1" : "v2";
            stateHandler.updateYear(yearsession.toString());
        });
    }

    $('#vg-drop-subject').select2().on("select2:select", function (e) {
        stateHandler.updateSubject($(this).select2('data')[0]['id']);
    });

    $('#vg-drop-course').select2().on("select2:select", function (e) {
        stateHandler.updateCourse($(this).select2('data')[0]['id']);
    });

    $('#vg-drop-section').select2().on("select2:select", function (e) {
        stateHandler.updateSection($(this).select2('data')[0]['id']);
    });

    if (campus != null) {
        populateYearSessionDrop();
        stateHandler.init();
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param yearsession a 5 character yearsession code.
     * @returns promise that resolves the data
     */
    function updateVGSubjectDrop() {
        return new Promise((resolve, reject) => {
            let url = `${API_HOST_URL}/api/${apiVersion}/subjects/${campus}/${yearsession}`;
            if (url in apiCache) {
                resolve(apiCache[url]);
            } else {
                $.ajax({
                    url: url,
                    type: "GET",
                    cache: true,
                    success: function (response) {
                        apiCache[url] = response;
                        resolve(response);
                    },
                    error: function () {
                        displayError("Unable to connect to API");
                        reject();
                    }
                });
            }
        });
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param subject is the 2 to 4 character subject code
     * @returns promise that resolves the data
     */
    function updateVGCourseDrop(subject) {
        return new Promise((resolve, reject) => {
            let url = `${API_HOST_URL}/api/${apiVersion}/courses/${campus}/${yearsession}/${subject}`;
            if (url in apiCache) {
                resolve(apiCache[url]);
            }
            $.ajax({
                url: url,
                type: "GET",
                cache: true,
                success: function (response) {
                    apiCache[url] = response;
                    resolve(response);
                },
                error: function () {
                    displayError("Unable to connect to API");
                    reject();
                }
            });
        });
    }

    /**
     * Retrieves the subjects and updates the View Grades Subject dropdown
     * @param course is the 3 to 4 character course code
     * @returns promise that resolves the data
     */
    function updateVGSectionDrop(course) {
        let subject = $("#vg-drop-subject").select2('data')[0]['id'];
        return new Promise((resolve, reject) => {
            let url = `${API_HOST_URL}/api/${apiVersion}/sections/${campus}/${yearsession}/${subject}/${course}`;
            if (url in apiCache) {
                resolve(apiCache[url]);
            }
            $.ajax({
                url: url,
                type: "GET",
                cache: true,
                success: function (response) {
                    apiCache[url] = response;
                    resolve(response);
                },
                error: function () {
                    displayError("Unable to connect to API");
                    reject();
                }
            });
        });
    }


    /**
     * Updates the dropdowns with the values
     * @param id is the CSS id of the dropdown
     * @param response is the API response data
     * @returns the parsed data in the dropdown
     */
    function updateVGDropdown(id, response) {
        let dropdown = $(`#vg-drop-${id}`);
        let data;
        // Populate the dropdown with the new data
        if (["subject", "course"].indexOf(id) >= 0) {
            if (id === "course") {
                data = response.map(item => ({
                    'id': `${item['course']}${item['detail']}`,
                    'text': `${item['course']}${item['detail']} - ${item['course_title']}`
                }));
            } else {
                data = response.map(item => ({
                    'id': item[id],
                    'text': `${item[id]} - ${item[`${id}_title`]}`
                }));
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
            data = response.map(item => ({'id': item, 'text': item}));
            dropdown.empty().prepend('<option></option>').select2({
                data: data,
            });
        }

        return data;
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
            stateHandler.updateYear(idSplit[0], false);
            stateHandler.updateSubject(idSplit[1], false);
            stateHandler.updateCourse(idSplit[2], false);
            stateHandler.updateSection(idSplit[3], false);
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
        $("#teaching-team-v1").text(data['educators'].replace(/;/gi, ", "));

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
        $("#teaching-team-v2").text(data['educators'].replace(/;/gi, ", "));

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
                labels: apiVersion === "v1" ? GRADES_V1.slice(0) : GRADES_V2.slice(0), // slicing creates a level copy
                datasets: [{
                    data: gradeData
                }]
            }
        });
        // Save to jQuery object

        $chart.data('chart', sectionGradesChart);
    }

});