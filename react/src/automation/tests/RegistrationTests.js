import { RequestLogger, RequestMock } from 'testcafe';

import config from "../config";
import RegistrationPage from "../pages/RegistrationPage";
import RestUtil from "../../js/react/util/RestUtil";
import { getURL } from "../util/ClientFunctions";

const registerPage = new RegistrationPage();

const logger = RequestLogger({
    logResponseHeaders: true,
    logResponseBody: true,
	logRequestBody: true
});

const USERNAME_ERROR_MESSAGE = "This username has a problem";
const PASSWORD_ERROR_MESSAGE = "This password has a problem";

const serverUsernameErrorMock = RequestMock().onRequestTo(/\/users\//).respond({
    username: [USERNAME_ERROR_MESSAGE]
}, 400, config.corsHeaders);
const serverPasswordErrorMock = RequestMock().onRequestTo(/\/users\//).respond({
    password: [PASSWORD_ERROR_MESSAGE]
}, 400, config.corsHeaders);
const serverErrorMock = RequestMock().onRequestTo(/\/users\//).respond(null, 500, config.corsHeaders);

fixture `Tests the registration page`
    .page `${config.siteUrl}/register`;

    test.requestHooks(logger)("registering with a username already being used", async (t) => {
        const name = Date.now().toString(10);
        await RestUtil.sendPOST("users/", {
            username: name,
            password: "a",
            email: ""
        });

        await t.typeText(registerPage.username, name)
            .typeText(registerPage.password, "a")
            .click(registerPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/users/") && record.response.statusCode === 400)).ok({timeout: 8000});
        
        await t.expect(registerPage.errorAlert.visible).eql(true);
    });
    
    test("disabling the register button", async (t) => {
        await registerPage.testDisablingSubmit(t);
    });
    
    test.requestHooks(logger, serverUsernameErrorMock)("registering with an server-side username error", async (t) => {
        await t.typeText(registerPage.username, "a_taken_username")
            .typeText(registerPage.password, "a")
            .click(registerPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/users/") && record.response.statusCode === 400)).ok();
        
        await t.expect(registerPage.errorAlert.visible).eql(true)
            .expect(registerPage.errorAlert.innerText).eql(USERNAME_ERROR_MESSAGE);
    });

    test.requestHooks(logger, serverPasswordErrorMock)("registering with an server-side password error", async (t) => {
        await t.typeText(registerPage.username, "a_taken_username")
            .typeText(registerPage.password, "a")
            .click(registerPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/users/") && record.response.statusCode === 400)).ok();
        
        await t.expect(registerPage.errorAlert.visible).eql(true)
            .expect(registerPage.errorAlert.innerText).eql(PASSWORD_ERROR_MESSAGE);
    });

    test.requestHooks(logger, serverErrorMock)("registering with some non-username/password server-side error", async (t) => {
        await t.typeText(registerPage.username, "a_taken_username")
            .typeText(registerPage.password, "a")
            .click(registerPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/users/") && record.response.statusCode === 500)).ok();
        
        await t.expect(registerPage.errorAlert.visible).eql(true);
    });

    test.requestHooks(logger)("successfully registering a new account", async (t) => {
        await t.typeText(registerPage.username, Date.now().toString(10))
            .typeText(registerPage.password, "a")
            .click(registerPage.submitButton)
            .expect(logger.contains(record => record.request.url.includes("/users/") && record.response.statusCode === 201)).ok({timeout: 8000});
        
        await t.expect(registerPage.successAlert.visible).eql(true);
    });

    test("test visiting the login page with the link", async (t) => {
        await t.click(registerPage.switchAction);
        await t.expect(getURL()).contains("/login", {timeout: 8000});
    });