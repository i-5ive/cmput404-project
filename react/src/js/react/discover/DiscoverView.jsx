import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import PostFeed from "../posts/PostFeed";
import { PostsStore, PostsActions } from "./PostsStore";

/**
 * Displays details about all public posts across all servers
 */
export default class DiscoverView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = PostsStore;
    }

    componentDidMount() {
        PostsActions.getPosts();
    }

    _loadMorePosts = () => {
        PostsActions.getPosts(this.state.nextPage);
    };

    render() {
        return (
            <div className="discoverPage">
                {
                    this.state.failedToFetchPosts && (
                        <Alert bsStyle="danger">
							An error occurred while fetching posts.
                        </Alert>
                    )
                }
                <PostFeed posts={this.state.posts}
                    isLoading={this.state.fetchingPosts}
                    loadMorePosts={this._loadMorePosts}
                    onDeletePost={PostsActions.deletePost}
                    onEditPost={PostsActions.editPost}
                    hasNextPage={Boolean(this.state.nextPage)}
                    errorDeletingPost={this.state.failedToDeletePost}
                    deletingPost={this.state.deletingPost}
                />
            </div>
        );
    }
}
