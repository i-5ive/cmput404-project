import React from "react";
import Reflux from "reflux";
import { withRouter } from "react-router-dom";

import AuthStore from "../auth/AuthStore";
import NotificationsPopover from "../friends/NotificationsPopover";
import NotificationsBadge from "../friends/NotificationsBadge";
import AuthActions from "../auth/AuthActions";

import { Nav, NavItem, OverlayTrigger, Popover, NavDropdown, MenuItem } from "react-bootstrap";

class HeaderProfileDetails extends Reflux.Component {
    constructor() {
        super();
        this.store = AuthStore;
    }

    shouldComponentUpdate(nextProps, nextState) {
        return nextState.isLoggedIn !== this.state.isLoggedIn;
    }

    _onSignInClicked = () => {
        this.props.history.push("/login");
    };

    _onProfileClicked = () => {
        this.props.history.push(`/profile/${this.state.userInfo.id}`);
    };

    _onSignOutClicked = () => {
        AuthActions.handleLogout();
        this.props.history.push("/");
    };

    renderNotifications() {
        return (
            <OverlayTrigger
                trigger="click"
                placement="bottom"
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
                <span className="notificationsBadge">
                    <span className="glyphicon glyphicon-bell headerNotifications" aria-hidden="true" />
                    <NotificationsBadge />
                </span>
            </OverlayTrigger>
        );
    }

    render() {
        const contents = this.state.isLoggedIn ? (
            [
                <NavItem key="notifications">
                    {
                        this.renderNotifications()
                    }
                </NavItem>,
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
            </div>
        );
    }
}

export default withRouter(HeaderProfileDetails);
