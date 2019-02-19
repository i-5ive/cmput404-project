import config from "../config";
import {isLoggedIn} from "../util/ClientFunctions";

const COOKIE_USERNAME = "user",
    COOKIE_USERID = "abc-defg-hij";

fixture `Tests the user initially loading the site`
    .page `${config.siteUrl}/`;

    test("loading the site with user login cookies set", async (t) => {
        await t.eval((username, userId) => {
            document.cookie = "core-username=" + username;
            document.cookie = "core-userid=" + userId;
        }, COOKIE_USERNAME, COOKIE_USERID);

        await t.eval(() => {
            window.location.reload();
        });

        const loggedIn = await isLoggedIn(t);
        await t.expect(loggedIn).eql(true);
    });

    test("loading the site without user login cookies set", async (t) => {
        const loggedIn = await isLoggedIn(t);
        await t.expect(loggedIn).eql(false);
    });