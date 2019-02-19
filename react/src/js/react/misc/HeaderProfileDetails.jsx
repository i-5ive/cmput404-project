import React from "react";
import Reflux from "reflux";
import { withRouter } from "react-router-dom";

import AuthStore from "../auth/AuthStore";
import NotificationsPopover from "../friends/NotificationsPopover";
import NotificationsBadge from "../friends/NotificationsBadge";

import { Nav, NavItem, OverlayTrigger, Popover } from "react-bootstrap";

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
                <NavItem key="name">
                    {
                        this.state.username
                    }
                </NavItem>
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
