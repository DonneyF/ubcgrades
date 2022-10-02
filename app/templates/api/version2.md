# Retrieve Grade Distributions

Required URL parameters are **bolded**.

| Endpoint                                                     | Description                                                | Example                                                                          |
| ------------------------------------------------------------ | ---------------------------------------------------------- |----------------------------------------------------------------------------------|
| /grades/**campus**/**yearsession**/**subject**/**course**/**section** | Retrieves a grade distribution report for a single section | [api/v2/grades/UBCV/2018W/MATH/100/101](/api/v2/grades/UBCV/2018W/MATH/100/101)  |
| /grades/**campus**/**yearsession**/**subject**/**course**    | Retrieves a grade distribution report for a course         | [/api/v2/grades/UBCV/2018W/MATH/100](/api/v2/grades/UBCV/2018W/MATH/100)         |
| /grades/**campus**/**yearsession**/**subject**               | Retrieves a grade distribution report for a subject        | [/api/v2/grades/UBCV/2018W/POLI](/api/v2/grades/UBCV/2018W/POLI)                 |
| /grades/**campus**/**yearsession**                           | Retrieves a grade distribution report for a yearsession    | [/api/v2/grades/UBCV/2017S](/api/v2/grades/UBCV/2017S)                           |
| /grades/**campus**/**yearsession**/**subject**/**course**/**section** | Retrieves a grade distribution report for a single section | [/api/v2/grades/UBCV/2018W/MATH/100/101](/api/v2/grades/UBCV/2018W/MATH/100/101) |

# Filters

Required URL parameters are **bolded**.

| Endpoint                                                    | Description                                                  | Example                                                      |
| ----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| /sections/**campus**/**yearsession**/**subject**/**course** | Retrieves all the section numbers under a particular course  | [/api/v2/sections/UBCV/2018W/BIOL/200](/api/v2/sections/UBCV/2018W/BIOL/200) |
| /courses/**campus**/**yearsession**/**subject**             | Retrieves all the course labels under a particular subject and yearsession | [/api/v2/courses/UBCV/2018W/POLI](/api/v2/courses/UBCV/2018W/POLI) |
| /courses/**campus**/**subject**                             | Retrieves all the distinct course labels under a particular subject | [/api/v2/courses/UBCV/ELEC](/api/v2/courses/UBCV/ELEC)       |
| /subjects/**campus**/**yearsession**                        | Retrieves all distinct subjects under a particular yearsession | [/api/v2/subjects/UBCV/2016W](/api/v2/subjects/UBCV/2016W)   |
| /subjects/**campus**                                        | Retrieves all distinct subjects across all yearsessions      | [/api/v2/subjects/UBCV](/api/v2/subjects/UBCV)               |
| /yearsessions/**campus**                                    | Retrieves all available yearsessions                         | [/api/v2/yearsessions/UBCV/](/api/v2/yearsessions/UBCV)      |

## Course Profile Data
| Endpoints                                                    | Description                                                  | Examples                                                                                                                                                                                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /course-statistics/**campus**/**subject** <br> /course-statistics/**campus**/**subject**/**course** | Retrieves general data regarding course averages, pass percentage, etc. | [/api/v2/course-statistics/UBCV/ENGL](/api/v2/course-statistics/UBCV/ENGL) <br> [/api/v2/course-statistics/UBCV/ENGL/112](/api/v2/course-statistics/UBCV/ENGL/112)                                                         |
| /course-statistics/distributions/**campus**/**subject** <br> /course-statistics/distributions/**campus**/**subject**/**course** | Retrieves historical course distributions                    | [/api/v2/course-statistics/distributions/UBCV/SCIE](/api/v2/course-statistics/distributions/UBCV/SCIE) <br> [/api/v2/course-statistics/distributions/UBCV/SCIE/001](/api/v2/course-statistics/distributions/UBCV/SCIE/001) |
| /course-statistics/teaching-team/**campus**/**subject** <br> /course-statistics/teaching-team/**campus**/**subject**/**course** | Retrieves who and when educators taught a course by yearsession (1) | [/api/v2/course-statistics/teaching-team/UBCV/LING](/api/v2/course-statistics/teaching-team/UBCV/LING) <br> [/api/v2/course-statistics/teaching-team/UBCV/LING/100](/api/v2/course-statistics/teaching-team/UBCV/LING/100) |

(1) An *educator* is any person that was involved in delivery of the course. This includes lecturers, teaching assistants, and professors.