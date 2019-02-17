import React from "react";
import Reflux from "reflux";

import { FormGroup, FormControl, Form, Button, Row, Col } from "react-bootstrap";
import PrivacyDropdown from "./PrivacyDropdown";

import "../../../scss/CreatePost.scss";
import { PostsStore, PostsActions } from "./PostsStore";

export default class CreatePost extends Reflux.Component {
    constructor(props) {
        super(props);
        this.store = PostsStore;
        this.state = {
            privacyKey: "public"
        };
    }

    // TODO submit this data
    handleSubmit = (e) => {
        const form = e.currentTarget;
        // post text value
        console.log(form.elements.post.value);
        const data = {
            content: form.elements.post.value,
            visibility: this.state.privacyKey
        };
        PostsActions.createPost(data);
    }

    handlePrivacySelect = (key) => {
        this.setState({ privacyKey: key });
    }

    // TODO handle adding image (also multi image upload?)
    addFile = (e) => {
        console.log(e.target.files[0]);
    }

    render() {
        return (
            <div className="create-post-wrapper">
                <Form noValidate onSubmit={this.handleSubmit}>
                    <FormGroup controlId="postTitle">
                        <FormControl bsSize="lg" className="form-control-lg" name="title" type="text" placeholder="Title" />
                    </FormGroup>
                    <FormGroup controlId="postDesc">
                        <FormControl bsSize="sm" name="desc" type="text" placeholder="Description" />
                    </FormGroup>
                    <FormGroup controlId="uploadImage">
                        <FormControl
                            id="fileUpload"
                            type="file"
                            accept=".jpeg, .png"
                            multiple
                            onChange={this.addFile}
                        />
                    </FormGroup>
                    <FormGroup controlId="formGroupPost">
                        <FormControl name="content" componentClass="textarea" rows="5" placeholder="What is Up?" />
                    </FormGroup>
                    <FormGroup controlId="originURL">
                        <FormControl name="origin" type="text" placeholder="origin?" />
                    </FormGroup>
                    <FormGroup controlId="sourceURL">
                        <FormControl name="source" type="text" placeholder="source" />
                    </FormGroup>
                    <FormGroup controlId="formTags">
                        <FormControl name="tags" type="text" placeholder="Add tags, separate by comma" />
                    </FormGroup>
                    <Row form>
                        <Col md={3} xs={2}>
                            <PrivacyDropdown
                                handleSelect={this.handlePrivacySelect} />
                        </Col>
                        <Col md={2} xs={3}>
                            <FormGroup className="editMode" controlId="formMode">
                                <FormControl componentClass="select">
                                    <option>Plaintext</option>
                                    <option>Markdown</option>
                                </FormControl>
                            </FormGroup>
                        </Col>
                        <Col md={7}>
                            <Button variant="primary" className="submit-button" type="submit">
                                Create Post
                            </Button>
                        </Col>
                    </Row>
                </Form>
            </div>
        );
    }
}
