# cmput404-project

[![Build Status](https://travis-ci.com/i-5ive/cmput404-project.svg?branch=master)](https://travis-ci.com/i-5ive/cmput404-project)

CMPUT404 Wi19 Team Project

We are making a distributed social network! Check out our video [here](https://youtu.be/9pP6n_PdUaw)! Test out our website with this [User Manual](https://github.com/i-5ive/cmput404-project/wiki/User-Manual).

# Setup

## React

#### Development
1. Ensure you have [Node v8 (Carbon)](https://nodejs.org/en/) installed. Note that this is not the highest version of the LTS right now (v10).

2. Run `npm install`

3. Run `npm start` to start running a local server hosting the react changes

#### Testing

You can run `npm test` to start the test runner. This will run Karma, the test runner, and show you the passing and failing front-end tests. This also runs a code-coverage check at the end of it, which shows you how much of the code is "covered". Karma hot-reloads when you make a file change, so you do not need to reboot or re-run karma with every change.

`npm run-script lint` will scan for styling errors and keep the codebase consistent. The build will fail if this fails.

#### Deployment

Running `npm run-script build` will generate `dist/index.html` you can open the path to this file in your browser to see the results of what was built.

## Django

Django 2.1.6  

### Installation

#### Windows
- Install [Python 3.5+](https://www.python.org/downloads/)
- [Add \python and \python\scripts to your system variables](https://www.java.com/en/download/help/path.xml)
- You can verify they are installed and attached to the path by typing `Python -v` and `pip -V`
- Run `pip install -r requirements.txt` to install all dependencies.
- export DJANGO_SITE_URL="https://weeb-tears.herokuapp.com"
- run `python manage.py runserver` to start the server locally.

#### Mac
 - Get [Homebrew](https://brew.sh/), if you haven't.
 - Install Python3 `brew install python3`
 - Create a virtual env by typing `virtualenv venv --python=python3`
   - This will help keep your packages for this project separate from other packages
 - You can activate the venv by typing `source venv/bin/activate`
 - Now type `pip install -r requirements.txt`
   - This will install Django, psycopyg2, etc, needed to run the project backend.
 - export DJANGO_SITE_URL="https://weeb-tears.herokuapp.com"
 - You should now be able to run `python3 src/django/manage.py runserver` to start the backend.

### Testing

You can run `python3 manage.py test` to run the django unit tests (if you have installed postgres locally (see below)). Otherwise run `pytest` to use a web-based database for the tests (slow).

##### Running local tests faster (mac instructions)

Run these commands:
```bash
brew install postgres
postgres -D /usr/local/var/postgres
createdb social_dist
psql social_dist
CREATE USER postgres SUPERUSER;
```

Now you can install [pgAdmin4](https://www.pgadmin.org/download/pgadmin-4-macos/), add a new server, choose a name, and the host will be `127.0.0.1`.

Now when you run `python manage.py test` it should run significiantly faster by using the local database you created.

# AJAX Usages
We use AJAX whenever we need to fetch (or send) data from/to our Django server. Here is a list of all the places in our front-end React code where we use AJAX:  

[Registering for a new account](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/auth/AuthStore.js#L98)  
[Logging into an existing account](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/auth/AuthStore.js#L125)  
[Creating a post](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L61)  
[Loading all public posts on the server](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L85)  
[Loading posts from only external servers](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L116)  
[Deleting a post](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L143)  
[Editing a post](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L174)  
[Viewing details about a specific post](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L197)  
[Adding a comment to a post](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L222)  
[Loading comments on a post](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/discover/PostsStore.js#L273)  
[Loading posts on the home feed](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/home/HomeStore.js#L37)  
[Deleting a post on the home feed](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/home/HomeStore.js#L64)  
[Loading pending friend requests](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/friends/FriendsStore.js#L35)  
[Sending a friend request](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/friends/FriendsStore.js#L56)  
[Responding to a friend request](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/friends/FriendsStore.js#L89)  
[Loading details about an author](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L54)  
[Loading an author's posts](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L88)  
[Updating an author profile](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L122)  
[Loading follow details about a specific author](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L233)  
[Unfollowing an author](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L256)  
[Sending a friend request](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L295)  
[Loading github repositories](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L330)  
[Deleting a post from the profile page](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L352)  
[Loading all users an author is following](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L381)  
[Loading all users an author is followed by](https://github.com/i-5ive/cmput404-project/blob/master/react/src/js/react/profile/ProfileStore.js#L401)  

# Resources Used

## Bootstrapping Resources and References
The boilerplate code for setting up React and Django was written by Bennett Hreherchuk for CMPUT401 and is reused here to form the foundation of this project. The code is the Intellectual Property of Bennett Hreherchuk and their team "The Indoors Club" under a non-competing agreement with the University of Alberta Outdoor's Club for six months after December 2018.
Files Included:
 - Most if not all of the configuration files (`.babelrc`, `.eslintrc.json`, `package.json`, etc)
 - index.html, index.js, and App.jsx

## External References

Python unit testing  
https://docs.python.org/3/library/unittest.mock.html  
License: [Python Software Foundation License](https://docs.python.org/3/license.html#psf-license-agreement-for-python-release)  

TestCafe Documentation  
https://devexpress.github.io/testcafe/documentation/test-api/selecting-page-elements/selectors/  
https://devexpress.github.io/testcafe/documentation/test-api/intercepting-http-requests/  
https://devexpress.github.io/testcafe/documentation/test-api/intercepting-http-requests/mocking-http-requests.html  

Setting cookies in JavaScript  
https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie  
License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)  

Restricting file size in Django  
http://www.learningaboutelectronics.com/Articles/How-to-restrict-the-size-of-file-uploads-with-Python-in-Django.php  

Limiting Django querysets  
https://docs.djangoproject.com/en/dev/topics/db/queries/#limiting-querysets  

How to expect url is redirect in TestCafe?  
  [Question](https://www.stackoverflow.com/questions/44878813/how-to-expect-url-is-redirect-in-testcafe)  
  [Answer by Alexander Moskovkin](https://stackoverflow.com/a/44880118)  
  [Alexander Moskovkin](https://www.stackoverflow.com/users/7162281/alexander-moskovkin), [Knovour](https://www.stackoverflow.com/users/711221/knovour), [Alexander Moskovkin](https://www.stackoverflow.com/users/7162281/alexander-moskovkin)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

How to display Base64 images in HTML?  
  [Question](https://www.stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html)  
  [Answer by VinayC](https://stackoverflow.com/a/8499716)  
  [VinayC](https://www.stackoverflow.com/users/417057/vinayc), [Sampath](https://www.stackoverflow.com/users/1077309/sampath), [Christopher](https://www.stackoverflow.com/users/619734/christopher), [dda](https://www.stackoverflow.com/users/1136195/dda)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

Delete cookie by name?  
  [Question](https://www.stackoverflow.com/questions/10593013/delete-cookie-by-name)  
  [Answer by emii](https://stackoverflow.com/a/23995984)  
  [emii](https://www.stackoverflow.com/users/3190005/emii), [Charlie](https://www.stackoverflow.com/users/603986/charlie), [paxdiablo](https://www.stackoverflow.com/users/14860/paxdiablo)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

CSRF with Django, React+Redux using Axios  
  [Question](https://www.stackoverflow.com/questions/39254562/csrf-with-django-reactredux-using-axios)  
  [Answer by krescruz](https://stackoverflow.com/a/48118202)  
  [krescruz](https://www.stackoverflow.com/users/3047021/krescruz), [Reed Dunkle](https://www.stackoverflow.com/users/6172657/reed-dunkle), [yestema](https://www.stackoverflow.com/users/2455457/yestema)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

Django - Overriding the Model.create() method?  
  [Question](https://www.stackoverflow.com/questions/2307943/django-overriding-the-model-create-method)  
  [Answer by Michael Bylstra](https://stackoverflow.com/a/12615339)  
  [Michael Bylstra](https://www.stackoverflow.com/users/343043/michael-bylstra), [nnov](https://www.stackoverflow.com/users/3453776/nnov), [ground5hark](https://www.stackoverflow.com/users/175098/ground5hark), [zaidfazil](https://www.stackoverflow.com/users/7256228/zaidfazil)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

multiple files upload using same input name in django  
  [Question](https://www.stackoverflow.com/questions/851336/multiple-files-upload-using-same-input-name-in-django)  
  [Answer by Justin Voss](https://stackoverflow.com/a/856126)  
  [Justin Voss](https://www.stackoverflow.com/users/5616/justin-voss), [SmileyChris](https://www.stackoverflow.com/users/143280/smileychris), [Abu Aqil](https://www.stackoverflow.com/users/105169/abu-aqil), [Paolo Bergantino](https://www.stackoverflow.com/users/16417/paolo-bergantino)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

Django: have admin take image file but store it as a base64 string  
  [Question](https://www.stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string)  
  [Answer by Ykh](https://stackoverflow.com/a/44492948)  
  [Ykh](https://www.stackoverflow.com/users/6786283/ykh), [mburke05](https://www.stackoverflow.com/users/1492284/mburke05), [Ykh](https://www.stackoverflow.com/users/6786283/ykh)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

How to convert a .png image to string and send it through Django API?  
  [Question](https://www.stackoverflow.com/questions/52444818/how-to-convert-a-png-image-to-string-and-send-it-through-django-api)  
  [Answer by Willem Van Onsem](https://stackoverflow.com/a/52444999)  
  [Willem Van Onsem](https://www.stackoverflow.com/users/67579/willem-van-onsem), [Dipesh Sinha](https://www.stackoverflow.com/users/9548616/dipesh-sinha), [Santosh Kumar](https://www.stackoverflow.com/users/939986/santosh-kumar)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

Django Rest Framework not responding to read_only on nested data  
  [Question](https://www.stackoverflow.com/questions/41248271/django-rest-framework-not-responding-to-read-only-on-nested-data)  
  [Answer by Ivan Semochkin](https://stackoverflow.com/a/41261614)  
  [Ivan Semochkin](https://www.stackoverflow.com/users/5231877/ivan-semochkin), [shanemgrey](https://www.stackoverflow.com/users/873749/shanemgrey), [Community](https://www.stackoverflow.com/users/-1/community)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

how to unit test file upload in django  
  [Question](https://www.stackoverflow.com/questions/11170425/how-to-unit-test-file-upload-in-django)  
  [Answer by Danilo Cabello](https://stackoverflow.com/a/27345260)  
  [Danilo Cabello](https://www.stackoverflow.com/users/157931/danilo-cabello), [Community](https://www.stackoverflow.com/users/-1/community), [damon](https://www.stackoverflow.com/users/1291096/damon), [ƘɌỈSƬƠƑ](https://www.stackoverflow.com/users/3165737/%c6%98%c9%8c%e1%bb%88s%c6%ac%c6%a0%c6%91)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

How to register users in Django REST framework?  
  [Question](https://www.stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework)  
  [Answer by cpury](https://stackoverflow.com/a/29867704)  
  [cpury](https://www.stackoverflow.com/users/1257278/cpury), [chaim](https://www.stackoverflow.com/users/788180/chaim), [Pang](https://www.stackoverflow.com/users/1402846/pang)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

Django-rest-framework permissions for create in viewset  
  [Question](https://www.stackoverflow.com/questions/22760191/django-rest-framework-permissions-for-create-in-viewset)  
  [Answer by argaen](https://stackoverflow.com/a/22767325)  
  [argaen](https://www.stackoverflow.com/users/3481357/argaen), [adi](https://www.stackoverflow.com/users/1223265/adi), [argaen](https://www.stackoverflow.com/users/3481357/argaen)  
  License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)    

[Github Events API](https://developer.github.com/v3/activity/events/types/)  

azu's github event parser for JavaScript (we converted his JavaScript/TypeScript code into Python, so credit for the Github events parser we're using goes to him)  
https://github.com/azu/parse-github-event/blob/master/src/parse-github-event.ts  
[MIT License](https://github.com/azu/parse-github-event/blob/master/LICENSE)  
[Github Profile](https://github.com/azu)  

Create an instance from serializer without persisting it to db  
[Question](https://www.stackoverflow.com/questions/35004398/create-an-instance-from-serializer-without-persisting-it-to-db)  
[Answer by Soufiaane](https://stackoverflow.com/a/35026359)  
[Soufiaane](https://www.stackoverflow.com/users/1882311/soufiaane), [Tomas Walch](https://www.stackoverflow.com/users/5798503/tomas-walch), [wim](https://www.stackoverflow.com/users/674039/wim), [knite](https://www.stackoverflow.com/users/649167/knite)  
License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)  

How to do CamelCase split in python  
[Question](https://www.stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python)  
[Answer by Jossef Harush](https://stackoverflow.com/a/37697078)  
[Jossef Harush](https://www.stackoverflow.com/users/3191896/jossef-harush), [nfs](https://www.stackoverflow.com/users/1654255/nfs)  
License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)  

Montserrat Font from Google Fonts  
https://fonts.google.com/specimen/Montserrat  
License: [SIL Open Font License](https://github.com/JulietaUla/Montserrat/blob/master/OFL.txt)  

Detecting when user scrolls to bottom of div with React js  
[Question](https://www.stackoverflow.com/questions/45585542/detecting-when-user-scrolls-to-bottom-of-div-with-react-js)  
[Answer by Brendan McGill](https://stackoverflow.com/a/49573628)  
[Brendan McGill](https://www.stackoverflow.com/users/4458849/brendan-mcgill), user5797064, [Pardeep Dhingra](https://www.stackoverflow.com/users/1031061/pardeep-dhingra)  
License: [Creative Commons Attribute-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)  
