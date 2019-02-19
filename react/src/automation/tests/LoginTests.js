import { RequestLogger, RequestMock } from 'testcafe';

import config from "../config";
import CredentialsPage from "../pages/CredentialsPage";
import { getURL } from "../util/ClientFunctions";

const loginPage = new CredentialsPage();

const logger = RequestLogger({
});

const CREDENTIALS_ERROR_MESSAGE = "The entered credentials are invalid.";

const credentialsErrorMock = RequestMock().onRequestTo(/\/login\//).respond({
    message: CREDENTIALS_ERROR_MESSAGE
}, 400, config.corsHeaders);
const serverErrorMock = RequestMock().onRequestTo(/\/login\//).respond(null, 500, config.corsHeaders);

const successMock = RequestMock().onRequestTo(/\/login\//).respond(null, 200, config.corsHeaders);

fixture `Tests the login page`
    .page `${config.siteUrl}/login`;

    test("disabling login button", async (t) => {
        await loginPage.testDisablingSubmit(t);
    });
    
    test.requestHooks(logger, credentialsErrorMock)("logging in with credentials that are incorrect", async (t) => {
        await t.typeText(loginPage.username, "a_taken_username")
            .typeText(loginPage.password, "a")
            .click(loginPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/login/") && record.response.statusCode === 400)).ok();
        
        await t.expect(loginPage.errorAlert.visible).eql(true)
            .expect(loginPage.errorAlert.innerText).eql(CREDENTIALS_ERROR_MESSAGE);
    });

    test.requestHooks(logger, serverErrorMock)("logging in with a server-side error", async (t) => {
        await t.typeText(loginPage.username, "a_taken_username")
            .typeText(loginPage.password, "a")
            .click(loginPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/login/") && record.response.statusCode === 500)).ok();
        
        await t.expect(loginPage.errorAlert.visible).eql(true);
    });

    test.requestHooks(logger, successMock)("successfully logging into an existing account", async (t) => {
        const COOKIE_USERNAME = "user",
            COOKIE_USERID = "abc-defg-hij";
        
        await t.eval((username, userId) => {
            document.cookie = "core-username=" + username;
            document.cookie = "core-userid=" + userId;
        }, COOKIE_USERNAME, COOKIE_USERID);

        await t.typeText(loginPage.username, COOKIE_USERNAME)
            .typeText(loginPage.password, "a")
            .click(loginPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/login/") && record.response.statusCode === 200)).ok({timeout: 8000});
        
        await t.expect(getURL()).notContains("/login", {timeout: 8000});
    });

    test("test visiting the register page with the link", async (t) => {
        await t.click(loginPage.switchAction);
        await t.expect(getURL()).contains("/register", {timeout: 8000});
    });