import React from "react";
import Reflux from "reflux";

import { PostsStore, PostsActions } from "../discover/PostsStore";
import LoadingComponent from "../misc/LoadingComponent";
import Post from "./Post";

export default class PostView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = PostsStore;
    }

    componentDidMount() {
        PostsActions.getPost(this.props.match.params.id);
    }

    render() {
        if (this.state.currentPost.length === 0) {
            return <LoadingComponent />;
        }
        return (
            <div className="postView">
                <Post
                    post={this.state.currentPost} />
            </div>
        );
    }
}
