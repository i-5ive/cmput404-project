import React from "react";

import PostFeed from "../posts/PostFeed";

/**
 * Displays details about all public posts
 */
export default class DiscoverView extends React.Component {
    // TODO: same concept as HomeView but without the user logged in
    render() {
        return (
            <div className="discoverPage">
                <PostFeed posts={[]} isLoading />
            </div>
        );
    }
}
