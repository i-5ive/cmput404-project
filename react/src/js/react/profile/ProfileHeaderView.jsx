import React from "react";
import Reflux from "reflux";

import { Alert, Button } from "react-bootstrap";

import ProfileActions from "./ProfileActions";
import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";
import AuthStore from "../auth/AuthStore";
import EditProfileModal from "./EditProfileModal";
import {createSummaryQuery, getAuthorUrl} from "../util/AuthorUtil";

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
                (this.state.isProfileActionDisabled !== nextState.isProfileActionDisabled) ||
                (this.state.isLoadingFollowStatus !== nextState.isLoadingFollowStatus);
    }

    _isLoggedInUser() {
        return (this.state.userId === this.props.id) || (this.state.userInfo && this.state.userInfo.id && this.props.id === this.state.userInfo.id);
    }

    componentDidMount() {
        ProfileActions.loadProfileDetails(this.props.id);
        if (!this._isLoggedInUser() && this.state.userId) {
            ProfileActions.loadFollowStatus(this.props.id, this.state.userId);
        }
    }

    componentDidUpdate(prevProps, prevState) {
        // handles user coming immediately to a profile (from entering the direct url) without visiting some other page first
        if (this.state.userId && !prevState.userId && !this._isLoggedInUser()) {
            ProfileActions.loadFollowStatus(this.props.id, this.state.userId);
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

    _onUnfollowClicked = () => {
        const author = createSummaryQuery(getAuthorUrl(this.props.id), this.state.profileDetails.displayName);
        ProfileActions.unfollowUser(author, this.state.userInfo);
    };

    _onSendRequestClicked = () => {
        const author = createSummaryQuery(getAuthorUrl(this.props.id), this.state.profileDetails.displayName);
        ProfileActions.sendFriendRequest(author, this.state.userInfo);
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
            } else if (!this.state.errorLoadingFollowStatus && !this.state.isLoadingFollowStatus) {
                if (this.state.isFollowingUser) {
                    text = "Unfollow";
                    onClick = this._onUnfollowClicked;
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

    renderActionNotification() {
        if (this.state.profileActionError) {
            return (
                <Alert bsStyle="danger">
                    {
                        this.state.profileActionError
                    }
                </Alert>
            );
        } else if (this.state.profileActionSuccess) {
            return (
                <Alert bsStyle="success">
                    {
                        this.state.profileActionSuccess
                    }
                </Alert>
            );
        } else if (this.state.isProfileActionDisabled) {
            return <LoadingComponent />;
        } else if (this.state.errorLoadingFollowStatus) {
            return (
                <Alert bsStyle="danger">
                    An error occurred while loading your follow status with this author
                </Alert>
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
                        this.renderActionNotification()
                    }
                    {
                        this.renderActionButton()
                    }
                </div>
                <hr />
            </div>
        );
    }
}
