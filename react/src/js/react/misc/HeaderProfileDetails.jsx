import React from "react";
import Reflux from "reflux";

import AuthStore from "../auth/AuthStore";

import { Nav, NavItem, Badge, OverlayTrigger, Popover } from "react-bootstrap";

export default class HeaderProfileDetails extends Reflux.Component {
    constructor() {
        super();
        this.store = AuthStore;
    }

    renderNotifications() {
        // TODO: only render the Badge if there is atleast one notification
        // TODO: render the number of notifications
        return (
            <OverlayTrigger
                trigger="click"
                placement="bottom"
                overlay={
                    <Popover
                        id="notifications-popover"
                        title="Notifications"
                    >
                        WOWWWWW A DROPDOWN!
                    </Popover>
                }
                rootClose
            >
                <span className="notificationsBadge">
                    <span className="glyphicon glyphicon-bell headerNotifications" aria-hidden="true" />
                    {
                        true && (
                            <Badge pill="true" variant="danger">
                                0
                            </Badge>
                        )
                    }
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
        ) : <NavItem>Sign In</NavItem>;
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
