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
                (this.state.isLoadingProfile !== nextState.isLoadingProfile) ||
                (this.state.isFriendsWithUser !== nextState.isFriendsWithUser);
    }

    componentDidMount() {
        ProfileActions.loadProfileDetails(this.props.id);
        if (this.state.userInfo && this.state.userInfo.id) {
            ProfileActions.loadFriendStatus(this.props.id, this.state.userInfo.id);
        }
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

    _onUnfriendClicked = () => {
        ProfileActions.unfriendUser(this.props.id, this.state.userInfo.id);
    };

    _onCancelRequestClicked = () => {
        ProfileActions.cancelFriendRequest(this.props.id, this.state.userInfo.id);
    };

    _onSendRequestClicked = () => {
        ProfileActions.sendFriendRequest(this.props.id, this.state.userInfo.id);
    };

    renderName() {
        let name = this.state.profileDetails.displayName;
        if (this.state.profileDetails.firstName) {
            name += ` (${this.state.profileDetails.firstName}`;
            if (this.state.profileDetails.lastName) {
                name += ` ${this.state.profileDetails.lastName}`;
            }
            name += ")";
        }
        return (
            <h4 className="name">
                {
                    name
                }
            </h4>
        );
    }

    renderActionButton() {
        if (this.state.userInfo) {
            let text, onClick;
            if (this.state.userInfo.id === this.props.id) {
                text = "Edit";
                onClick = this._onShowModal;
            } else if (!this.state.errorLoadingFriendStatus) {
                if (this.state.isFriendsWithUser) {
                    text = "Unfriend";
                    onClick = this._onUnfriendClicked;
                } else if (this.state.sentFriendRequestToUser) {
                    text = "Cancel friend request";
                    onClick = this._onCancelRequestClicked;
                } else {
                    text = "Send friend request";
                    onClick = this._onSendRequestClicked;
                }
            } else {
                return null;
            }
            return (
                <Button bsStyle="primary" onClick={onClick} disabled={this.state.isProfileActionDisabled}>
                    {
                        text
                    }
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
                {
                    this.renderName()
                }
                <p>
                    {
                        this.state.profileDetails.bio
                    }
                </p>
                <div className="detailsFooter">
                    {
                        this.renderActionButton()
                    }
                </div>
                <hr />
            </div>
        );
    }
}
