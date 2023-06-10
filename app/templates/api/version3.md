# Retrieve Grade Distributions

Required URL parameters are **bolded**.

| Endpoint                                                     | Description                                                | Example                                                                          |
| ------------------------------------------------------------ | ---------------------------------------------------------- |----------------------------------------------------------------------------------|
| /grades/**campus**/**yearsession**/**subject**/**course**/**section** | Retrieves a grade distribution report for a single section | [/api/v3/grades/UBCV/2022S/MATH/100/92A](/api/v3/grades/UBCV/2022S/MATH/100/92A) |
| /grades/**campus**/**yearsession**/**subject**/**course**    | Retrieves a grade distribution report for a course         | [/api/v3/grades/UBCV/2022S/MATH/100](/api/v3/grades/UBCV/2022S/MATH/100)         |
| /grades/**campus**/**yearsession**/**subject**               | Retrieves a grade distribution report for a subject        | [/api/v3/grades/UBCV/2022S/POLI](/api/v3/grades/UBCV/2022S/POLI)                 |
| /grades/**campus**/**yearsession**                           | Retrieves a grade distribution report for a yearsession    | [/api/v3/grades/UBCV/2022S](/api/v3/grades/UBCV/2022S)                           |

# Filters

Required URL parameters are **bolded**.

| Endpoint                                                    | Description                                                  | Example                                                                      |
| ----------------------------------------------------------- | ------------------------------------------------------------ |------------------------------------------------------------------------------|
| /sections/**campus**/**yearsession**/**subject**/**course** | Retrieves all the section numbers under a particular course  | [/api/v3/sections/UBCV/2022W/BIOL/200](/api/v3/sections/UBCV/2022W/BIOL/200) |
| /courses/**campus**/**yearsession**/**subject**             | Retrieves all the course labels under a particular subject and yearsession | [/api/v3/courses/UBCV/2022S/POLI](/api/v3/courses/UBCV/2022S/POLI)           |
| /courses/**campus**/**subject**                             | Retrieves all the distinct course labels under a particular subject | [/api/v3/courses/UBCV/ELEC](/api/v3/courses/UBCV/ELEC)                       |
| /subjects/**campus**/**yearsession**                        | Retrieves all distinct subjects under a particular yearsession | [/api/v3/subjects/UBCV/2022S](/api/v3/subjects/UBCV/2022S)                   |
| /subjects/**campus**                                        | Retrieves all distinct subjects across all yearsessions      | [/api/v3/subjects/UBCV](/api/v3/subjects/UBCV)                               |
| /yearsessions/**campus**                                    | Retrieves all available yearsessions                         | [/api/v3/yearsessions/UBCV/](/api/v3/yearsessions/UBCV)                      |

## Course Profile Data

| Endpoints                                                    | Description                                                  | Examples                                                                                                                                                                                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /course-statistics/**campus**/**subject** <br> /course-statistics/**campus**/**subject**/**course** | Retrieves general data regarding course averages, pass percentage, etc. | [/api/v3/course-statistics/UBCV/ENGL](/api/v3/course-statistics/UBCV/ENGL) <br> [/api/v3/course-statistics/UBCV/ENGL/112](/api/v3/course-statistics/UBCV/ENGL/112)                                                         |
| /course-statistics/distributions/**campus**/**subject** <br> /course-statistics/distributions/**campus**/**subject**/**course** | Retrieves historical course distributions                    | [/api/v3/course-statistics/distributions/UBCV/SCIE](/api/v3/course-statistics/distributions/UBCV/SCIE) <br> [/api/v3/course-statistics/distributions/UBCV/SCIE/001](/api/v3/course-statistics/distributions/UBCV/SCIE/001) |
| /course-statistics/teaching-team/**campus**/**subject** <br> /course-statistics/teaching-team/**campus**/**subject**/**course** | Retrieves who and when educators taught a course by yearsession (1) | [/api/v3/course-statistics/teaching-team/UBCV/LING](/api/v3/course-statistics/teaching-team/UBCV/LING) <br> [/api/v3/course-statistics/teaching-team/UBCV/LING/100](/api/v3/course-statistics/teaching-team/UBCV/LING/100) |

(1) An *educator* are staff members that are involved in delivery of the course. For yearsessions 2022S and above, they do not include teaching assistants.