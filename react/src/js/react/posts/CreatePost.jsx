import React from "react";
import Reflux from "reflux";

import { FormGroup, FormControl, Form, Button, Row, Col } from "react-bootstrap";
import PrivacyDropdown from "./PrivacyDropdown";

import "../../../scss/CreatePost.scss";
import { PostsStore, PostsActions } from "./PostsStore";
import AuthStore from "../auth/AuthStore";

export default class CreatePost extends Reflux.Component {
    constructor(props) {
        super(props);
        this.stores = [PostsStore, AuthStore];
        this.state = {
            privacyKey: "PUBLIC"
        };
    }

    // TODO submit this data
    handleSubmit = (e) => {
        e.preventDefault();
        const form = e.currentTarget;
        // post text value
        // console.log(form.elements.post.value);
        console.log(this.state.userId);
        let categories = form.elements.categories.value;
        if (!categories) {
            categories = [];
        }

        const tags = form.elements.categories.value
        const data = {
            title: form.elements.title.value,
            content: form.elements.content.value,
            source: form.elements.source.value,
            origin: form.elements.origin.value,
            contentType: form.elements.contentType.value,
            description: form.elements.description.value,
            // unlisted: form.elements.unlisted.value,
            categories: categories,
            visibility: this.state.privacyKey,
            author: this.state.userId
        };
        console.log(data);
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
                    <FormGroup controlId="title">
                        <FormControl bsSize="lg" className="form-control-lg" name="title" type="text" placeholder="Title" />
                    </FormGroup>
                    <FormGroup controlId="description">
                        <FormControl bsSize="sm" name="desc" type="text" placeholder="Description" />
                    </FormGroup>
                    <FormGroup enctype="multipart/form-data" controlId="uploadImage">
                        <FormControl
                            id="fileUpload"
                            type="file"
                            accept=".jpeg, .png"
                            multiple
                            // onChange={this.addFile}
                        />
                        <button type="reset" className="btn btn-warning">Reset</button>
                    </FormGroup>
                    <FormGroup controlId="content">
                        <FormControl name="content" componentClass="textarea" rows="5" placeholder="What is Up?" />
                    </FormGroup>
                    <FormGroup controlId="origin">
                        <FormControl name="origin" type="text" placeholder="origin url" />
                    </FormGroup>
                    <FormGroup controlId="source">
                        <FormControl name="source" type="text" placeholder="source url" />
                    </FormGroup>
                    <FormGroup controlId="categories">
                        <FormControl name="tags" type="text" placeholder="Add tags, separate by comma" />
                    </FormGroup>
                    <Row form>
                        <Col>
                            {/* <Col md={3} xs={2}> */}
                            <PrivacyDropdown
                                handleSelect={this.handlePrivacySelect} />
                        </Col>
                        <Col>
                            <FormGroup controlId="unlisted">
                                {/* <FormLabel>Password</FormLabel> */}
                                <FormControl name="unlisted" type="checkbox" label="Unlisted" />
                            </FormGroup>
                        </Col>
                        <Col>
                            <FormGroup controlId="contentType">
                                <FormControl name="contentType" componentClass="select">
                                    <option value="text/plain">Plaintext</option>
                                    <option value="text/markdown">Markdown</option>
                                </FormControl>
                            </FormGroup>
                        </Col>
                        <Col>
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
