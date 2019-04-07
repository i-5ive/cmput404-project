import React from "react";
import Reflux from "reflux";
import { withRouter } from "react-router-dom";

import AuthStore from "../auth/AuthStore";
import NotificationsPopover from "../friends/NotificationsPopover";
import NotificationsBadge from "../friends/NotificationsBadge";
import PostModal from "../posts/PostModal";
import AuthActions from "../auth/AuthActions";

import { Nav, NavItem, OverlayTrigger, Popover, NavDropdown, MenuItem } from "react-bootstrap";

class HeaderProfileDetails extends Reflux.Component {
    constructor() {
        super();
        this.store = AuthStore;
        this.state = {
            showModal: false
        };
    }

    shouldComponentUpdate(nextProps, nextState) {
        return (nextState.isLoggedIn !== this.state.isLoggedIn) ||
            (nextProps.showModal !== this.state.showModal);
    }

    _onSignInClicked = () => {
        this.props.history.push("/login");
    };

    _onProfileClicked = () => {
        this.props.history.push(`/profile/${this.state.userId}`);
    };

    _onSignOutClicked = () => {
        AuthActions.handleLogout();
        this.props.history.push("/");
    };

    renderNotifications() {
        return (
            <span className="notificationsBadge">
                <span className="far fa-bell headerNotifications" aria-hidden="true" />
                <NotificationsBadge />
            </span>
        );
    }

    onCreatePostClicked = () => {
        this.setState({
            showModal: true
        });
    }

    handleClose = () => {
        this.setState({
            showModal: false
        });
    }

    renderCreatePost() {
        return (
            <React.Fragment>
                <span className="createPostBadge" onClick={this.onCreatePostClicked}>
                    <span className="fas fa-pencil-alt" aria-hidden="true" />
                </span>
            </React.Fragment>
        );
    }

    render() {
        const contents = this.state.isLoggedIn ? (
            [
                <NavItem key="create-post" onClick={this.onCreatePostClicked}>
                    {
                        this.renderCreatePost()
                    }
                </NavItem>,
                <OverlayTrigger
                    trigger="click"
                    placement="bottom"
                    key="notifications"
                    overlay={
                        <Popover
                            id="notifications-popover"
                            title="Notifications"
                        >
                            <NotificationsPopover />
                        </Popover>
                    }
                    rootClose
                >
                    <NavItem>
                        {
                            this.renderNotifications()
                        }
                    </NavItem>
                </OverlayTrigger>,
                <NavDropdown key="profile-dropdown-item" title={this.state.username} id="profile-dropdown">
                    <MenuItem key="profile" onClick={this._onProfileClicked}>View Profile</MenuItem>
                    <MenuItem key="signOut" onClick={this._onSignOutClicked}>Sign Out</MenuItem>
                </NavDropdown>
            ]
        ) : (
            <NavItem key="signIn" onClick={this._onSignInClicked}>
                Sign In
            </NavItem>
        );
        return (
            <div className="headerProfile">
                <Nav>
                    {
                        contents
                    }
                </Nav>
                <PostModal
                    show={this.state.showModal}
                    handleClose={this.handleClose}
                />
            </div>
        );
    }
}

export default withRouter(HeaderProfileDetails);
