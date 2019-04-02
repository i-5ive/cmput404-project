import React from "react";
import Reflux from "reflux";

import { Alert, Button, Form, FormGroup, FormControl, Thumbnail, Radio } from "react-bootstrap";
import ReactMarkdown from "react-markdown";

import { PostsStore, PostsActions } from "../discover/PostsStore";
import LoadingComponent from "../misc/LoadingComponent";
import { formatDate } from "../util/DateUtil";
import Post from "./Post";
import AuthStore from "../auth/AuthStore";
import { Link } from "react-router-dom";

/**
 * Renders details about one specific post
 */
export default class PostView extends Reflux.Component {
    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
        this.state = {
            newCommentText: ""
        };
    }

    componentDidMount() {
        const postId = window.location.href.split("/post/")[1],
            isExternal = postId.includes("http");
        PostsActions.getPost(postId, isExternal);
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.currentPost !== prevState.currentPost && this.state.currentPost) {
            PostsActions.loadComments(this.state.currentPost);
        }
    }

    handleCommentSubmit = (e) => {
        e.preventDefault();
        if (e.currentTarget.elements.comment.value !== "") {
            // eslint-disable-next-line no-undef
            const id = this.state.currentPost.id,
                form = e.currentTarget,
                data = {
                    comment: form.elements.comment.value,
                    author: this.state.userInfo,
                    contentType: form.elements.contentType.value,
                    post: this.state.currentPost.origin,
                    published: (new Date()).toISOString(),
                    id: "1"
                };
            PostsActions.addComment(id, data, this.state.currentPost.origin);
        }
        this.setState({
            newCommentText: ""
        });
    }

	_onCommentChange = (e) => {
	    this.setState({
	        newCommentText: e.target.value
	    });
	};

	// Credit to Brendan McGill for this: https://stackoverflow.com/a/49573628
    handleScroll = (e) => {
        const bottom = e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
        if (bottom) {
            PostsActions.loadComments(this.state.currentPost, this.state.nextCommentsPage);
        }
    }

    renderCommentText(comment) {
        if (comment.contentType === "text/markdown") {
            return <ReactMarkdown source={comment.comment} />;
        } else {
            return <span>{comment.comment}</span>;
        }
    }

    renderComments() {
        const comments = this.state.comments.map((comment) => (
            <Thumbnail key={comment.id}>
                <div className="comment">
                    {this.renderCommentText(comment)} <br />
                    Posted by <Link to={`/profile/${encodeURIComponent(comment.author.url)}/`}>{comment.author.displayName}</Link>  on {formatDate(comment.published)}
                </div>
            </Thumbnail>

        ));
        return (
            <div onScroll={(this.state.nextCommentsPage && !this.state.fetchingComments) ? this.handleScroll : undefined} className="comments-wrapper">
                {
                    comments
                }
                {
                    this.state.fetchingComments && <LoadingComponent />
                }
            </div>
        );
    }

    renderMakeComments() {
        if (this.state.creatingComment) {
            return <LoadingComponent />;
        }
        return (
            <Thumbnail className="comment-thumbnail">
                <Form onSubmit={this.handleCommentSubmit}>
                    <FormGroup controlId="comment">
                        <FormControl name="comment"
                            componentClass="textarea"
                            rows="5"
                            maxLength="130"
                            value={this.state.newCommentText}
                            onChange={this._onCommentChange}
                            placeholder="Comment on this post..." />
                    </FormGroup>
                    <FormGroup controlId="contentType">
                        <div className="comment-type-buttons-row">
                            <Radio radioGroup="contentTypeGroup" name="contentType" value="text/plain" defaultChecked>
                                Plaintext
                            </Radio>
                            <Radio radioGroup="contentTypeGroup" name="contentType" value="text/markdown">
                                Markdown
                            </Radio>
                        </div>
                        <Button bsStyle="primary" disabled={!this.state.newCommentText} className="submit-button submit-button-comment" type="submit">
                            Comment
                        </Button>
                    </FormGroup>
                </Form>
            </Thumbnail>
        );
    }

    render() {
        if (this.state.failedToFetchPost) {
            return <Alert bsStyle="danger">An error occurred while fetching the post</Alert>;
        } else if (!this.state.currentPost) {
            return (
                <div className="center-loader">
                    <LoadingComponent />
                </div>
            );
        }

        return (
            <div className="postView">
                <Post
                    post={this.state.currentPost}
                    images={this.state.currentPostImages}
                    isPostView />
                {this.renderMakeComments()}
                {
                    this.renderComments()
                }
            </div>
        );
    }
}
