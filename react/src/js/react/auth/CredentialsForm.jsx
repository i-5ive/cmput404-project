import React from "react";
import PropTypes from "prop-types";

import { Link } from "react-router-dom";
import { Button, FormGroup, FormControl, ControlLabel } from "react-bootstrap";

import { INVERSE_ALPHANUMERIC_REGEX } from "../constants/RegexConstants";

const validateUsername = (field) => {
        if (field.length >= 150) {
            return "Your username is too long. It must be less than 150 characters.";
        } else if (field.length === 0) {
            return "Your username can't be empty.";
        } else if (field.match(INVERSE_ALPHANUMERIC_REGEX)) {
            return "Your username can only contain alphanumeric characters and underscores.";
        }
        return null;
    },

    validatePassword = (field) => {
        if (field.length >= 150) {
            return "Your password is too long. It must be less than 150 characters.";
        } else if (field.length === 0) {
            return "Your password can't be empty.";
        }
        return null;
    },

    getValidationState = (message) => {
        return message ? "error" : null;
    },

    CredentialsForm = (props) => {
        const usernameMessage = validateUsername(props.username),
            passwordMessage = validatePassword(props.password),
            usernameState = getValidationState(usernameMessage),
            passwordState = getValidationState(passwordMessage);
        return (
            <div>
                <h3>
                    {
                        props.action
                    }
                </h3>
                <FormGroup controlId="username" validationState={usernameState}>
                    <ControlLabel>Username</ControlLabel>
                    <FormControl
                        type="username"
                        value={props.username}
                        onChange={props.onUsernameChange}
                        autoFocus
                        placeholder="Username" />
                    {
                        usernameState && (
                            <h5>
                                {
                                    usernameMessage
                                }
                            </h5>
                        )
                    }
                </FormGroup>
                <FormGroup controlId="password" validationState={passwordState}>
                    <ControlLabel>Password</ControlLabel>
                    <FormControl
                        value={props.password}
                        onChange={props.onPasswordChange}
                        type="password"
                        placeholder="Password" />
                    {
                        passwordState && (
                            <h5>
                                {
                                    passwordMessage
                                }
                            </h5>
                        )
                    }
                </FormGroup>

                <Button bsStyle="primary"
                    onClick={props.onSubmit}
                    disabled={props.disableSubmit || Boolean(passwordState || usernameState)}>
                    {
                        props.action
                    }
                </Button>
                <Link to={props.switchRoute} className="credentialsSwitchAction">
                    {
                        props.switchActionText
                    }
                </Link>
            </div>
        );
    };

CredentialsForm.propTypes = {
    username: PropTypes.string,
    password: PropTypes.string,
    onUsernameChange: PropTypes.func,
    onPasswordChange: PropTypes.func,
    action: PropTypes.string,
    onSubmit: PropTypes.func,
    disableSubmit: PropTypes.bool,
    switchActionText: PropTypes.string,
    switchRoute: PropTypes.string
};

export default CredentialsForm;
