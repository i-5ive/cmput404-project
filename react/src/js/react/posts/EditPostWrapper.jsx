import React from "react";
import Reflux from "reflux";

import { Alert } from "react-bootstrap";

import CreateView from "./CreatePost";
import { PostsStore, PostsActions } from "../discover/PostsStore";

import LoadingComponent from "../misc/LoadingComponent";

export default class EditPostWrapper extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = PostsStore;
    }

    componentDidMount() {
        PostsActions.clearEditNotifications();
    }

    render() {
        return (
            <div>
                {
                    this.state.isEditingPost && <LoadingComponent />
                }
                {
                    this.state.errorEditingPost && (
                        <Alert bsStyle="danger">
							An error occurred while editing the post
                        </Alert>
                    )
                }
                {
                    this.state.successfullyEditedPost && (
                        <Alert bsStyle="success">
							The post was successfully updated
                        </Alert>
                    )
                }
                {
                    !this.state.isEditingPost && <CreateView />
                }
            </div>
        );
    }
}
