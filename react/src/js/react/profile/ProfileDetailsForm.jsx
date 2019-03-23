import React from "react";
import Reflux from "reflux";

import { FormGroup, FormControl, ControlLabel } from "react-bootstrap";

import ProfileStore from "./ProfileStore";
import ProfileActions from "./ProfileActions";
import { NAME_REGEX, EMAIL_REGEX, GITHUB_REGEX, ALPHANUMERIC_REGEX } from "../constants/RegexConstants";

const nameValidator = (value, maxLength, allowEmpty = true) => {
        if (value.length === 0) {
            if (!allowEmpty) {
                return "Your name can not be empty.";
            }
        } else if (value.length > maxLength) {
            return `Your name can be no more than ${maxLength} characters long.`;
        } else if (!value.match(NAME_REGEX)) {
            return "Your name must contain only alphanumeric characters, spaces, underscores and dashes.";
        } else if (!value.match(ALPHANUMERIC_REGEX)) {
            return "Your name must contain at least one alphanumeric character.";
        }
        return null;
    },

    getValidationState = (message) => {
        return message ? "error" : null;
    };

/**
 * Renders the form that allows editing a profile
 */
export default class ProfileDetailsForm extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = ProfileStore;
    }

    _onDisplayNameChange = (e) => {
        ProfileActions.setDisplayName(e.target.value);
    };

    _onFirstNameChange = (e) => {
        ProfileActions.setFirstName(e.target.value);
    };

    _onLastNameChange = (e) => {
        ProfileActions.setLastName(e.target.value);
    };

    _onEmailAddressChange = (e) => {
        ProfileActions.setEmailAddress(e.target.value);
    };

    _onGithubLinkChange = (e) => {
        ProfileActions.setGithubLink(e.target.value);
    };

    _onBioChange = (e) => {
        ProfileActions.setBio(e.target.value);
    };

    _validateDisplayName(value) {
        return nameValidator(value, 80, false);
    }

    _validateName(value) {
        return nameValidator(value, 30);
    }

    _validateEmail(value) {
        if (value.length > 0 && !value.match(EMAIL_REGEX)) {
            return "This is not a valid email address.";
        } else if (value.length > 80) {
            return "Your email address can be no more than 80 characters long.";
        }
        return null;
    }

    _validateGithub(value) {
        if (value.length > 0 && !value.match(GITHUB_REGEX)) {
            return "This is not a valid link to a github account.";
        }
        return null;
    }

    _validateBio(value) {
        if (value.length > 1024) {
            return "Your description can be no more than 1024 characters.";
        }
        return null;
    }

    renderElement(id, errorMessage, label, placeholder, value, onChange, inputType = "text", autoFocus = false, componentClass = undefined, rows = undefined) {
        return (
            <FormGroup controlId={id} validationState={getValidationState(errorMessage)}>
                <ControlLabel>{label}</ControlLabel>
                <FormControl type={inputType}
                    placeholder={placeholder}
                    value={value}
                    onChange={onChange}
                    autoFocus={autoFocus}
                    componentClass={componentClass}
                    rows={rows}
                />
                {
                    errorMessage && (
                        <h5 className="error-text">
                            {
                                errorMessage
                            }
                        </h5>
                    )
                }
            </FormGroup>
        );
    }

    render() {
        const validity = {
            displayName: this._validateDisplayName(this.state.editProfileDetails.displayName),
            firstName: this._validateName(this.state.editProfileDetails.firstName),
            lastName: this._validateName(this.state.editProfileDetails.lastName),
            email: this._validateEmail(this.state.editProfileDetails.email),
            github: this._validateGithub(this.state.editProfileDetails.github),
            bio: this._validateBio(this.state.editProfileDetails.bio)
        };
        return (
            <div>
                {
                    this.renderElement("displayName", validity.displayName, "Display name",
                        "Enter the name that you want other users to see", this.state.editProfileDetails.displayName,
                        this._onDisplayNameChange, "text", true)
                }

                {
                    this.renderElement("firstName", validity.firstName, "First name",
                        "Enter your first name", this.state.editProfileDetails.firstName,
                        this._onFirstNameChange)
                }
                {
                    this.renderElement("lastName", validity.lastName, "Last name",
                        "Enter your last name", this.state.editProfileDetails.lastName,
                        this._onLastNameChange)
                }

                {
                    this.renderElement("email", validity.email, "Email address",
                        "Enter your email address", this.state.editProfileDetails.email,
                        this._onEmailAddressChange, "email")
                }
                {
                    this.renderElement("github", validity.github, "Github account",
                        "Enter the link to your github account (ex: https://github.com/your_github_username)", this.state.editProfileDetails.github,
                        this._onGithubLinkChange, "url")
                }
                {
                    this.renderElement("bio", validity.bio, "Description",
                        "Enter a description about you to show in your profile", this.state.editProfileDetails.bio,
                        this._onBioChange, "text", false, "textarea", "6")
                }
            </div>
        );
    }
}
