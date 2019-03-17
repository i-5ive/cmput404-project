import React from "react";
import Reflux from "reflux";

import PropTypes from "prop-types";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";

import AuthStore from "../auth/AuthStore";
import FriendsActions from "./FriendsActions";

/**
 * Renders a friend request
 */
class FriendRequestView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = AuthStore;
    }

    shouldComponentUpdate(nextProps) {
        return nextProps.disableActions !== this.props.disableActions || nextProps.request.id !== this.props.request.id;
    }

    _onApproveClicked = () => {
        FriendsActions.respondToFriendRequest(this.state.userId, this.props.request, true);
    };

    _onRejectClicked = () => {
        FriendsActions.respondToFriendRequest(this.state.userId, this.props.request, false);
    };

    render() {
        return (
            <div className="friendRequest">
                <Link className="name" to={`/profile/${encodeURIComponent(this.props.request.id)}/`}>
                    {
                        this.props.request.displayName
                    }
                </Link>
                <div className="buttons">
                    <Button bsStyle="primary"
                        onClick={this._onApproveClicked}
                        disabled={this.props.disableActions}>
                        Accept
                    </Button>
                    <Button onClick={this._onRejectClicked}
                        disabled={this.props.disableActions}>
                        Reject
                    </Button>
                </div>
            </div>
        );
    }
}

FriendRequestView.propTypes = {
    request: PropTypes.object,
    disableActions: PropTypes.bool
};

export default FriendRequestView;
