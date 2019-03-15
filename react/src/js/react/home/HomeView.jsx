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
        HomeActions.loadPosts(0);
    }

    _loadMorePosts = (pageNumber) => {
        HomeActions.loadPosts(pageNumber);
    };

    render() {
        return (
            <div className="homePage">
                {
                    this.state.errorLoadingPosts && (
                        <Alert bsStyle="danger">
                            An error ocurred while loading posts
                        </Alert>
                    )
                }
                <PostFeed posts={this.state.posts}
                    isLoading={this.state.isLoadingPosts}
                    loadMorePosts={HomeActions.loadPosts}
                />
            </div>
        );
    }
}
