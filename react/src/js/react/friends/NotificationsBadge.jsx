import React from "react";
import Reflux from "reflux";

import FriendsStore from "./FriendsStore";
import { Badge } from "react-bootstrap";

export default class NotificationsBadge extends Reflux.Component {
    constructor() {
        super();
        this.store = FriendsStore;
    }

    shouldComponentUpdate(nextProps, nextState) {
        return this.state.friendRequests.length !== nextState.friendRequests.length;
    }

    render() {
        if (this.state.friendRequests.length === 0) {
            return null;
        }
        return (
            <Badge pill="true" variant="danger">
                {
                    this.state.friendRequests.length
                }
            </Badge>
        );
    }
}
