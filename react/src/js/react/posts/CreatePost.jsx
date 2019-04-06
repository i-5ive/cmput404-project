/* eslint-disable one-var */
import React from "react";
import Reflux from "reflux";

import { FormGroup, FormControl, Form, Button, ModalFooter, Radio, Badge, ControlLabel, CloseButton, Alert } from "react-bootstrap";
import update from "immutability-helper";

import PrivacyDropdown from "./PrivacyDropdown";

import { PostsStore, PostsActions } from "../discover/PostsStore";
import AuthStore from "../auth/AuthStore";
import LoadingComponent from "../misc/LoadingComponent";
import HomeActions from "../home/HomeActions";

const PRIVATE_STATUS = "PRIVATE";

export default class CreatePost extends Reflux.Component {
    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
        this.state = {
            privacyKey: "PUBLIC",
            tags: [],
            newTagValue: "",
            tagStatusMessage: this._getTagStatusMessage(""),
            visibleTo: [],
            displayVisibleTo: false,
            newUsernameValue: "",
            usernameStatusMessage: this._getUsernameStatusMessage("")
        };
    }

    componentDidMount() {
        const id = window.location.href.endsWith("edit") && window.location.href.split("/post/")[1].split("/edit")[0];
        if (window.location.href.endsWith("edit") && id) {
            PostsActions.getPost(id);
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.successfullyCreatedPost !== prevState.successfullyCreatedPost &&
            this.state.successfullyCreatedPost) {
            this.props.handleClose();
            PostsActions.getPosts();
            HomeActions.loadPosts();
        }
        if (!this.state.fetchingPost && prevState.fetchingPost) {
            const form = document.querySelector("form");
            form.elements.title.value = this.state.currentPost.title;
            form.elements.content.value = this.state.currentPost.content;
            form.elements.contentType.value = this.state.currentPost.contentType;
            form.elements.description.value = this.state.currentPost.description;
            // eslint-disable-next-line
            this.setState({
                tags: this.state.currentPost.categories,
                privacyKey: this.state.currentPost.visibility,
                author: this.state.currentPost.author
            });
            form.elements.unlisted.checked = this.state.currentPost.unlisted;
        }
    }

    handleSubmit = (e) => {
        e.preventDefault();
        const form = e.currentTarget;
        const files = form.elements.fileUpload.files;

        // eslint-disable-next-line no-undef
        const formData = new FormData();
        Array.from(files).forEach((file) => {
            formData.append("imageFiles", file);
        });

        const data = {
            title: form.elements.title.value,
            content: form.elements.content.value,
            contentType: form.elements.contentType.value,
            description: form.elements.description.value,
            categories: this.state.tags,
            visibility: this.state.privacyKey,
            author: this.state.userId,
            unlisted: form.elements.unlisted.checked
        };
        if (data.visibility === PRIVATE_STATUS) {
            formData.append("visibleTo", JSON.stringify(this.state.visibleTo));
        }
        formData.append("postData", JSON.stringify(data));
        formData.append("query", "createPost");
        if (window.location.href.endsWith("edit")) {
            console.log(formData);
            PostsActions.putPost(formData);
        } else {
            PostsActions.createPost(formData);
        }
    }

    handlePrivacySelect = (key) => {
        this.setState({
            privacyKey: key,
            displayVisibleTo: key === PRIVATE_STATUS
        });
    }

	_resetFiles = () => {
	    const files = document.getElementById("fileUpload");
	    if (files) {
	        files.value = "";
	    }
	};

    _onAddTag = (value) => {
        const tags = update(this.state.tags, {
            $push: [value]
        });
        this.setState({
            tags: tags
        });
    }

    _onAddUsername = (value) => {
        const visibleTo = update(this.state.visibleTo, {
            $push: [value]
        });
        this.setState({
            visibleTo: visibleTo
        });
    };

    _onRemoveTag = (value) => {
        const index = this.state.tags.indexOf(value);
        if (index > -1) {
            const tags = update(this.state.tags, {
                $splice: [[index, 1]]
            });
            const state = {
                tags: tags
            };
            if (this.state.newTagValue === value) {
                state.tagStatusMessage = null;
            }
            this.setState(state);
        }
    };

    _onRemoveUsername = (value) => {
        const index = this.state.visibleTo.indexOf(value);
        if (index > -1) {
            const visibleTo = update(this.state.visibleTo, {
                $splice: [[index, 1]]
            });
            const state = {
                visibleTo: visibleTo
            };
            if (this.state.newUsernameValue === value) {
                state.usernameStatusMessage = null;
            }
            this.setState(state);
        }
    };

    _getTagStatusMessage = (tag) => {
        if (tag.length === 0) {
            return "The category can not be blank.";
        } else if (this.state.tags.indexOf(tag) > -1) {
            return "This category is already included.";
        } else if (tag.length > 30) {
            return "Categories can be no more than 30 characters long.";
        } else if (tag === "github") {
            return "This category is reserved and can not be used.";
        }
        return null;
    };

    _getUsernameStatusMessage = (username) => {
        if (username.length === 0) {
            return "The username or URL can not be blank.";
        } else if (this.state.visibleTo.indexOf(username) > -1) {
            return "This user is already included.";
        }
        return null;
    };

    _onTagValueChange = (e) => {
        this.setState({
            newTagValue: e.target.value,
            tagStatusMessage: this._getTagStatusMessage(e.target.value)
        });
    };

    _onUsernameValueChange = (e) => {
        this.setState({
            newUsernameValue: e.target.value,
            usernameStatusMessage: this._getUsernameStatusMessage(e.target.value)
        });
    };

    _addCurrentTag = () => {
        this._onAddTag(this.state.newTagValue);
        this.setState({
            newTagValue: "",
            tagStatusMessage: this._getTagStatusMessage("")
        });
    };

    _addCurrentUsername = () => {
        this._onAddUsername(this.state.newUsernameValue);
        this.setState({
            newUsernameValue: "",
            usernameStatusMessage: this._getUsernameStatusMessage("")
        });
    };

    renderTag = (tag) => {
        return (
            <div key={tag} className="tag">
                <Badge>
                    {
                        tag
                    }
                    <CloseButton onClick={() => {
                        this._onRemoveTag(tag);
                    }} />
                </Badge>
            </div>
        );
    };

    renderTags() {
        return (
            <div>
                <ControlLabel>
                    Categories
                </ControlLabel>
                <div className="tags-container">
                    {
                        this.state.tags.map(this.renderTag)
                    }
                </div>
                <div className="create-tag-wrapper">
                    <FormControl
                        name="addTag"
                        type="text"
                        value={this.state.newTagValue}
                        onChange={this._onTagValueChange}
                        placeholder="Add a new category..." />
                    <Button bsStyle="primary"
                        disabled={Boolean(this.state.tagStatusMessage)}
                        onClick={this._addCurrentTag}>
                        Add
                    </Button>
                </div>
                {
                    this.state.tagStatusMessage && (
                        <div className="error-text">
                            {
                                this.state.tagStatusMessage
                            }
                        </div>
                    )
                }
            </div>
        );
    }

    renderVisibleToUser = (user) => {
        return (
            <div key={user} className="tag">
                <Badge>
                    {
                        user
                    }
                    <CloseButton onClick={() => {
                        this._onRemoveUsername(user);
                    }} />
                </Badge>
            </div>
        );
    };

    renderVisibleTo() {
        return (
            <div className="visible-to">
                <ControlLabel>
                    Visible To
                </ControlLabel>
                <div className="tags-container">
                    {
                        this.state.visibleTo.map(this.renderVisibleToUser)
                    }
                </div>
                <div className="share-user-wrapper">
                    <FormControl
                        name="addTag"
                        type="text"
                        value={this.state.newUsernameValue}
                        onChange={this._onUsernameValueChange}
                        placeholder="Enter the username (or URL) of someone to share with..." />
                    <Button bsStyle="primary"
                        disabled={Boolean(this.state.usernameStatusMessage)}
                        onClick={this._addCurrentUsername}>
                        Add
                    </Button>
                </div>
                {
                    this.state.usernameStatusMessage && (
                        <div className="error-text">
                            {
                                this.state.usernameStatusMessage
                            }
                        </div>
                    )
                }
            </div>
        );
    }

    renderVisibility() {
        return (
            <div>
                <ControlLabel>
                    Visibility
                </ControlLabel>
                <br />
                <PrivacyDropdown
                    handleSelect={this.handlePrivacySelect} />
                <br />
                {
                    this.state.displayVisibleTo && this.renderVisibleTo()
                }
                <br />
            </div>
        );
    }

    renderErrors() {
        if (!this.state.failedToCreatePost) {
            return null;
        } else if (this.state.invalidSharedUsernames) {
            return (
                <Alert bsStyle="danger">
                    {
                        this.state.invalidSharedUsernames.length === 1 ? "The following username was invalid: " : "The following usernames were invalid: "
                    }
                    {
                        this.state.invalidSharedUsernames.join(", ")
                    }
                </Alert>
            );
        }
        return (
            <Alert bsStyle="danger">
                An error occurred while creating the post.
            </Alert>
        );
    }

    render() {
        return (
            <div className="create-post-wrapper">
                {
                    this.renderErrors()
                }
                {
                    this.state.creatingPost && <LoadingComponent />
                }
                <Form onSubmit={this.handleSubmit}>
                    <div className="scrollable">
                        <ControlLabel>
                            Title
                        </ControlLabel>
                        <FormGroup controlId="title">
                            <FormControl name="title" type="text" placeholder="Enter the title of the post" maxLength="100" />
                        </FormGroup>

                        <ControlLabel>
                            Description
                        </ControlLabel>
                        <FormGroup controlId="description">
                            <FormControl componentClass="textarea" name="desc" type="text" placeholder="Enter a description about the post" maxLength="100" />
                        </FormGroup>

                        <ControlLabel>
                            Attached Images
                        </ControlLabel>
                        <FormGroup controlId="fileUpload">
                            <FormControl
                                type="file"
                                accept=".jpeg, .png"
                                multiple
                                className="file-input-button"
                            />
                            <Button onClick={this._resetFiles}
                                bsStyle="primary">Clear Images</Button>
                        </FormGroup>

                        <ControlLabel>
                            Content
                        </ControlLabel>
                        <FormGroup controlId="content">
                            <FormControl name="content" componentClass="textarea" rows="5" placeholder="Enter the content of the post" />
                        </FormGroup>

                        <div className="type-buttons-row">
                            <Radio radioGroup="contentTypeGroup" name="contentType" value="text/plain" defaultChecked>
                                Plaintext
                            </Radio>
                            <Radio radioGroup="contentTypeGroup" name="contentType" value="text/markdown">
                                Markdown
                            </Radio>
                        </div>

                        <div className="unlisted-group">
                            <FormGroup controlId="unlisted">
                                <FormControl name="unlisted" type="checkbox" />
                            </FormGroup>
                            <span>Unlisted</span>
                        </div>

                        {
                            this.renderVisibility()
                        }

                        {
                            this.renderTags()
                        }
                        <br />
                    </div>

                    <ModalFooter>
                        <Button onClick={this.props.handleClose}>
                            Cancel
                        </Button>
                        <Button bsStyle="primary" type="submit" disabled={this.state.creatingPost}>
                            {window.location.href.endsWith("edit") ? "Update Post" : "Create Post"}
                        </Button>
                    </ModalFooter>
                </Form>
            </div>
        );
    }
}
