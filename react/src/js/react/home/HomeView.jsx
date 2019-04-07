import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import PostFeed from "../posts/PostFeed";

import HomeStore from "./HomeStore";
import HomeActions from "./HomeActions";

/**
 * Displays posts visible to the currently logged in user
 */
export default class HomeView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = HomeStore;
    }

    componentDidMount() {
        HomeActions.loadPosts();
    }

    _loadMorePosts = () => {
        HomeActions.loadPosts(this.state.nextPage);
    };

    render() {
        return (
            <div className="homePage">
                {
                    this.state.errorLoadingPosts && (
                        <Alert bsStyle="danger">
                            An error occurred while loading posts
                        </Alert>
                    )
                }
                <PostFeed posts={this.state.posts}
                    isLoading={this.state.isLoadingPosts}
                    loadMorePosts={this._loadMorePosts}
                    onDeletePost={HomeActions.deletePost}
                    onEditPost={HomeActions.editPost}
                    hasNextPage={Boolean(this.state.nextPage)}
                    errorDeletingPost={this.state.failedToDeletePost}
                    deletingPost={this.state.deletingPost}
                />
            </div>
        );
    }
}
