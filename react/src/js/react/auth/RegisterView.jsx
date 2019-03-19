import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import CredentialsForm from "./CredentialsForm";

import AuthActions from "./AuthActions";
import AuthStore from "./AuthStore";

export default class RegisterView extends Reflux.Component {
    constructor() {
        super();
        this.store = AuthStore;
        this.state = {
            enteredUsername: "",
            enteredPassword: ""
        };
    }

    componentDidMount() {
        AuthActions.resetRegistrationNotifications();
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
        AuthActions.handleRegistration(this.state.enteredUsername, this.state.enteredPassword);
    };

    render() {
        return (
            <div className="credentialsPage">
                {
                    this.state.registerErrorMessage && (
                        <Alert bsStyle="danger">
                            {
                                this.state.registerErrorMessage
                            }
                        </Alert>
                    )
                }
                {
                    this.state.isSuccessfullyRegistered && (
                        <Alert bsStyle="success">
                            Your account has been created. It must be approved by an administrator before you can use it.
                        </Alert>
                    )
                }

                <CredentialsForm
                    username={this.state.enteredUsername}
                    password={this.state.enteredPassword}
                    onUsernameChange={this._onUsernameChange}
                    onPasswordChange={this._onPasswordChange}
                    action="Register"
                    onSubmit={this._onSubmit}
                    disableSubmit={this.state.isRegistering}
                    switchActionText="Login to an existing account"
                    switchRoute="/login"
                />
            </div>
        );
    }
}
