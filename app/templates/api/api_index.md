The API served here requires no API key. All data will be served via JSON. The base url is `https://ubcgrades.com/api`

There are multiple versions of the API to conform to different data sources.

# Version 1 (v1)

Version 1 of the API supports only retrieval of grade distributions and filtering through them. The data source is from the PAIR Reports website, which is no longer available. As a result, some of the data 2014S and later can be in accurate. There will be no more updates to the data served by this endpoint. **This API only supports the UBCV campus**.

# Version 2 (v2)

Version 2 of the API supports retrieval of grade distributions, filtering through them, and course statistics as well. The data source for v2 is from the Tableau Dashboard for retrieval of individual grade distributions. Data for the course statistics uses data from v1 for grade distributions earlier than 2014S. This API supports the UBCV and UBCO campus.

# Version 3 (v3)

Version 3 is v2 with additional data dependencies on the second version Tableau Dashboard. It carries data from 2019W onward. Data for course statistics uses data from both v1 and v2 for grade distributions earlier than 2021W. This API supports the UBCV and UBCO campus. Some endpoints are not available in v3, and v2 should be used instead.

# Definitions

| Key         | Description                                                  | Examples             |
| ----------- | ------------------------------------------------------------ | -------------------- |
| campus      | A four character string for the campus. This key must take one of two values: "UBCV" or "UBCO" | UBCV, UBCO           |
| yearsession | A 5-character string whose first 4 characters is a year and last character is either `W` for winter or `S` for summer. | 2018W, 2012S         |
| subject     | A 2-4 character string that represents a subject code.       | BA, KIN, APSC        |
| course      | A 3-4 character string whose first three characters is a three-digit number. The optional fourth character is a detail modifier. | 001, 200, 230A, 342C |
| section     | A 3-character string that represents a section in a course. This can be a lecture, tutorial, lab, etc. | 001, 100, GIS, T1A   |

# Download Data

Visit [https://github.com/DonneyF/ubc-pair-grade-data](https://github.com/DonneyF/ubc-pair-grade-data) for the raw data.