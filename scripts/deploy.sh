export DJANGO_SITE_URL="https://cmput404-i5.herokuapp.com"
cd react
npm install
npm run-script build
mv -vf dist/* ../static
