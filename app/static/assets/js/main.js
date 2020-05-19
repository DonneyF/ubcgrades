/*-----------------------------------
    * Global Variables
    *-----------------------------------*/

let yearsession;
let apiVersion;
let campus = localStorage.getItem("campus");

const YEARSESSIONS_UBCV = ['2019S', '2018W', '2018S', '2017W', '2017S', '2016W', '2016S', '2015W', '2015S', '2014W', '2014S', '2013W', '2013S', '2012W', '2012S', '2011W', '2011S', '2010W', '2010S', '2009W', '2009S', '2008W', '2008S', '2007W', '2007S', '2006W', '2006S', '2005W', '2005S', '2004W', '2004S', '2003W', '2003S', '2002W', '2002S', '2001W', '2001S', '2000W', '2000S', '1999W', '1999S', '1998W', '1998S', '1997W', '1997S', '1996W', '1996S'];
const YEARSESSIONS_UBCO = YEARSESSIONS_UBCV.slice(0, 11);
const HEADMATTER_V1_KEYS = ["average", "stdev", "high", "low", "pass", "fail", "enrolled", "withdrew", "audit", "other"];
const HEADMATTER_V2_KEYS = ["average", "stdev", "high", "low", "enrolled"];
const GRADES_V1 = ["0-9%", "10-19%", "20-29%", "30-39%", "40-49%", "<50%", "50-54%", "55-59%", "60-63%", "64-67%", "68-71%", "72-75%", "76-79%", "80-84%", "85-89%", "90-100%"];
const GRADES_V2 = GRADES_V1.slice(5);
const API_HOST_URL = "http://localhost:5000";

class YearSession {
    constructor(yearsession) {
        this.year = parseInt(yearsession.substring(0, 4));
        this.session = yearsession.substring(4);
    }

    toString() {
        return this.year + this.session;
    }
}


/*-----------------------------------
* Campus Selector and Dropdowns
*-----------------------------------*/
// Populate local storage with the desired campus if not already existing
if (localStorage.getItem("campus") == null) $('#exampleModal').modal('show');


/*-----------------------------------
* Display Errors
*-----------------------------------*/
// Use a counter to generate and collapse multiple alerts
let errorCounter = 0;

function displayError(message) {
    // Show error
    let errorId = `error-${errorCounter}`;
    $("#notification").append(`<div class="alert alert-danger mt-3" id="${errorId}"><strong>Error.</strong> ${message}</div>`);
    // Fade the error after a second
    $(`#${errorId}`).fadeTo(1500, 500).slideUp(500, function () {
        $(`#${errorId}`).slideUp(1000);
        // Delete the HTML element after its hidden.
        $(`#${errorId}`).remove();
    });
    errorCounter++;
}