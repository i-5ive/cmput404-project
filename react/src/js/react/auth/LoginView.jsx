import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import CredentialsForm from "./CredentialsForm";

import AuthActions from "./AuthActions";
import AuthStore from "./AuthStore";

export default class LoginView extends Reflux.Component {
    constructor() {
        super();
        this.store = AuthStore;
        this.state = {
            enteredUsername: "",
            enteredPassword: ""
        };
    }

    _redirectToHome() {
        this.props.history.push("/");
    }

    componentDidMount() {
        AuthActions.resetLoginNotifications();
        if (this.state.isLoggedIn) {
            this._redirectToHome();
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.isLoggedIn && !prevState.isLoggedIn) {
            this._redirectToHome();
        }
    }

    _onUsernameChange = (e) => {
        this.setState({
            enteredUsername: e.target.value
        });
    };

    _onPasswordChange = (e) => {
        this.setState({
            enteredPassword: e.target.value
        });
    };

    _onSubmit = () => {
        AuthActions.handleLogin(this.state.enteredUsername, this.state.enteredPassword);
    };

    render() {
        return (
            <div className="credentialsPage">
                {
                    this.state.loginErrorMessage && (
                        <Alert bsStyle="danger">
                            {
                                this.state.loginErrorMessage
                            }
                        </Alert>
                    )
                }
                <CredentialsForm
                    username={this.state.enteredUsername}
                    password={this.state.enteredPassword}
                    onUsernameChange={this._onUsernameChange}
                    onPasswordChange={this._onPasswordChange}
                    action="Sign In"
                    onSubmit={this._onSubmit}
                    disableSubmit={this.state.isLoggingIn}
                    switchActionText="Register for a new account"
                    switchRoute="/register"
                />
            </div>
        );
    }
}
