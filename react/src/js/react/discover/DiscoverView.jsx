import React from "react";
import Reflux from "reflux";

import PostFeed from "../posts/PostFeed";
import { PostsStore, PostsActions } from "./PostsStore";

/**
 * Displays details about all public posts
 */
export default class DiscoverView extends Reflux.Component {
    // TODO: same concept as HomeView but without the user logged in
    constructor(props) {
        super(props);
        this.store = PostsStore;
        this.state = {
            currentPageNumber: 1
        };
    }

    componentDidMount() {
        this._loadMorePosts(1);
    }

    _loadMorePosts = (pageNumber) => {
        PostsActions.getPosts(pageNumber);
    };

    render() {
        return (
            <div className="discoverPage">
                <PostFeed posts={this.state.posts}
                    isLoading={this.state.fetchingPosts}
                    loadMorePosts={this._loadMorePosts}
                    currentPage={this.state.currentPageNumber}
                />
            </div>
        );
    }
}
