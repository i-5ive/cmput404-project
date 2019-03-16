import React from "react";
import Reflux from "reflux";
import PropTypes from "prop-types";

import ReactMarkdown from "react-markdown";
import { withRouter, Link } from "react-router-dom";
import { PostsStore, PostsActions } from "../discover/PostsStore";
import { Thumbnail, Button } from "react-bootstrap";
import { formatDate } from "../util/DateUtil";
import AuthStore from "../auth/AuthStore";

/**
 * Displays a singular post
 */
class Post extends Reflux.Component {
    static propTypes = {
        post: PropTypes.object.isRequired,
        isPostView: PropTypes.bool,
		images: PropTypes.array
    }

    static defaultProps ={
        isPostView: false
    }

    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
    }

    renderHeaderButtons = () => {
        // TODO Add edit button
        const isCurrentUser = (this.props.post.author.id === this.state.userId);
        return (
            <div className="buttons">
                <i className="fas fa-user-lock">{this.props.post.visibility}</i>
                <Button
                    variant="primary"
                    className="permalink-button"
                    onClick={this.handlePermalink}>
                    <i className="fas fa-link" />
                </Button>
                {isCurrentUser
                    ? <Button
                        variant="primary"
                        className="delete-button"
                        onClick={this.handleDeletePost}>
                        <i className="far fa-trash-alt" />
                    </Button>
                    : null }
            </div>
        );
    }

    // From VinayC, https://stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html
    renderContent = (posts) => {
        const contentList = [];
        posts.forEach((post, index) => {
            const { contentType, content } = post;
            if (contentType === "image/png;base64" || contentType === "image/jpeg;base64") {
                const name = `data:${contentType},${content}`;
                contentList.push(<img key={`image-${index}`} className="post-image" src={name} />);
            } else if (contentType === "text/markdown") {
                contentList.push(<ReactMarkdown key={post.id} source={content} />);
            } else {
                contentList.push(<span key={`text-${index}`} className="post-text">{content}</span>);
            }
        });
        return contentList;
    }

    // TODO
    renderComments() {
        return null;
    }

    renderFooter() {
        const commentsLength = this.props.post.comments.length;
        return (
            <div className="post-footer">
                <p className="categories">{this.props.post.categories}</p>
                { commentsLength ? <a onClick={this.handlePermalink}>{`${commentsLength} comments`}</a> : null}
            </div>
        );
    }

    handleDeletePost = () => {
        PostsActions.deletePost(this.props.post.id, this.props.post.post_id);
    }

    handlePermalink = () => {
        this.props.history.push(`/post/${this.props.post.id}`);
    }

    render() {
        const post = this.props.post;
		let posts = [post];
		if (this.props.images) {
			posts = posts.concat(this.props.images);
		}
        return (
            <Thumbnail>
                <div className="post-header">
                    <p className="post-time">
                        Posted by <Link to={`/profile/${encodeURIComponent(post.author.url)}/`}>{post.author.displayName}</Link> on {formatDate(post.published)}
                    </p>
                    {!this.props.isPostView ? this.renderHeaderButtons() : null}
                </div>
                <h3 className="post-title">{this.props.post.title}</h3>
                <p className="post-desc">{this.props.post.description}</p>
                <div className="post-body">
                    {
                        this.renderContent(posts)
                    }
                </div>
                {this.renderFooter()}
                {
                    this.renderComments()
                }
            </Thumbnail>
        );
    }
}

export default withRouter(Post);
