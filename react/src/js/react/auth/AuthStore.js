import Reflux from "reflux";

import Actions from "./AuthActions";

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

		if (process.env.NODE_ENV === "development"){
			window.DEV_AUTH_STORE = this;
		}
    }

	/**
	 * Handles a user's login attempt
	 * @param {String} username - the username that a user is attempting to log in with
	 * @param {String} password - the password that a user is attempting to log in with
	 */
	onHandleLogin(username, password) {
		this.setState({
			isLoggingIn: true
		});
		
		// TODO: wait for request made to server
		this.setState({
			isLoggingIn: false,
			isLoggedIn: true,
			username: username
		});
	}
}