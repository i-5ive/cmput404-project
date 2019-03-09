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
	    loadMorePosts: PropTypes.function,
	    posts: PropTypes.array,
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
          {this.props.posts.map(post => (
            <Post key={post} post={post} />
          ))}
        </div>
      );
    }
}
