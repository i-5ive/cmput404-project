import React from "react";
import PropTypes from "prop-types";

import { Thumbnail } from "react-bootstrap";

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
        hasNextPage: PropTypes.bool,
        onDeletePost: PropTypes.func,
        onEditPost: PropTypes.func,
        deletingPost: PropTypes.bool,
        errorDeletingPost: PropTypes.bool
    }

    /**
     * Loads more posts from the database
     */
    loadMorePosts = () => {
        if (this.props.hasNextPage) {
            this.props.loadMorePosts();
        }
    }

    // Credit to Brendan McGill for this: https://stackoverflow.com/a/49573628
    handleScroll = (e) => {
        const bottom = e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
        if (bottom) {
            this.loadMorePosts();
        }
    }

    render() {
        return (
            <div className="post-feed" onScroll={(this.props.hasNextPage && !this.props.isLoading) ? this.handleScroll : undefined}>
                {this.props.posts.map((post) => (
                    <Post key={post.id}
                        onDelete={this.props.onDeletePost}
                        onEdit={this.props.onEditPost}
                        isDeleting={this.props.deletingPost === post.id}
                        failedToDeletePost={this.props.errorDeletingPost === post.id}
                        post={post} />
                ))}
                {
                    this.props.isLoading && <LoadingComponent />
                }
                {
                    !this.props.isLoading && this.props.posts.length === 0 && (
                        <Thumbnail className="posts-not-found">
                            No posts were found.
                        </Thumbnail>
                    )
                }
            </div>
        );
    }
}
