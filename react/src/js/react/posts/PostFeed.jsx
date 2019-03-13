import React from "react";
import PropTypes from "prop-types";

import Post from "./Post";
import LoadingComponent from "../misc/LoadingComponent";
/**
 * This is componenet will GET from the posts database to get all the posts.
 * From here it will dynamically create components for all the posts
 */
export default class PostFeed extends React.Component {
	static propTypes = {
	    loadMorePosts: PropTypes.func,
	    posts: PropTypes.oneOfType([
	        PropTypes.array,
	        PropTypes.object
	    ]),
	    isLoading: PropTypes.bool,
	    currentPage: PropTypes.number
	}

    /**
     * GET's to the database
     */
    loadMorePosts = () => {
        this.props.loadMorePosts(this.props.currentPage + 1);
    }

    render() {
        if (this.props.isLoading) {
            return <LoadingComponent />;
        }

        return (
            <div className="post-feed">
                {Object.keys(this.props.posts).map((post, index) => (
                    <Post key={index} post={this.props.posts[post]} />
                ))}
            </div>
        );
    }
}
