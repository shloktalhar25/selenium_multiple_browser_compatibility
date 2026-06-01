This is designed to automatically check whether a web application continues to work correctly whenever a browser such as Chrome, Firefox, or Edge receives an update.
Normally browsers update automatically in the background. 

they can sometimes cause unexpected issues in websites or web applications. In many cases, teams only discover these problems after users start reporting them.
To solve this problem, the system automatically detects browser version changes and runs a set of basic validation tests. 
This helps identify compatibility issues early, before they affect end users
The system first checks the installed versions of Chrome, Firefox, and Edge on the machine.
It then compares the current versions with the versions that were previously recorded..
If a browser update is detected, the system automatically triggers validation tests for that browser using Selenium Server mode. Multiple browsers can be tested at the same time.
Once the tests are completed, the results are stored in a report file. If a browser passes all tests, its version information is updated in the local registry. If a browser fails, its version is not updated so that the system can continue checking it in future runs until the issue is resolved.
Test Cases:
Website: OrangeHrm: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login 
(might be slow sometimes)
 
  Opening the login page.
Entering user credentials.
Verifying successful login.
Navigating through application pages.
Interacting with user profile elements.
Logging out and verifying redirection
