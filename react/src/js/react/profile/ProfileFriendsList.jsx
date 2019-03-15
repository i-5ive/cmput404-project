import React from "react";
import Reflux from "reflux";

import ProfileStore from "./ProfileStore";
import LoadingComponent from "../misc/LoadingComponent";
import { Link } from "react-router-dom";
import { isExternalAuthor } from "../util/AuthorUtil";

/**
 * Renders a user's list of friends
 */
export default class ProfileFriendsList extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = ProfileStore;
    }

    shouldComponentUpdate(prevProps, prevState) {
        return this.state.profileDetails !== prevState.profileDetails;
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
        if (!this.state.profileDetails) {
            return <LoadingComponent />;
        } else if (this.state.profileDetails.friends.length === 0) {
            return <h5>This user has no friends.</h5>;
        }
        return (
            <div>
                {
                    this.state.profileDetails.friends.map(this.renderFriendDetails)
                }
            </div>
        );
    }
}
