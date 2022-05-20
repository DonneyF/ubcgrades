# About & Help

UBCGrades.com is a simple website for you to view and visualize historic grade distribution of courses at the University of British Columbia Vancouver and Okanagan. UBCGrades.com is no way affiliated with the University of British Columbia.

The purpose of this website is to simply display grade reports in a more useable manner than what is officially provided by UBC as well as to report older grade data that has been removed from public access. 

## Data Source

The source of data for this website is from [ubc-pair-grade-data](https://github.com/DonneyF/ubc-pair-grade-data). 

> There are two main sources for the data. The first (now deprecated) source was from the old PAIR Reports dashboard located [here](https://webprd01.pair.ubc.ca/reports/welcome.action). This tool was removed in the summer of 2019 in favor of a Tableau dashboard found [here](http://pair.ubc.ca/student-performance/grades-distribution/) (the UBC VPN is needed to access), serving as the second source.

**Q: How are statistics computed?**

A: See the scripts in the source code.

**Q: How updated is this website**:

A: Grade data changes all the time, due to various reasons like deferred exams, appeals, etc. This website is as up to date as the latest commits of the grade data repo mentioned above.

## View Grades

This page allows you to retrieve single-section grade reports.

**Q: Why are some grade entries missing?**

A: For section grades 2014S and later, the page loads data from the Tableau dashboard. For some years, the dashboard does not report grades for grade categories with entries of 6 or less for privacy reasons.

**Q: So then why do I see some grade entries with 6 or less?**:

A: Where possible, it is possible to extrapolate the value of the missing grade entry (for example, if every grade category was populated and only one was missing, we simply subtract the sum from the number of enrolled students).

## Statistics by Course

This page allows you to retrieve basic course statistics.

**Q: Why is there no pass-percentage?**

A: It is not possible to compute the pass percentage from sections from the Tableau dashboard as it does not report the number of students who failed for all sections.

**Q: What is "Teaching Team"?**:

A: This is the names of all personnel credited with the delivery of the course. You will see TA and other facilitators if the Tableau Dashboard has reported them. For courses delivered earlier than 2014S, only the professor(s) were reported.

## Other

**Q: Why did you make this website?**

A: Back in 2018W when the Pair Reports website was still up, I was interested in questions like "what is the average grade of a first-year student?" or "Does MATH grade harshly more than other subjects?". While you can't directly answer these questions from this website, the data is there for you to get some idea of the answer to these questions. Retrieving all the data from the Pair Reports website was also a fun challenge.

**Q: How can I use the data already computed in my application?**

A: You can use the API for this website, which does not require a key.