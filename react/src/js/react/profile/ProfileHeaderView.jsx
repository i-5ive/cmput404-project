import React from "react";
import Reflux from "reflux";

import { Alert, Button } from "react-bootstrap";

import ProfileActions from "./ProfileActions";
import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";
import AuthStore from "../auth/AuthStore";
import EditProfileModal from "./EditProfileModal";

/**
 * Renders the part of the profile page that displays details about an author
 */
export default class ProfileHeaderView extends Reflux.Component {

    constructor(props) {
        super(props);
        this.stores = [ProfileStore, AuthStore];
        this.state = {
            modalVisible: false
        };
    }

    shouldComponentUpdate(nextProps, nextState) {
        return (this.state.modalVisible !== nextState.modalVisible) ||
                (this.state.profileDetails !== nextState.profileDetails) ||
                (this.state.isLoadingProfile !== nextState.isLoadingProfile);
    }

    componentDidMount() {
        ProfileActions.loadProfileDetails(this.props.id);
    }

    _onShowModal = () => {
        ProfileActions.initEditProfileDetails();
        this.setState({
            modalVisible: true
        });
    };

    _onHideModal = () => {
        this.setState({
            modalVisible: false
        });
    };

    renderGithubLink() {
        if (!this.state.profileDetails.github) {
            return null;
        }
        return (
            <a href={this.state.profileDetails.github} className="github" target="_blank">
                Github Profile
            </a>
        );
    }

    renderEditButton() {
        if (this.state.userInfo && this.state.userInfo.id === this.props.id) {
            return (
                <Button bsStyle="primary" onClick={this._onShowModal}>
                    Edit
                </Button>
            );
        }
        return null;
    }

    render() {
        if (this.state.errorLoadingProfile) {
            return (
                <Alert bsStyle="danger">
                    An error occurred while loading the user profile details.
                </Alert>
            );
        } else if (this.state.isLoadingProfile || !this.state.profileDetails) {
            return <LoadingComponent />;
        } 
        return (
            <div className="details">
                <EditProfileModal visible={this.state.modalVisible}
                                id={this.props.id}
                                onClose={this._onHideModal} />
                <h4 className="name">
                    {
                        this.state.profileDetails.displayName
                    }
                </h4>
                <p>
                    {
                        this.state.profileDetails.bio
                    }
                </p>
                <div className="detailsFooter">
                    {
                        this.renderGithubLink()
                    }
                    {
                        this.renderEditButton()
                    }
                </div>
                <hr />
            </div>
        );
    }
}