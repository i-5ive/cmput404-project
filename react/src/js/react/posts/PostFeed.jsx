import React from "react";
import Reflux from "reflux";

import CreatePost from "./CreatePost";
import Post from "./Post";

import { PostsStore, PostsActions } from "./PostsStore";
import AuthStore from "../auth/AuthStore";
/**
 * This is componenet will GET from the posts database to get all the posts.
 * From here it will dynamically create components for all the posts
 */
export default class PostFeed extends Reflux.Component {
    constructor() {
        super();
        this.stores = [PostsStore, AuthStore];
    }

    componentDidMount() {
        PostsActions.getPosts();
    }

    render() {
        return (
            <div>
                <div className="filter-posts-wrapper">
                    <p className="filter-posts-text">
                        I want to see:
                    </p>
                    <input type="checkbox" name="Friends" value="Friends" />
                    <label htmlFor="Friends">Friends</label>
                    <input type="checkbox" name="FOAF" value="FOAF" />
                    <label htmlFor="FOAF">FOAF</label>
                    <input type="checkbox" name="Public" value="Public" />
                    <label htmlFor="Public">Public</label>
                </div>
                <CreatePost />
                <div className="post-feed">
                    {this.state.posts.map((post) => (
                        <Post className="post" key={post.id} postId={post.post_id} data={post} />
                    ))}
                </div>
            </div>
        );
    }
}
