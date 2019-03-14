import React from "react";
import Reflux from "reflux";
import PropTypes from "prop-types";

import ReactMarkdown from "react-markdown";
import { withRouter } from "react-router-dom";
import { PostsStore, PostsActions } from "../discover/PostsStore";
import { Thumbnail, Button } from "react-bootstrap";
import { formatDate } from "../util/DateUtil";
import AuthStore from "../auth/AuthStore";

/**
 * Displays a singular post
 */
class Post extends Reflux.Component {
    static propTypes = {
        post: PropTypes.array.isRequired,
        isPostView: PropTypes.bool
    }

    static defaultProps ={
        isPostView: false
    }

    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
        this.currentPost = this.props.post[0];
    }

    renderHeaderButtons = () => {
        // TODO Add edit button
        const isCurrentUser = (this.currentPost.author.id === this.state.userId);
        return (
            <div className="buttons">
                <i className="fas fa-user-lock">{this.currentPost.visibility}</i>
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
                console.log(content);
                contentList.push(<ReactMarkdown source={content} />);
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
        const commentsLength = this.currentPost.comments.length;
        return (
            <div className="post-footer">
                <p className="categories">{this.currentPost.categories}</p>
                { commentsLength ? <a onClick={this.handlePermalink}>{`${commentsLength} comments`}</a> : null}
            </div>
        );
    }

    handleDeletePost = () => {
        PostsActions.deletePost(this.currentPost.id, this.currentPost.post_id);
    }

    handlePermalink = () => {
        this.props.history.push(`/post/${this.currentPost.id}`);
    }

    render() {
        const { post } = this.props;

        return (
            <Thumbnail>
                <div className="post-header">
                    {/* TODO Add Author URL here */}
                    <p className="post-time">
                        Posted by <a href="#">{this.currentPost.author.displayName}</a> on {formatDate(this.currentPost.published)}
                    </p>
                    {!this.props.isPostView ? this.renderHeaderButtons() : null}
                </div>
                <h3 className="post-title">{this.currentPost.title}</h3>
                <p className="post-desc">{this.currentPost.description}</p>
                <div className="post-body">
                    {
                        this.renderContent(post)
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
