import React from "react";
import Reflux from "reflux";
import PropTypes from "prop-types";

import ReactMarkdown from "react-markdown";
import { withRouter, Link } from "react-router-dom";
import { Thumbnail, Button, Badge, Alert } from "react-bootstrap";
import { formatDate } from "../util/DateUtil";
import AuthStore from "../auth/AuthStore";

import LoadingComponent from "../misc/LoadingComponent";

/**
 * Displays a singular post
 */
class Post extends Reflux.Component {
    static propTypes = {
        post: PropTypes.object.isRequired,
        isPostView: PropTypes.bool,
        images: PropTypes.array,
        onDelete: PropTypes.func,
        failedToDeletePost: PropTypes.bool,
        isDeleting: PropTypes.bool
    }

    static defaultProps ={
        isPostView: false
    }

    constructor(props) {
        super(props);
        this.store = AuthStore;
    }

    renderHeaderButtons = () => {
        if (this.props.post.categories.includes("github")) {
            return null;
        }
        // TODO Add edit button
        const isCurrentUser = this.state.isLoggedIn && (this.props.post.author.id === this.state.userInfo.id);
        return (
            <div className="buttons">
                <Button
                    bsStyle="primary"
                    className="permalink-button"
                    disabled={this.props.isDeleting}
                    onClick={this.handlePermalink}>
                    <i className="fas fa-link" />
                </Button>
                {isCurrentUser
                    ? <Button
                        bsStyle="danger"
                        className="delete-button"
                        disabled={this.props.isDeleting}
                        onClick={this.handleDeletePost}>
                        <i className="far fa-trash-alt" />
                    </Button>
                    : null }
            </div>
        );
    }

    // From VinayC, https://stackoverflow.com/a/8499716
    renderContent = (posts) => {
        if (posts.length === 1 && !posts[0].content) {
            return (
                <div className="empty">
					This post has no content.
                </div>
            );
        }
        const contentList = [];
        posts.forEach((post, index) => {
            const { contentType, content } = post;
            if (contentType === "image/png;base64" || contentType === "image/jpeg;base64") {
                const name = `data:${contentType},${content}`;
                contentList.push(<br key={`break-${index}`} />);
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

    renderCategory(category) {
        return (
            <Badge key={category} className="category-badge">
                {
                    category
                }
            </Badge>
        );
    }

    renderTotalComments(commentsLength) {
        const text = `${commentsLength} comments`;
        if (this.props.isPostView) {
            return (
                <span className="comments-count">
                    {text}
                </span>
            );
        }
        return (
            <Link className="comments-count" to={`/post/${this.props.post.id}/`}>
                {text}
            </Link>
        );
    }

    renderFooter() {
        const commentsLength = this.props.post.comments.length;
        return (
            <div>
                <div className="categories-wrapper">
                    <span className="glyphicon glyphicon-tags" />
                    {
                        this.props.post.categories.length === 0 && (
                            <span>
								No categories
                            </span>
                        )
                    }
                    {
                        this.props.post.categories.map(this.renderCategory)
                    }
                </div>
                <div className="bottom-row">
                    <span className="glyphicon glyphicon-comment" />
                    {
                        this.renderTotalComments(commentsLength)
                    }
                    <div className="visibility-details">
                        <span className="glyphicon glyphicon-eye-open" />
                        <span className="visibility-text">{this.props.post.visibility}</span>
                    </div>
                </div>

            </div>
        );
    }

	handlePermalink = () => {
	    this.props.history.push(`/post/${this.props.post.id}/`);
	};

    handleDeletePost = () => {
        this.props.onDelete(this.props.post.id, this.props.post.post_id);
    }

    renderTitle() {
        if (this.props.post.title) {
            return <h3 className="post-title">{this.props.post.title}</h3>;
        }
        return (
            <h3 className="empty">
				No title
            </h3>
        );
    }

    render() {
        if (this.props.isDeleting) {
            return (
                <Thumbnail>
                    <div>
                        <LoadingComponent />
                        <span className="deleting-message">
							This post is being deleted.
                        </span>
                    </div>
                </Thumbnail>
            );
        }

        const post = this.props.post;
        let posts = [post];
        if (this.props.images) {
            posts = posts.concat(this.props.images);
        }
        return (
            <Thumbnail>
                {
                    this.props.failedToDeletePost && (
                        <Alert bsStyle="danger">
							An error occurred while deleting the post.
                        </Alert>
                    )
                }
                <div className="post-header">
                    {
                        this.renderTitle()
                    }
                    {!this.props.isPostView ? this.renderHeaderButtons() : null}
                </div>
                <div className="post-time">
					Posted by <Link to={`/profile/${encodeURIComponent(post.author.url)}/`}>{post.author.displayName}</Link> on {formatDate(post.published)}
                </div>
                <hr />
                <div className="post-body">
                    {
                        this.renderContent(posts)
                    }
                </div>
                <hr />
                {this.renderFooter()}
                {
                    this.renderComments()
                }
            </Thumbnail>
        );
    }
}

export default withRouter(Post);
