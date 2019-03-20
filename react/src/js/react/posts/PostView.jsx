import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import { PostsStore, PostsActions } from "../discover/PostsStore";
import LoadingComponent from "../misc/LoadingComponent";
import Post from "./Post";

/**
 * Renders details about one specific post
 */
export default class PostView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = PostsStore;
    }

    componentDidMount() {
        PostsActions.getPost(this.props.match.params.id);
    }

    render() {
        if (this.state.failedToFetchPost) {
            return <Alert bsStyle="danger">An error occurred while fetching the post</Alert>;
        } else if (!this.state.currentPost) {
            return (
                <div className="center-loader">
                    <LoadingComponent />
                </div>
            );
        }
        return (
            <div className="postView">
                <Post
                    post={this.state.currentPost}
                    images={this.state.currentPostImages}
                    isPostView />
            </div>
        );
    }
}
