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
	    hasNextPage: PropTypes.bool
	}

    /**
     * Loads more posts from the database
     */
	 // TODO: call this somehow
    loadMorePosts = () => {
		if (this.props.hasNextPage) {
			this.props.loadMorePosts();
		}
    }

    render() {
        if (this.props.isLoading) {
            return <LoadingComponent />;
        }

        return (
            <div className="post-feed">
                {this.props.posts.map((post) => (
                    <Post key={post.id} post={post} />
                ))}
				{
					this.props.hasNextPage && (<p>Should Load More</p>)
				}
            </div>
        );
    }
}
