import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import ProfileStore from "./ProfileStore";
import ProfileActions from "./ProfileActions";
import LoadingComponent from "../misc/LoadingComponent";
import { Link } from "react-router-dom";
import { isExternalAuthor } from "../util/AuthorUtil";

/**
 * Renders a list of users that a specific user is following
 */
export default class ProfileFollowedUsers extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = ProfileStore;
    }

    componentDidMount() {
        ProfileActions.loadFollowedUsers(this.props.id);
    }

    renderFriendDetails(friend) {
        return (
            <div className="friendSummary" key={friend.id}>
                <Link to={`/profile/${encodeURIComponent(friend.id)}/`}>
                    {
                        friend.displayName
                    }
                </Link>
                <h5>
                    {
                        isExternalAuthor(friend.id) ? "External Author" : "Local Author"
                    }
                </h5>
            </div>
        );
    }

    render() {
        if (this.state.isLoadingFollowedUsers) {
            return <LoadingComponent />;
        } else if (this.state.failedToLoadFollowed) {
            return (
                <Alert bsStyle="danger">
                    An error occurred while loading followed users.
                </Alert>
            );
        } else if (this.state.followedUsers.length === 0) {
            return <h5>This user is not following anyone.</h5>;
        }
        return (
            <div>
                {
                    this.state.followedUsers.map(this.renderFriendDetails)
                }
            </div>
        );
    }
}
