# Retrieve Grade Distributions

Required URL parameters are **bolded**.

| Endpoint                                                     | Description                                                | Example                                                      |
| ------------------------------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------ |
| /grades/**campus**/**yearsession**/**subject**/**course**/**section** | Retrieves a grade distribution report for a single section | [/v1/grades/UBCV/2018W/MATH/100/101](/api/v1/grades/UBCV/2018W/MATH/100/101) |
| /grades/**campus**/**yearsession**/**subject**/**course**    | Retrieves a grade distribution report for a course         | [/api/v1/grades/UBCV/2018W/MATH/100](/api/v1/grades/UBCV/2018W/MATH/100) |
| /grades/**campus**/**yearsession**/**subject**               | Retrieves a grade distribution report for a subject        | [/api/v1/grades/UBCV/2018W/POLI](/api/v1/grades/UBCV/2018W/POLI) |
| /grades/**campus**/**yearsession**                           | Retrieves a grade distribution report for a yearsession    | [/api/v1/grades/UBCV/2017S](/api/v1/grades/UBCV/2017S)       |

# Filters

Required URL parameters are **bolded**.

| Endpoint                                                    | Description                                                  | Example                                                      |
| ----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| /sections/**campus**/**yearsession**/**subject**/**course** | Retrieves all the section numbers under a particular course  | [/api/v1/sections/UBCV/2018W/BIOL/200](/api/v1/sections/UBCV/2018W/BIOL/200) |
| /courses/**campus**/**yearsession**/**subject**             | Retrieves all the course labels under a particular subject and yearsession | [/api/v1/courses/UBCV/2018W/POLI](/api/v1/courses/UBCV/2018W/POLI) |
| /courses/**campus**/**subject**                             | Retrieves all the distinct course labels under a particular subject | [/api/v1/courses/UBCV/ELEC](/api/v1/courses/UBCV/ELEC)       |
| /subjects/**campus**/**yearsession**                        | Retrieves all distinct subjects under a particular yearsession | [/api/v1/subjects/UBCV/2016W](/api/v1/subjects/UBCV/2016W)   |
| /subjects/**campus**                                        | Retrieves all distinct subjects across all yearsessions      | [/api/v1/subjects/UBCV](/api/v1/subjects/UBCV)               |
| /yearsessions/**campus**                                    | Retrieves all available yearsessions                         | [/api/v1/yearsessions/UBCV/](/api/v1/yearsessions/UBCV)      |