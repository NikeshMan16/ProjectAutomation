Read me file
This is a practice automation test script for a Test ecommerce site
Test Cases for Login Page

| Test CaseID | TestCase Description                             | Precondition                   | Test Steps                                                                                                   | Expected Result                                                                       | Actual Result |
|-------------|--------------------------------------------------|--------------------------------|--------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------|
| TC_001      | Test Login for valid users                       | User must be on the Login Page | 1.Go to url:"saucedemo.com"<br/>2.Enter the credentials for valid_user<br/>3.Click on submit button          | The user must be directed to the main page.                                           |               |
| TC_002      | Test Login for problem_user                      | User must be on the Login Page | 1.Go to url:"saucedemo.com"<br/>2.Enter the credentials for problem_user<br/>#3.Click on submit button       | The user must directed to the main page.                                              |               |
| TC_003      | Test Login for invalid or locked out users       | User must be on the Login Page | 1.Go to url:"saucedemo.com"<br/>2.Enter the credentials for locked_out_user<br/>3.Click on submit button     | Validation error message must be displayed and user should still be on the login page |               |
| TC_004      | Test Login for empty username and valid password | User must be on the Login Page | 1.Go to url:"saucedemo.com"<br/>2.Enter the valid password <br/>3.Click on submit button                     | Validation error message indicating user field is required should be shown.           |               |
| TC_005      | Test Login for valid username and empty password | User must be on the Login Page | 1.Go to url:"saucedemo.com"<br/>2.Enter the valid username and empty password.<br/>3. Click on submit button | Validation error message incdicating password is required should be shown.            |               |

Test Logins are done for all the users provided by the test automation site within the script but all are not mentioned in the test case.

Test Cases for Functional Requirement of the Ecommerce site including add to cart functionalit,view product functionality, checkout functionality
