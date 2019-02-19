import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import FriendsStore from "./FriendsStore";
import FriendRequestView from "./FriendRequestView";

/**
 * Renders the friend request notifications popover
 */
export default class NotificationsPopover extends Reflux.Component {
    constructor() {
        super();
        this.store = FriendsStore;
    }

    shouldComponentUpdate(nextProps, nextState) {
        return this.state.friendRequests.length !== nextState.friendRequests.length || this.state.isRespondingToRequest !== nextState.isRespondingToRequest;
    }

    render() {
        return (
            <div>
                {
                    this.state.friendRequests.length === 0 && (
                        <h5>You have no friend requests.</h5>
                    )
                }
                {
                    this.state.errorSendingResponse && (
                        <Alert bsStyle="danger">
                            An error occurred while responding to the request.
                        </Alert>
                    )
                }
                {
                    this.state.successfullyRespondedToRequest && (
                        <Alert bsStyle="success">
                            Your response has been recorded.
                        </Alert>
                    )
                }
                {
                    this.state.friendRequests.map((request) => {
                        return (
                            <FriendRequestView key={request.id}
                                request={request}
                                disableActions={this.state.isRespondingToRequest} />
                        );
                    })
                }
            </div>
        );
    }
}
