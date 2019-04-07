import React from "react";
import Reflux from "reflux";

import { Alert, Modal, ModalBody, ModalHeader, ModalFooter, ModalTitle, Button } from "react-bootstrap";

import LoadingComponent from "../misc/LoadingComponent";
import ProfileStore from "./ProfileStore";
import ProfileActions from "./ProfileActions";
import ProfileDetailsForm from "./ProfileDetailsForm";

/**
 * Renders the modal that allows editing the currently selected profile
 */
export default class EditProfileModal extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = ProfileStore;
    }

    shouldComponentUpdate(nextProps, nextState) {
        return (this.state.isSavingProfile !== nextState.isSavingProfile) ||
            (this.props.visible !== nextProps.visible) ||
            (this.state.canSaveProfile !== nextState.canSaveProfile);
    }

    componentDidUpdate(prevProps, prevState) {
        if (!this.state.isSavingProfile && prevState.isSavingProfile && this.state.successfullySavedProfile) {
            this.props.onClose();
        }
    }

    _onSaveClicked = () => {
        ProfileActions.saveProfileDetails(this.props.id, this.state.editProfileDetails);
    };

    render() {
        return (
            <Modal show={this.props.visible} onHide={this.props.onClose}>
                <ModalHeader closeButton>
                    <ModalTitle>Edit Profile</ModalTitle>
                </ModalHeader>
                <ModalBody>
                    {
                        this.state.isSavingProfile && <LoadingComponent />
                    }
                    {
                        this.state.errorSavingProfile && (
                            <Alert bsStyle="danger">
                                An error occurred while updating your profile.
                            </Alert>
                        )
                    }
                    {
                        this.state.successfullySavedProfile && (
                            <Alert bsStyle="success">
                                Your profile was successfully updated.
                            </Alert>
                        )
                    }
                    <ProfileDetailsForm />
                </ModalBody>
                <ModalFooter>
                    <Button onClick={this.props.onClose}>
                        Exit
                    </Button>
                    <Button bsStyle="primary"
                        onClick={this._onSaveClicked}
                        disabled={this.state.isSavingProfile || !this.state.canSaveProfile}>
                        Save
                    </Button>
                </ModalFooter>
            </Modal>
        );
    }
}
