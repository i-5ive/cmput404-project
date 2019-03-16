# cmput404-project
CMPUT404 Wi19 Team Project

We are making a distributed social network!

## Resources
The boilerplate code for setting up React and Django was written by Bennett Hreherchuk for CMPUT401 and is reused here to form the foundation of this project. The code is the Intellectual Property of Bennett Hreherchuk and their team "The Indoors Club" under a non-competing agreement with the University of Alberta Outdoor's Club for six months after December 2018. 
Files Included:
 - Most if not all of the configuration files (`.babelrc`, `.eslintrc.json`, `package.json`, etc)
 - index.html, index.js, and App.jsx

## External References
TODO: stackoverflow references in code should be placed here

Python unit testing  
https://docs.python.org/3/library/unittest.mock.html  

TestCafe Documentation  
https://devexpress.github.io/testcafe/documentation/test-api/selecting-page-elements/selectors/  
https://devexpress.github.io/testcafe/documentation/test-api/intercepting-http-requests/  
https://devexpress.github.io/testcafe/documentation/test-api/intercepting-http-requests/mocking-http-requests.html  

# Running local tests faster (mac instructions)
`brew install postgres`
`postgres -D /usr/local/var/postgres`
`createdb social_dist`
`psql social_dist`
`CREATE USER postgres SUPERUSER;`
Install [pgAdmin4](https://www.pgadmin.org/download/pgadmin-4-macos/)
 * add a new server, choose a name and the host will be `127.0.0.1`