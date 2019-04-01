import Reflux from "reflux";

import cookie from "cookie";
import _ from "lodash";

import Actions from "./AuthActions";
import RestUtil from "../util/RestUtil";
import { HOST_URL } from "../constants/ServerConstants";
import CookieUtil from "../util/CookieUtil";

import HomeActions from "../home/HomeActions";

const getLoginStateFromCookies = () => {
    const cookies = cookie.parse(document.cookie),
        username = cookies["core-username"],
        id = cookies["core-userid"],
        password = cookies["core-password"],
        url = `${HOST_URL}/author/${id}`;
    if (!username || !id || !password) {
        return null;
    }
    return {
        username: username,
        userInfo: {
            id: url,
            host: HOST_URL,
            displayName: username,
            url: url
        },
        userId: id,
        password: password
    };
};

/**
 * This store keeps track of the state of components that deal with user authentication
 */
export default class AuthStore extends Reflux.Store {
    constructor() {
        super();
        this.state = {
            isLoggedIn: false
        };
        this.listenables = Actions;

        if (process.env.NODE_ENV === "development") {
            window.DEV_AUTH_STORE = this;
        }
    }

    onResetRegistrationNotifications() {
        this.setState({
            isSuccessfullyRegistered: false,
            registerErrorMessage: null
        });
    }

    onResetLoginNotifications() {
        this.setState({
            loginErrorMessage: null
        });
    }

    _onLogin(userInfo) {
    // TODO: any actions to perform after logging in
    }

    /**
     * Parses cookies to update the user's login state
     */
    onParseLoginCookies() {
        const state = getLoginStateFromCookies();
        if (state) {
            Object.assign(state, {
                isLoggedIn: true
            });
            this.setState(state);
            this._onLogin(state.userInfo);
        }
    }

    /**
     * Handles a user registering for a new account
     * @param {String} username - the username of the account
     * @param {String} password - the password of the account
     */
    onHandleRegistration(username, password) {
        this.setState({
            isRegistering: true,
            isSuccessfullyRegistered: false,
            registerErrorMessage: null
        });

        RestUtil.sendPOST("users/", {
            username: username,
            password: password,
            email: ""
        }, false).then((res) => {
            this.setState({
                isRegistering: false,
                isSuccessfullyRegistered: true
            });
        }).catch((err) => {
            const message = _.get(err, "response.data.username[0]") || _.get(err, "response.data.password[0]", "An error happened while creating your account.");
            this.setState({
                isRegistering: false,
                registerErrorMessage: message
            });
            console.error(err);
        });
    }

    /**
     * Handles a user's login attempt
     * @param {String} username - the username that a user is attempting to log in with
     * @param {String} password - the password that a user is attempting to log in with
     */
    onHandleLogin(username, password) {
        this.setState({
            isLoggingIn: true,
            isLoggedIn: false,
            loginErrorMessage: null
        });

        RestUtil.sendPOST("login/", {
            query: "login",
            username: username,
            password: password
        }, false).then((res) => {
            CookieUtil.setCookie("core-username", username);
            CookieUtil.setCookie("core-password", password);
            CookieUtil.setCookie("core-userid", res.data.userId);
            const loginState = getLoginStateFromCookies();
            this.setState(Object.assign(loginState, {
                isLoggingIn: false,
                isLoggedIn: true
            }));
            this._onLogin(loginState.userInfo);
        }).catch((err) => {
            this.setState({
                isLoggingIn: false,
                loginErrorMessage: _.get(err, "response.data.message", "An error occurred while logging in.")
            });
            console.error(err);
        });
    }

    /**
     * Handles the user logging out of the application
     */
    onHandleLogout() {
        CookieUtil.deleteCookie("core-username");
        CookieUtil.deleteCookie("core-userid");
        CookieUtil.deleteCookie("core-password");
        this.setState({
            isLoggedIn: false,
            username: null,
            userInfo: null,
            userId: null
        });
        HomeActions.reloadPosts();
    }
}
